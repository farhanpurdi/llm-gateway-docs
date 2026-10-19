# Project Context Master — LLM Gateway

Versi konsolidasi **1.12**, diperbarui **19 Oktober 2026**, Asia/Jakarta.
Baca [README](README.md) untuk navigasi; dokumen ini adalah context aktif lintas fase.
Rancangan awal dan seluruh evidence historis dipertahankan pada arsip/laporan terkait.

## 1. Konteks satu menit

Gateway LLM internal perusahaan: **OpenCode → LiteLLM → OpenAI API**.
Developer memakai virtual key pribadi; PostgreSQL menyimpan identitas, key dan spend.
LiteLLM adalah Data Plane. Custom Control Plane baru direncanakan pada Phase 2.

**Phase 1 DITUTUP DENGAN CATATAN untuk v0.0.1**, atas persetujuan eksplisit pengguna
18 Oktober 2026: **APPROVED_OVERRIDE O-10**. Tujuh feedback, batas penutupan dan
tindak lanjut dimiliki [laporan closeout](reports/PHASE1_V0_0_1_CLOSEOUT.md).
Penutupan diterima melalui hasil teknis dan pengecualian; pengujian VM/server,
snapshot, TTL Redis dan penerimaan perusahaan yang belum ada bukti tidak menjadi PASS.
**Phase 2 dan Phase 3 tetap NOT_STARTED.**

| Kontrak | Nilai yang dipertahankan |
|---|---|
| Provider | OpenAI saja, tanpa cross-provider fallback |
| Alias fast | `company-fast` → `openai/gpt-5.6-terra` |
| Alias coding | `company-coding` → `openai/gpt-5.6-sol` |
| Client pertama | OpenCode 2.0.18 yang sudah diuji |
| Repositori | Empat sibling repo: infra/config/e2e/docs; root bukan Git |
| Runtime kerja lokal | Docker existing port4000; jangan membuat staging/container/environment baru untuk tugas dokumentasi |
| Arah deployment | VM GCP, setting default/HTTP awal dan keamanan bertahap sesuai O-10; belum dieksekusi/diverifikasi di sesi ini |
| Policy | `pilot.yaml`: kedua alias, team US$10/anggota US$2/RPM30/TPM100000 |
| Redis | Dependency operasional existing; target TTL24jam dicatat, belum diaktifkan sebagai cache native |
| Versi rilis | v0.0.1 disepakati; tag Git/publikasi release belum dibuat pada pemeriksaan 18 Oktober |

## 2. Bukti yang sudah tersedia

Pengujian terakhir **17 Oktober 2026**, bukan tes ulang sesi pencatatan:
full run **134 pytest PASS, exit0** (97 unit/5 smoke/30 live/2 outage), ditambah
**13 skenario native**. Config63 dan infra31 tes offline PASS; total offline unik191.
Kedua agent OpenCode, streaming/tools, limit/reset/biaya, rotasi key, restore83tabel,
config-only rollback serta audit privasi/cleanup PASS sesuai batas skenario.
[Laporan per milestone](reports/PHASE1_FINAL_CROSSCHECK_REPORT.md) dan
[32 file kode](reports/PHASE1_FINAL_CODE_APPENDIX.md) menyimpan implementasi/evidence.

Pengguna mereview dan merge PR ke main: config#4, infra#7, E2E#6, docs#1.
Pemeriksaan ulang18Oktober: tree main keempat repo identik dengan candidate yang
diuji. Enam CI promosi PASS; CI docs pada b53677f juga PASS sebelum merge.
[Refs/PR/version record](reports/phase1-v0.0.1-evidence/release-record.json).
Pembaruan closeout/panduan dipublikasikan pada branch
`docs/phase1-v0.0.1-closeout-20261018` atas instruksi push pengguna19Oktober.
Status merge ke main dan CI terbaru mengikuti PR branch tersebut; publikasi branch
tidak membuat tag v0.0.1 atau menjalankan deployment.

H1–H10D adalah checkpoint teknis lokal. P1-00…P1-18 tetap pemetaan acceptance;
[Phase 1](architecture/phase-1.md) membedakan bukti teknis dan penutupan melalui O-10.

## 3. Keputusan yang mengikat

Permintaan eksplisit terbaru pengguna → ADR/override yang disetujui → master +
baseline yang dirujuk → source/bukti aktual → catatan historis. Source membuktikan
implementasi, bukan mengesahkan perubahan desain atau penerimaan risiko sendiri.

O-01 memakai Docker lokal existing4000; O-04 memusatkan docs/report pada repo docs;
O-06 memilih pilot.yaml; O-07 menunda pilot nyata/peserta/PIC; O-08 menetapkan
CI offline GitHub + full live manual lokal; O-09 menyiapkan promosi kedua history.
Pengguna kemudian melakukan review/merge sendiri, terverifikasi GitHub.

**O-10, 18 Oktober:** Phase 1 ditutup v0.0.1 dengan catatan. CVE image diterima untuk
fase ini; dua kandidat DHI dicatat untuk evaluasi mendatang. VM GCP/default/HTTP
awal dan keamanan bertahap dipilih. Snapshot/backup serta biaya didiskusikan dengan
manager. TTL Redis24jam dan belum ada kebijakan pembatasan pengguna Redis tambahan
dicatat sebagai arah, bukan pengaturan yang sudah terbukti aktif. Detail satu pintu:
[register ADR](adr/README.md) dan [tujuh feedback](reports/PHASE1_V0_0_1_CLOSEOUT.md).

| Status bukti/keputusan | Arti |
|---|---|
| `LOCAL_VERIFIED` | Implementasi dan bukti lokal dalam batas skenario |
| `PARTIAL` | Sebagian acceptance terbukti |
| `OPEN` / `NOT_VERIFIED` | Keputusan/bukti tertentu belum tersedia |
| `NOT_STARTED` | Pekerjaan belum dimulai |
| `APPROVED_OVERRIDE` | Pengecualian/perubahan scope yang disetujui pengguna; termasuk penutupan O-10 dengan catatan |
| `PROPOSED` | Usulan belum disetujui |
| `DONE_VERIFIED` | Acceptance terkait lengkap beserta bukti dan proses review yang diperlukan |

Label fase **ditutup dengan catatan** memakai APPROVED_OVERRIDE O-10. Jangan mengubah
seluruh baris P1 menjadi DONE_VERIFIED: deployment GCP/TTL/snapshot/pilot nyata yang
belum diuji tetap NOT_VERIFIED, walaupun tidak lagi menghalangi penutupan fase ini.

## 4. Urutan baca dan pemilik informasi

1. Master ini untuk posisi dan aturan lintas fase.
2. [Phase 1](architecture/phase-1.md) untuk status P1 dan peta H1–H10D.
3. [Register ADR](adr/README.md) untuk keputusan/drift, termasuk O-10.
4. [Closeout v0.0.1](reports/PHASE1_V0_0_1_CLOSEOUT.md) dan checkpoint terbaru [work log](handover/WORK_LOG.md).
5. [Panduan penggunaan](developer/panduan-penggunaan.md) untuk operator/developer;
   source/runbook/evidence dibuka hanya bila terkait tugas.
6. [Phase 2](architecture/phase-2.md)/[Phase 3](architecture/phase-3.md) hanya ketika relevan atau diperintahkan.

Arsip [rancangan awal](archive/PROJECT_MASTER_CONTEXT.md) dan
[handoff H1–H10](archive/LLM_GATEWAY_PROJECT_CONTEXT_HANDOFF.md) adalah snapshot
historis, bukan master paralel. Catatan lama IN_PROGRESS/open gate tidak membatalkan
O-10 yang lebih baru. Evidence historis dan attempt gagal tidak ditulis ulang.

## 5. Aturan dan batas yang tetap berlaku

- Dua alias/OpenAI-only tetap; perubahan mapping/provider harus disetujui.
- Jangan mulai custom UI/control plane/SSO/HA/Phase2/3 dari penutupan ini.
- Source aplikasi tetap tiga repo komponen; docs di repo docs. Root bukan parent Git/monorepo.
- Satu HTTP client E2E `tests/client.py`; fixtures/cleanup di conftest dan assertion di test_*.py.
- Identitas katalog model berasal dari filename; katalog bukan generator runtime otomatis.
- Jangan commit `.env`, raw key, salt, dump, prompt/source/response sensitif atau log mentah.
- Pertahankan audit: block/offboard/rotate, tidak hard-delete. Freeze provisioning manual
  saat offboard tetap diperlukan; belum atomic/SSO deprovision.
- Security minimum tetap tujuan desain. Penundaan HTTP/HTTPS/firewall/admin/snapshot
  adalah pengecualian eksplisit O-10, tidak mengubahnya menjadi kontrol yang sudah diterapkan.
- Jangan menghapus Redis, mengaktifkan cache, mengubah TTL seluruh key atau membuka
  port Redis dari tugas pencatatan. Target24jam bukan retensi spend PostgreSQL,
  expiry virtual key, durasi budget atau reset rate limit.
- Budget30d teruji reset awal bulan berikutnya UTC, scheduler sekitar10menit;
  reset bukan prepaid cap dan anggota lama belum otomatis dimigrasikan.
- Baseline scan hanya temuan fixable sesuai policy; PASS bukan zero-CVE. CVE diterima
  untuk penutupan ini oleh pengguna, bukan dibuktikan hilang atau otomatis false positive.
- Full live/outage berbayar/berdampak dikerjakan serial dan sesuai scope; tugas docs
  tidak menjalankannya. Jangan mengulang paid test untuk perubahan docs/metadata saja.
- Perubahan major dijelaskan sebelum implementasi. Persetujuan yang sudah ada tidak
  ditanyakan ulang; evaluasi DHI/TTL/deploy nyata membutuhkan task/target yang konkret.

## 6. Langkah setelah penutupan

Pengguna akan setup VM GCP, mengamati trafik, lalu berdiskusi dengan manager.
Belum ada IP/domain, bukti deploy, penguatan akses atau jadwal snapshot yang aktif
dalam context. Biaya/cap/provider invoice, lisensi/retensi/ownership tetap tindak
lanjut; jangan mengarang persetujuan perusahaan. Pilot nyata/peserta/PIC tetap ditunda.

Kandidat evaluasi: `dhi.io/postgres:16.15-alpine3.23` dan
`dhi.io/redis:7.4.11-debian13`. Keduanya belum dipasang/dites kompatibilitas proyek.
Snapshot dipilih sebagai opsi awal, jadwal/retensi belum diputuskan. Redis TTL24jam
masih target; runtime YAML belum menghubungkan Redis sebagai nativecache.
Daftar lanjutan L-01…L-07 dimiliki laporan closeout, bukan roadmap fase baru.

## 7. Prompt chat baru

```text
Baca README, MASTER_CONTEXT.md, architecture/phase-1.md, adr/README.md,
reports/PHASE1_V0_0_1_CLOSEOUT.md dan checkpoint terbaru handover/WORK_LOG.md.
Phase1 v0.0.1 DITUTUP DENGAN CATATAN, APPROVED_OVERRIDE O-10 tanggal18Oktober2026.
Pertahankan dua alias OpenAI, empat sibling repo dan Docker lokal existing4000.
PR main keempat repo merged; bukti fullrun17Oktober:134pytest+13native PASS exit0.
Source main identik candidate; perubahan docs closeout belum otomatis ada di main/tag.
CVE image diterima untuk fase ini; dua kandidat DHI hanya evaluasi mendatang.
Pengguna memilih VM GCP/default/HTTP awal dan keamanan bertahap; deployment belum terbukti.
Snapshot dan biaya dibahas dengan manager; jadwal/retensi/approval perusahaan belum ada.
TTLRedis24jam adalah target, belum diterapkan; jangan ubah cache/auth/budget dari catatan ini.
Pilot nyata/peserta/PIC ditundaO-07. Phase2/3 NOT_STARTED; jangan mulai otomatis.
Kerjakan task yang diminta, verifikasi source/bukti, lalu update pemilik dokumen dan log.
```
