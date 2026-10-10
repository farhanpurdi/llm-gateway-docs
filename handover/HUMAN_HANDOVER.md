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

Usulan teknis tetap **P1-06/F-01**, menutup gap validator exact alias/provider/upstream.
Tidak perlu rewrite arsitektur berdasarkan bukti sekarang. M-01/M-02/M-04/M-05 perlu
keputusan owner sebelum perubahan besar. M-03 penempatan docs telah dipilih user:
repo docs existing; migrasi masih perlu commit/review/push, tanpa membuat parent repo.
