# Laporan P1-09/P1-10 — Limit pilot, token dan biaya

Pengujian: 2026-10-13; penutupan dokumentasi: 2026-10-14, Asia/Jakarta. Acuan user: [pilot.yaml](../../llm-gateway-config/policies/teams/pilot.yaml), kedua alias; Docker existing port 4000.

Status: **P1-09 dan P1-10 LOCAL_VERIFIED** dalam skenario yang disebut; belum release DONE atau Phase 1 exit gate.

## P1-09 — Batas penggunaan pilot

Tujuannya memastikan limit yang disepakati benar-benar tersimpan dan menolak penggunaan yang melampaui batas.

| Pengaturan pilot | Nilai |
|---|---|
| Model | company-fast dan company-coding |
| Budget team | US$10 |
| Budget anggota dalam team | US$2; dibagi oleh seluruh key anggota tersebut |
| Request team | 30/menit; dibagi seluruh anggota/key team |
| Token team | 100.000/menit; dibagi seluruh anggota/key team |
| Durasi team dan anggota | 30d, dengan reset kalender versi LiteLLM terpasang |

**Bug yang ditemukan dan diperbaiki:** script add-member sebelumnya mengirim nominal US$2 tanpa durasi. Reproduksi lewat script asli menunjukkan budget anggota tersimpan dengan `budget_duration: null` dan `budget_reset_at: null`. Jadi batas anggota tidak otomatis kembali ke nol. Script sekarang mengirim `budget_duration: "30d"`, sesuai maksud budget bulanan dan periode team existing.

```python
# scripts/teams/add-member.sh: payload native LiteLLM
{
    "team_id": team_id,
    "max_budget_in_team": member_budget,
    "budget_duration": "30d",
    "member": {"role": "user", "user_id": user_id},
}
```

Nilai file pilot tidak diubah. Tes persistence memeriksa nominal asli US$10/US$2, RPM30/TPM100000 dan kedua alias pada identitas disposable, bukan hanya membaca YAML. Tes enforcement memakai batas kecil pada team/key tes agar tidak harus menghabiskan budget atau mengirim 100.000 token. Override fixture bukan perubahan policy pilot perusahaan.

Tes tambahan memeriksa beberapa key tidak dapat menghindari RPM/TPM team, recovery pada team yang sama, kedua key anggota ditolak saat budget anggota habis, anggota lain masih boleh memakai budgetnya, seluruh anggota ditolak saat budget team habis, dan key lain masih boleh dipakai bila hanya satu key kehabisan budget sendiri.

**Semantik reset yang terverifikasi:** pada LiteLLM 1.104.0 dengan setting existing UTC/midnight, `30d` dijadwalkan ke awal bulan berikutnya. Contoh aktual: dibuat 13 Oktober → reset 1 November 2026 pukul 00:00 UTC. Ini mengoreksi asumsi catatan sebelumnya bahwa selalu 30 hari sejak provisioning. Scheduler existing memeriksa budget jatuh tempo setiap 597–605 detik; rollover dapat tertunda sampai pemeriksaan berikutnya. Tes reset memakai budget anggota 5 detik hanya pada fixture dan menunggu scheduler existing, tanpa mengubah jam/server/scheduler.

Perubahan script berlaku pada provisioning berikutnya. Anggota lama dengan durasi null tidak dimigrasikan diam-diam. Operator perlu menentukan user/team pilot nyata dan memperbarui durasi anggota lama secara terarah bila mereka akan dipakai; histori/spend tidak dihapus.

## P1-10 — Token dan biaya bisa diperiksa sampai identitas pemakai

Tujuannya menaikkan pembuktian dari sekadar spend positif menjadi pemeriksaan tiap request. Masing-masing alias diuji dengan dua anggota/key berbeda. Setiap request memakai teks kecil, `max_tokens: 16`, reasoning none dan service tier default.

Tes mencocokkan ID respons provider dengan row spend PostgreSQL yang dibaca melalui API gateway. Pada versi terpasang, `request_id` row memakai ID respons provider; header `x-litellm-call-id` adalah ID trace gateway yang berbeda. Assertion memeriksa user, hash identitas key, team, alias logical, upstream, seluruh token dan biaya; polling juga memeriksa counter key/anggota/user/team.

Tarif standar per sejuta token, diverifikasi 13 Oktober melalui dokumentasi resmi dan tabel aktif LiteLLM:

| Alias | Input | Cached input | Output |
|---|---|---|---|
| company-fast | US$2 | US$0,20 | US$12 |
| company-coding | US$4 | US$0,40 | US$20 |

Sumber: [OpenAI GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [OpenAI GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol). Harga merupakan snapshot saat verifikasi; test oracle perlu diperiksa kembali bila harga berubah. Tidak menambahkan pricing override pada runtime.

Rumus tes independen:

```python
cost = (
    (prompt_tokens - cached_tokens) * input_rate
    + cached_tokens * cached_input_rate
    + completion_tokens * output_rate
)
# Reasoning sudah termasuk completion_tokens; jangan dihitung dua kali.
```

Rumus memakai Decimal, memeriksa token valid, menolak input/cache yang tidak konsisten dan tidak menganggap long context/cache creation sebagai tarif teks pendek. Tes negatif membuktikan attribution salah, token salah, spend NaN dan biaya berbeda gagal pada assertion yang sama dengan tes live.

| Bukti dua request per alias | Prompt / completion per request | Biaya hitung | Spend tersimpan |
|---|---|---|---|
| company-fast | 12 / 4 | US$0.000144 | US$0.000144 |
| company-coding | 12 / 5 | US$0.000296 | US$0.000296 |

Total empat request pembuktian biaya: US$0.000440. Selisih hitung vs row/counter berada dalam toleransi US$0.00000001. Angka ini bukan total seluruh percobaan/regresi sesi.
Query PostgreSQL read-only pada namespace baru `e2e-p109-*` mencatat 33 request dengan
spend positif: 29 Terra (US$0.002224) dan 4 Sol (US$0.000592), total **US$0.002816**.
Angka ini termasuk percobaan awal namespace tersebut, tetapi tidak mencakup fixture
regresi limits lama atau invoice OpenAI. [Aggregate aktual](p1-09-10-evidence/cleanup-accounting.jsonl).

Helper HTTP tetap pada satu LiteLLMClient. Model-info disaring agar hanya mengembalikan mapping/harga publik; error HTTP tidak mencetak body mentah. Credential fixture memakai repr tersensor agar kegagalan assertion tidak memperlihatkan virtual key. Tidak membangun billing engine atau client admin kedua.

## Perubahan source dan kode lengkap

- Infra: add-member.sh menambah durasi; test-operations.py menguji payload script create-team/add-member lewat curl stub tanpa Docker/provider.
- E2E: client.py menambah pembacaan budget/member/harga dengan output aman; conftest.py membaca pilot.yaml dan membuat fixture dua anggota/empat key dengan cleanup terkonfirmasi walau provisioning gagal sebagian.
- E2E: accounting.py menambahkan oracle biaya independen; test_spend.py mengganti tes spend positif dengan rekonsiliasi kedua alias; test_pilot_limits.py menambah persistence, shared limits, recovery dan reset.
- E2E: unit/test_accounting.py dan unit/test_suite_validator.py menambah negatif biaya/atribusi/privacy dan melindungi enam tes baru agar tidak hilang diam-diam; validate-suite.py kini mewajibkan 20 fungsi gateway.
- requirements.txt mencatat PyYAML yang sudah tersedia di .venv existing. Tidak menginstal dependency atau membuat environment baru.

[Isi lengkap sebelas file + SHA-256](P1_09_P1_10_CODE_APPENDIX.md). File shared mempertahankan kode sesi sebelumnya. Source awal/akhir dan scope tersedia pada [evidence](p1-09-10-evidence/README.md).

## Hasil pengujian dan percobaan awal

| Pemeriksaan | Hasil |
|---|---|
| Config CI 7 tahap, 63 tes kontrak | PASS, exit 0 |
| Infra CI 7 tahap, 23 tes operasi | PASS, exit 0 |
| E2E CI 8 tahap, 61 tes offline | PASS, exit 0 |
| Total offline unik | 147; hitungan CI/unit tidak digandakan |
| Smoke health/auth/model exposure/persistence pilot | 4 PASS, exit 0 |
| Regresi live P1-09/P1-10 dan limits existing | 11 PASS, exit 0; 676,73 detik termasuk menunggu reset native |
| Validasi dokumen dan scope | PASS: 59 Markdown; roadmap/ADR valid, 24 evidence historis identik; 11 hash kode cocok dan 9 asset aktif identik |
| Pemeriksaan diff empat repo | PASS, exit 0; tidak ada kesalahan whitespace |

Percobaan awal dipertahankan dalam evidence: satu mock unit masih memiliki side_effect Unexpected GET; diperbaiki lalu unit PASS. Smoke awal salah mengasumsikan reset rolling dan menganggap respons team/update sebagai row team; assertion diperbaiki sesuai calendar/persistence API. Tes spend awal memakai ID trace gateway sehingga tidak menemukan row; ID respons provider diperiksa lalu diperbaiki. Assertion awal juga dapat memperlihatkan credential dalam repr container; log evidence disensor dan fixture/error helper diperkuat. Reset awal timeout 100 detik; kode scheduler menunjukkan interval sekitar 10 menit sehingga waktu tunggu tes diperbaiki. Ini masalah harness/semantik, dibedakan dari bug script durasi anggota.

## Batas bukti dan pekerjaan berikutnya

Tidak ada perubahan routing/model/provider, YAML pilot/runtime, image/schema, jaringan, Redis, environment, staging, restart/container baru, commit/push atau deployment. Query akhir mengonfirmasi 22 team dan 80 key tes P1-09 sudah diblokir, bukan dihapus, agar audit tetap tersedia. Anggota/team pilot nyata belum dipilih atau dimigrasikan.

Bukti biaya berlaku untuk Chat Completions teks pendek, default tier dan respons yang diuji. Diskon cached input/reasoning diuji unit; workload cache panjang, cache write, streaming/tools/multimodal/tier lain serta invoice OpenAI belum direkonsiliasi. Spend asinkron berarti budget bukan dompet prepaid yang menjamin tidak pernah melewati batas satu request; tes tiny-budget sengaja membuktikan request pertama dapat melampaui cap lalu request berikutnya ditolak. Concurrency/multi-pod/stress test bukan bukti sesi ini.

Native token/cost tracking telah diperiksa sesuai acceptance awal P1-09/P1-10; gate commit/review/CI candidate, cap/alert provider dan ownership billing tetap terpisah. Berikutnya P1-11/P1-12: onboarding dan agent OpenCode kedua alias, streaming dan tool sampai hasilnya digunakan. Phase 1 belum ditutup dan belum ada persetujuan deployment server.
