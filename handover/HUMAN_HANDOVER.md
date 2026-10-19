# Checklist handover ke engineer atau operator baru

**Status18Oktober2026:** pengguna menutup Phase1 dengan catatan untuk v0.0.1,
APPROVED_OVERRIDE O-10. [Tujuh feedback/catatan lanjutan](../reports/PHASE1_V0_0_1_CLOSEOUT.md)
dan [panduan penggunaan sederhana](../developer/panduan-penggunaan.md) menjadi acuan.
Deployment GCP, snapshot, TTL dan kontrol keamanan yang belum dibuktikan tetap
NOT_VERIFIED. Checklist penyerahan akses di bawah tidak otomatis tercentang dari sign-off fase.

## Pahami proyek dalam 15 menit

1. [Overview](../architecture/overview.md): tujuan, alur request dan pembagian fase.
2. [Master](../MASTER_CONTEXT.md): keputusan tetap, environment dan batasan.
3. [Phase1](../architecture/phase-1.md): apa yang teruji dan apa yang belum selesai.
4. [Register keputusan](../adr/README.md): opsi major yang belum boleh diimplementasikan.
5. [Log terbaru](WORK_LOG.md) dan [reports](../reports/README.md): asal klaim progres.

## Serah-terima akses dan kepemilikan

| Peran yang harus ditentukan | Tanggung jawab | Status nama/PIC |
|---|---|---|
| Pemilik project | Scope, prioritas, penerimaan fase | Pengguna menyetujui penutupan O-10; nama/PIC formal belum ditulis |
| Platform/operator | Runtime, release, backup dan incident | Belum dicatat |
| Security/data owner | Secret, paparan akses, CVE, privacy/retention | Belum dicatat |
| Billing owner | OpenAI project/billing, limit/cap/alert dan pilot budget | Belum dicatat |
| Reviewer/repo owner | PR, merge gate, refs/tag dan publikasi docs | Review/merge pengguna terverifikasi; PIC formal dan publikasi tag belum dicatat |

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

## Melanjutkan setelah penutupan

Phase1 v0.0.1 ditutup melalui O-10; jangan mengulang rencana sebelum PR main merged.
Bukti teknis terakhir:134pytest+13native PASS exit0, config63/infra31 offline PASS,
restore83tabel, rotasi key, config-only rollback dan audit privasi/cleanup PASS.
[Panduan penggunaan](../developer/panduan-penggunaan.md) memisahkan tugas operator
(onboarding/health/pemakaian) dari developer (key/OpenCode/model/error).

Pengguna akan setup VM GCP/default/HTTP awal dan mengamati trafik sebelum memilih
keamanan bersama manager. Snapshot backup dan biaya juga dibahas manager; tidak
mengaku sudah ada jadwal snapshot atau persetujuan biaya perusahaan. Target TTLRedis
24jam belum diterapkan dan scope key belum ditentukan; tidak mengubah expiry key,
reset budget atau retensi PostgreSQL. Dua kandidat DHI belum diuji pada proyek.

[L-01…L-07](../reports/PHASE1_V0_0_1_CLOSEOUT.md) mencatat tindak lanjut operasional.
Pilot nyata/peserta/PIC tetap ditundaO-07. Tag v0.0.1 belum dibuat. Pembaruan docs
closeout dipublikasikan pada branch `docs/phase1-v0.0.1-closeout-20261018` atas instruksi
push19Oktober; status merge/CI mengikuti PR terbaru. Phase2/3 belum dimulai;
minta task konkret sebelum implementasi/deploy, tanpa meminta ulang keputusan fase.
