# Project Context Master — LLM Gateway

Versi konsolidasi 1.1 · 2026-10-10 · Bahasa kerja: Indonesia.
**Baca [README](README.md) untuk navigasi, lalu mulai context proyek di sini.** Dokumen ini menggabungkan rancangan awal dan pekerjaan aktual;
keputusan desain tidak berubah hanya karena kode atau tes yang ada berbeda.

## 1. Konteks satu menit

Bangun gateway LLM internal perusahaan: **OpenCode → LiteLLM → OpenAI API**.
Developer memakai virtual key, bukan master/provider key. PostgreSQL menyimpan identitas,
key, dan spend. LiteLLM adalah **Data Plane**; custom **Control Plane** baru Phase 2.

| Kontrak Phase 1 yang dipertahankan | Nilai |
|---|---|
| Provider | **OpenAI saja**, tidak ada cross-provider fallback |
| Alias fast | `company-fast` → `openai/gpt-5.6-terra` |
| Alias coding | `company-coding` → `openai/gpt-5.6-sol` |
| Client pertama | OpenCode; jangan mengembalikan template lama tanpa mengecek versi |
| Repo | Tiga komponen: infra/config/e2e; dokumentasi: `llm-gateway-docs` |
| Environment yang diizinkan saat ini | **Docker existing, port 4000**; jangan membuat staging/environment/container baru |
| Posisi | **Phase 1: fungsi lokal teruji; exit gate/release/pilot belum selesai** |
| Phase 2 / Phase 3 | Belum dimulai; tidak otomatis aktif setelah H10D |

**H1–H10D adalah checkpoint teknis lokal, bukan pengganti P1-00…P1-18.**
Bukti terakhir 10 Oktober: 37 E2E/unit (22+3+12), 12 tes operasional, OpenCode fast smoke,
restore 83 tabel, config release/rollback, dan scan sesuai baseline lulus.
Bukti tersebut dibaca ulang pada sesi konsolidasi; **bukan pengujian live baru**.

## 2. Urutan baca dan pemilik informasi

1. Baca master ini seluruhnya.
2. Baca **[Phase 1](architecture/phase-1.md)**: tabel P1, pemetaan H, bukti, gap, next task.
3. Baca **[Keputusan dan evaluasi drift](adr/README.md)** sebelum mengubah scope/arsitektur.
4. Baca **[Log dan handoff aktif](handover/WORK_LOG.md)** untuk checkpoint terbaru.
5. Hanya bila relevan, baca [Phase 2](architecture/phase-2.md) atau [Phase 3](architecture/phase-3.md).
6. Buka source/runbook/bukti yang ditautkan oleh item aktif; jangan memuat semua arsip kode di awal chat.

| Dokumen | Perannya sekarang |
|---|---|
| `MASTER_CONTEXT.md` | Satu pintu masuk dan aturan lintas fase; master konsolidasi aktif |
| `architecture/phase-1.md` | Pemilik status acceptance P1 dan pemetaan ke H1–H10D |
| `architecture/phase-2.md`, `architecture/phase-3.md` | Roadmap masa depan; tidak berisi klaim implementasi |
| `adr/README.md` + `adr/001…017-*.md` | Register keputusan/drift; detail setiap ADR mempertahankan ID asli |
| `handover/WORK_LOG.md` | Catatan perubahan context, bukti dan tugas berikutnya |
| [PROJECT_MASTER_CONTEXT.md](archive/PROJECT_MASTER_CONTEXT.md) | Baseline rancangan asli; teks PLANNING/TODO adalah snapshot awal |
| [LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md](archive/LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md) | Arsip detail H1–H10; potongan kode/status lama bukan instruksi eksekusi terbaru |
| [Laporan H1–H10](reports/PHASE1_H1_H10_REPORT.md) | Hasil sesi implementasi sebelumnya, bukan penutupan seluruh gate awal |

Kedua sumber asli dipertahankan, hanya diberi penunjuk baca. Jangan memperbarui tiga master
secara paralel. Status aktif cukup di dokumen fase; master tetap ringkas dan log append-only.
Permintaan user terbaru memusatkan semua dokumentasi/laporan ke repo `llm-gateway-docs` yang sudah ada.
Dokumen root lama hanya penunjuk; rancangan awal dan handoff lengkap berada di `archive/`.
Ini perubahan kepemilikan dokumentasi yang diizinkan, bukan perubahan Data Plane/roadmap fase.

## 3. Urutan otoritas dan disiplin bukti

Permintaan eksplisit terbaru user → ADR yang disetujui → master konsolidasi + baseline
keputusan yang dirujuk → source/bukti kondisi terpasang → catatan historis.
**Source membuktikan keadaan aktual, bukan mengesahkan penyimpangan desain.**
Usulan/temuan tidak menjadi persetujuan hanya karena ditulis dalam dokumen.

| Status | Arti |
|---|---|
| `LOCAL_VERIFIED` | Ada implementasi dan bukti lokal dalam batas skenario yang disebut |
| `PARTIAL` | Sebagian acceptance terbukti, sisanya belum |
| `OPEN` / `NOT_VERIFIED` | Keputusan/bukti belum tersedia; bukan otomatis bug |
| `NOT_STARTED` | Pekerjaan belum dimulai |
| `APPROVED_OVERRIDE` | Perubahan spesifik yang memang diinstruksikan user; jangan perluas cakupannya |
| `PROPOSED` | Belum diizinkan/diterapkan |
| `DONE_VERIFIED` | Acceptance lengkap + commit/PR/review sesuai policy + bukti + docs |

Jangan menyamakan file dibuat, pytest collection, scan PASS, health HTTP 200, atau test
unit dengan acceptance live/production. Kegagalan lama yang sudah diperbaiki tetap ada
sebagai riwayat. Model access terbukti melalui gateway untuk credential saat tes;
akses langsung API/billing corporate dan akurasi harga belum otomatis terbukti.

## 4. Aturan yang tidak boleh dilanggar

- Phase 1 tetap dua alias dan OpenAI saja. Perubahan mapping/provider membutuhkan ADR/persetujuan.
- Jangan membangun custom UI, SSO, backend control plane, billing engine atau HA pada Phase 1.
- Security minimum (TLS lintas mesin, secret, ACL, backup) tetap Phase 1; enterprise scale Phase 3.
- Gunakan satu `LiteLLMClient` di E2E: `tests/client.py` HTTP, `conftest.py` fixture/cleanup,
  `test_*.py` assertion. Jangan tambah admin client abstraction kedua.
- `models/*.yaml`: identitas dari filename; bukan file config runtime yang otomatis di-load.
- Jangan hard-delete audit. Offboarding sekarang snapshot + koordinasi freeze provisioning;
  belum ada atomic revocation terhadap penerbitan key bersamaan atau integrasi SSO.
- Redis ada dan menjadi dependency operasional sekarang, tetapi kebutuhan distributed cache/
  rate limiting belum dibuktikan. Jangan menghapusnya atau mengklaim wajib desain tanpa keputusan.
- Jangan menaikkan vulnerability baseline diam-diam. PASS baseline bukan zero vulnerabilities.
- Jangan menaruh `.env`, raw virtual key, dump, prompt sensitif, atau salt dalam Git/context.
- Jangan membuat staging lagi. Perintah scanner default yang membuat container juga tidak
  dijalankan pada constraint sekarang; gunakan opsi native bila pengujian memang diperlukan.
- Perubahan major harus dijelaskan dahulu: masalah, opsi, dampak, risiko, migrasi/rollback,
  dan persetujuan user. Sesi konsolidasi ini tidak mengimplementasikannya.

## 5. Keadaan penting dan langkah berikutnya

Root workspace belum merupakan repo Git; tiga komponen dan satu repo dokumentasi terpisah.
Dokumentasi kini berada di repo docs existing, tetapi migrasi dan banyak perubahan komponen belum commit. H7 merge gate sebelumnya dikonfirmasi user; bukan bukti CI candidate terbaru hijau.
Tidak ada release tag/sign-off atau bukti pilot 2–5 developer pada kumpulan bukti ini.

**Risiko/gap yang harus dibaca sebelum deploy:**
- Validator belum mengunci exact upstream/provider/alias; gap berhasil direproduksi offline.
- Gateway bind semua interface; TLS/admin isolation/log content minimization belum dibuktikan.
- Tes budget saat ini key-level + team RPM; bukan bukti seluruh member/team budget dan TPM.
- Biaya positif/retensi audit bukan pembuktian harga/token akurat terhadap provider billing.
- OpenCode fast smoke + API tool calling bukan bukti agent coding menyeluruh kedua alias.
- Provider 429/5xx/timeout dan enforcement selama DB outage belum terbukti oleh health drill.
- Release/rollback hanya config, image/schema sama; bukan deployment server lintas versi.
- Temuan scan terakhir: PostgreSQL 1 Critical/28 High, Redis 2 High, LiteLLM 0/0;
  nilai ini historis tanggal tes, bukan janji keadaan keamanan saat ini.

**Tugas sesi terbaru:** DOC-MIGRATE — pusat dokumentasi, ADR, runbook dan handover.
DOC-CONSOLIDATE tetap tercatat sebagai sesi evaluasi sebelumnya.
**Usulan next task:** `P1-06 / F-01` menguatkan validator kontrak dan konsistensi katalog,
setelah user melanjutkan pekerjaan. Tidak mulai deployment atau Phase 2 otomatis.
M-03 penempatan dokumentasi diselesaikan dengan repo docs existing atas instruksi user;
publikasi/commit belum dilakukan. M-01/M-02/M-04/M-05 tetap terbuka dalam register drift.

## 6. Prompt chat baru

```text
Mulai dari llm-gateway-docs/README.md dan llm-gateway-docs/MASTER_CONTEXT.md.
Lanjutkan architecture/phase-1.md, adr/README.md, handover/WORK_LOG.md di repo docs.
Pertahankan OpenAI-only, dua alias yang ditetapkan, tiga repo komponen dan Docker existing 4000.
H10D lokal selesai bukan Phase 1 exit gate. Cocokkan source/Git dengan bukti sebelum coding.
Kerjakan hanya item yang saya minta; usulan next P1-06/F-01 belum dikerjakan.
Jangan buat staging atau mulai Phase 2; minta keputusan sebelum perubahan major.
Laporkan ID, file, hasil tes aktual, batasan, commit jika ada, dan update dokumen fase/log.
```
