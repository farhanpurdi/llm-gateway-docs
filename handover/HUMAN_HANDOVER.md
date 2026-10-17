# Checklist handover ke engineer atau operator baru

## Pahami proyek dalam 15 menit

1. [Overview](../architecture/overview.md): tujuan, alur request dan pembagian fase.
2. [Master](../MASTER_CONTEXT.md): keputusan tetap, environment dan batasan.
3. [Phase1](../architecture/phase-1.md): apa yang teruji dan apa yang belum selesai.
4. [Register keputusan](../adr/README.md): opsi major yang belum boleh diimplementasikan.
5. [Log terbaru](WORK_LOG.md) dan [reports](../reports/README.md): asal klaim progres.

## Serah-terima akses dan kepemilikan

| Peran yang harus ditentukan | Tanggung jawab | Status nama/PIC |
|---|---|---|
| Pemilik project | Scope, prioritas, penerimaan fase | Belum dicatat di context |
| Platform/operator | Runtime, release, backup dan incident | Belum dicatat |
| Security/data owner | Secret, paparan akses, CVE, privacy/retention | Belum dicatat |
| Billing owner | OpenAI project/billing, limit/cap/alert dan pilot budget | Belum dicatat |
| Reviewer/repo owner | PR, merge gate, refs/tag dan publikasi docs | Belum dicatat |

Jangan mengisi nama atau budget berdasarkan tebakan. Serahkan akses repository/provider/
server melalui jalur aman; jangan mencantumkan key, `.env`, salt atau dump pada dokumen ini.
Pada 2026-10-13, user mengoreksi acuan pengerjaan/tes final pilot ke `pilot.yaml`: kedua alias,
team US$10, anggota US$2, RPM30/TPM100000. Script team/anggota kini memakai `30d`;
reset awal bulan UTC dan scheduler sekitar10menit terverifikasi pada LiteLLM1.104.0.
[ADR-016](../adr/016-pilot-limits.md) mencatat keputusan;
nama PIC dan cap provider tetap belum ditentukan. Skenario tes dibatasi sesuai policy.

## Yang harus tersedia sebelum engineer lama melepas tugas

- [ ] Empat repo ada dalam layout sibling sesuai [README](../README.md); source refs/dirty
  state dicatat. Jangan mengira HEAD lama sudah memuat perubahan terbaru.
- [ ] Dokumen, source perubahan, PR/commit dan evidence dapat diakses reviewer yang tepat.
- [ ] Operator mengetahui config aktif, port4000, tiga container existing dan keterbatasannya.
- [ ] Secret dan pasangan backup/salt diserahkan secara privat, dengan akses minimum.
- [ ] Runbook [deployment](../operations/deployment.md), [backup](../operations/backup.md),
  [incident](../operations/incident.md), [rollback](../operations/rollback.md) dipahami.
- [ ] Gap limits/cost/provider failures/OpenCode agent dan CVE tersisa tidak disamarkan.
- [ ] Freeze provisioning/offboarding dipahami; shared team tidak diblokir untuk satu user.
- [ ] Next task, pemilik, scope dan status persetujuan ditulis jelas dalam log.

Daftar ini adalah checklist handover; kotak kosong bukan bukti sudah dilaksanakan.
Pengujian ulang dipilih sesuai perubahan dan otorisasi. Simulasi outage, restore dan live
inference punya dampak/biaya; jangan dijalankan serentak hanya untuk membaca dokumentasi.

## Rekomendasi tugas berikutnya

P1-06/F-01/F-02 sudah LOCAL_VERIFIED static/offline pada 2026-10-12;
[laporan dan kode](../reports/P1_06_MODEL_CONTRACT_REPORT.md). P1-09/P1-10 juga kini
LOCAL_VERIFIED: 147 offline,4 smoke,11 live PASS; [laporan/kode terbaru](../reports/P1_09_P1_10_LIMITS_COST_REPORT.md).
P1-11/P1-12 kini LOCAL_VERIFIED17Oktober: onboarding operator asli, agent kedua alias
read/edit/shell/hasil tool, kode terverifikasi dan SSE/API tools PASS.
[79unit/5smoke/6live terfokus dan kode](../reports/P1_11_P1_12_OPENCODE_REPORT.md).
**Task aktifP1-FINAL:** user meminta sampai akhir dan full cross-check/test. Native
error/retry13kasus, HTTPguard6, outagePG/Redis2, rotasikey2 dan configrollbackPASS;
CI lokalconfig63/infra31/E2E97unitPASS; fullrun97unit/5smoke/30live/2outage+13nativePASS,exit0.
O-08 hostedoffline + live manual4000 diterapkan;3draftPRcandidate kedevelop tersedia.
[laporan aktif](../reports/PHASE1_FINAL_CROSSCHECK_REPORT.md) dan checkpointlog menjadi
acuan melanjutkan. Pilot nyata/peserta/PIC ditundaO-07, bukan pilotPASS.
TargetCI/CVE/server mengikuti [proposal keputusan](../reports/PHASE1_RELEASE_DECISIONS.md).
Anggota lama belum dimigrasikan dan billing invoice/cap provider
tetap tersisa. M-01/M-02/M-04 dan bagian lain M-05 perlu keputusan owner sebelum
perubahan besar. M-03 penempatan docs telah dipilih user:
repo docs existing; commit migrasi lokal `1d07d02` terverifikasi 2026-10-12, publikasi/review
remote belum diperiksa. Source komponen masih perlu dicakup commit/review final.
Urutan pekerjaan lengkap ada pada [rencana penutupan Phase 1](../architecture/phase-1-completion-plan.md).
