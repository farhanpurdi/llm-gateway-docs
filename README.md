# Company AI Platform — pusat dokumentasi LLM Gateway

**Mulai di sini untuk handover ke manusia atau AI.** Repository ini menjelaskan tujuan,
rancangan, pekerjaan yang sudah terbukti, batasan, dan langkah yang belum dikerjakan.
Tidak berisi secret, database backup, atau deployment environment.

## Apa yang dibangun?

Satu pintu akses AI untuk developer perusahaan. Developer menggunakan **OpenCode** dan
virtual key miliknya; **LiteLLM** mengatur akses model, batas pemakaian dan pencatatan
biaya, lalu meneruskan request ke **OpenAI**. Provider key tetap di server.

Manfaat yang dituju: akses bisa dicabut per pengguna, biaya bisa ditelusuri, dan tools
client memakai nama model perusahaan yang stabil. Backend administrasi dan portal
custom baru direncanakan pada Phase2; keandalan enterprise dikembangkan pada Phase3.

**Posisi sekarang: Phase 1 DITUTUP DENGAN CATATAN, versi v0.0.1**, atas keputusan
pengguna 18 Oktober 2026 (O-10). [Tujuh feedback dan catatan penutupan](reports/PHASE1_V0_0_1_CLOSEOUT.md)
menjadi acuan aktif. **[Mulai menggunakan gateway](developer/panduan-penggunaan.md)**
untuk panduan operator/developer yang sederhana. Phase2/3 belum dimulai.
Untuk pekerjaan lokal tetap **Docker existing port4000; jangan membuat staging/container baru.**
Pengguna akan setup VM GCP sesuai tahapan O-10; sesi dokumentasi ini tidak menjalankan deploy.
Paket P1-06/F-01/F-02 selesai dalam scope static/offline pada 12 Oktober;
[laporan dan kode](reports/P1_06_MODEL_CONTRACT_REPORT.md). P1-09/P1-10 kini
**LOCAL_VERIFIED**: limit pilot, reset budget anggota, token dan biaya kedua alias
telah diuji; [laporan dan kode](reports/P1_09_P1_10_LIMITS_COST_REPORT.md).
P1-11/P1-12 juga **LOCAL_VERIFIED** pada17Oktober: onboarding dan agent kedua alias,
79 unit/5 smoke/6 live terfokus PASS; [laporan dan kode](reports/P1_11_P1_12_OPENCODE_REPORT.md).
Full cross-check akhir kini PASS: 97 unit, 5 smoke, 30 live, 2 outage dan 13 skenario
native; config 63 serta infra 31 tes offline PASS. Lihat
[laporan akhir per milestone](reports/PHASE1_FINAL_CROSSCHECK_REPORT.md).
Empat PR main sudah direview/merged; isi main identik candidate yang diuji. CVE image
diterima untuk fase ini; VM GCP/default/HTTP awal dan keamanan bertahap dipilih.
Snapshot/biaya menunggu diskusi manager. TTLRedis24jam adalah target yang belum
diterapkan; tag v0.0.1 dan deployment VM belum dibuat/dibuktikan oleh pencatatan ini.

## Jalur baca sesuai kebutuhan

| Pembaca | Urutan yang disarankan |
|---|---|
| Orang baru / pemilik project | [Overview](architecture/overview.md) → [master](MASTER_CONTEXT.md) → [Phase1](architecture/phase-1.md) |
| AI yang melanjutkan pekerjaan | [Master](MASTER_CONTEXT.md) → [Phase1](architecture/phase-1.md) → [keputusan/drift](adr/README.md) → [log](handover/WORK_LOG.md) → [protokol AI](handover/AI_CONTINUATION.md) |
| Developer pengguna gateway | [Panduan penggunaan sederhana](developer/panduan-penggunaan.md) → [Model catalog](developer/model-catalog.md) → [OpenCode](developer/opencode.md) → [API](developer/api.md) |
| Pengembang dengan Codex | [Skill proyek dan contoh penggunaan](developer/codex-skills.md) |
| Operator | [Panduan operasi](operations/README.md) → [deployment](operations/deployment.md) / [backup](operations/backup.md) / [incident](operations/incident.md) / [rollback](operations/rollback.md) |
| Engineer pengganti | [Checklist handover](handover/HUMAN_HANDOVER.md) → source terkait → bukti pada [reports](reports/README.md) |
| Reviewer arsitektur | [Indeks ADR](adr/INDEX.md) → [drift/open decisions](adr/README.md) → dokumen fase yang relevan |

Jangan membaca seluruh arsip/kode laporan sekaligus. Baca bagian inti di atas, kemudian
ikuti tautan item tugas aktif. Ini mengurangi kehilangan konteks di dokumen panjang.

## Struktur dan pemilik informasi

```text
llm-gateway-docs/
├── README.md                  # navigasi untuk manusia dan AI
├── MASTER_CONTEXT.md          # aturan/posisi lintas fase, satu master aktif
├── architecture/              # overview + roadmap/status Phase1–3
├── adr/                       # ADR001–017 + drift/override/keputusan terbuka
├── operations/                # deployment, rollback, backup, incident, lifecycle
├── developer/                 # OpenCode, API, model catalog, compatibility
├── handover/                  # log, protokol AI, checklist manusia
├── reports/                   # hasil milestone, kode snapshot dan evidence historis
├── archive/                   # rancangan awal dan handoff panjang
└── scripts/validate-docs.py    # validasi tautan, struktur dan integritas migrasi
```

- Rancangan/kontrak: master + ADR. Status acceptance: file fase terkait.
- Keputusan major belum disetujui: register ADR/drift; tidak boleh dianggap izin coding.
- Log adalah riwayat sesi, bukan master kedua. Laporan adalah bukti bertanggal.
- Source implementasi tetap di tiga repo komponen; **docs bukan runtime config**.
- Semua dokumen operasional sekarang dipusatkan di repo ini. README komponen hanya
  memberi navigasi/petunjuk menjalankan repo masing-masing.
- Tiga file context root sudah tidak ada pada pemeriksaan 2026-10-12. Master aktif ada di
  repo ini; rancangan awal dan handoff lama tetap tersedia di `archive/`.
- Urutan pekerjaan sampai rilis tersedia pada [rencana penutupan Phase 1](architecture/phase-1-completion-plan.md).

## Cara menyimpan workspace untuk handover

```text
company-ai-platform/            # folder biasa; bukan parent Git yang dibuat sesi ini
├── llm-gateway-docs/           # repo docs existing
├── llm-gateway-infra/          # repo Docker dan script operasi
├── llm-gateway-config/         # repo config/model/policy/client template
└── llm-gateway-e2e/            # repo pengujian
```

Tautan antarrepo memakai layout sibling ini. Pada Git web viewer repo terpisah, tautan
ke source sibling mungkin tidak dapat dinavigasi; clone berdampingan atau gunakan URL
commit repo yang disepakati saat rilis. Jangan mengarang remote/organization.
Validasi repo docs sendiri boleh melewati tautan source sibling yang belum di-checkout;
validasi handover lengkap memerlukan empat repo dan mode `--workspace`.

```bash
# Dari llm-gateway-docs; tidak mengakses Docker/provider:
python3 scripts/validate-docs.py --workspace
```

Migrasi docs sudah tercatat pada commit lokal **`1d07d02`** (diperiksa 2026-10-12).
Push/review remote belum diverifikasi. Perubahan ketiga repo komponen masih belum tercakup
seluruhnya di HEAD; pembaruan rencana terbaru juga perlu dicakup saat publikasi berikutnya.
Tidak membuat repo/remote/submodule baru. Data rahasia diserahkan lewat jalur terpisah yang aman.
