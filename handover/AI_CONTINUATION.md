# Melanjutkan proyek dengan AI tanpa kehilangan konteks

**Posisi18Oktober2026:** Phase1 v0.0.1 DITUTUP DENGAN CATATAN, APPROVED_OVERRIDE
O-10. Baca [closeout tujuh feedback](../reports/PHASE1_V0_0_1_CLOSEOUT.md) sebelum
menafsirkan status gate dalam laporan lama. [Panduan pengguna](../developer/panduan-penggunaan.md)
adalah pintu masuk operator/developer. Phase2/3 belum dimulai.

## Paket konteks minimum

Baca berurutan: [README](../README.md) → [master](../MASTER_CONTEXT.md) →
[fase aktif](../architecture/phase-1.md) → [register ADR/drift](../adr/README.md) →
[checkpoint log terbaru](WORK_LOG.md). Setelah memilih task, baca source/runbook/bukti
hanya yang terkait. Jangan memuat lampiran kode atau seluruh arsip pada awal sesi.

## Protokol kerja

1. Nyatakan phase/task ID, hasil sebelumnya yang dipakai dan batas scope yang disetujui.
2. Periksa HEAD, working tree dan source aktual. HEAD lama tidak mencakup file dirty/untracked.
3. Bedakan target desain, implementasi aktual, bukti tes, dan rekomendasi. Gunakan enum status
   pada master; `LOCAL_VERIFIED` bukan `DONE_VERIFIED` release.
4. Pilih task/paket yang diminta user dan cocokkan dengan checkpoint terbaru.
   Next task pada handoff tidak otomatis menjadi instruksi coding ketika user meminta dokumentasi.
5. Tunjukkan proposal/risiko sebelum perubahan major; jangan mengarang approval atau
   menyamakan isi ADR berstatus OPEN dengan keputusan final.
6. Gunakan Docker existing4000; tidak membuat staging/environment/container baru. Jangan
   menjalankan raw deployment/outage/provider request hanya karena contoh command tersedia.
7. Pertahankan OpenAI-only, exact dua alias, arsitektur satu client E2E, audit retention,
   dan koordinasi provisioning saat offboarding. Policy pilot final mengikuti
   `pilot.yaml` sesuai [ADR-016/O-06](../adr/016-pilot-limits.md) untuk pengerjaan/tes
   final pilot: kedua alias, team US$10, anggota US$2, RPM30/TPM100000; script team
   existing30d. P1-09 memperbaiki durasi anggota; reset awal bulan UTC dan scheduler
   sekitar10menit terverifikasi. Batasi jumlah request/token tes; gate release masih OPEN.
   Phase2/3 belum dimulai.
8. Catat pekerjaan/hasil aktual, failure, lokasi evidence, perubahan keputusan, commit/PR
   jika ada, dan next exact task di log. Update hanya status fase yang terkait.

## Prompt siap pakai

```text
Baca README.md, MASTER_CONTEXT.md, architecture/phase-1.md, adr/README.md,
reports/PHASE1_V0_0_1_CLOSEOUT.md dan checkpoint terbaru handover/WORK_LOG.md.
Phase1 v0.0.1 DITUTUP DENGAN CATATAN, APPROVED_OVERRIDE O-10 tanggal18Oktober2026.
Pertahankan dua alias OpenAI sesuai mapping, empat sibling repo dan Docker lokal existing4000.
PR main config#4/infra#7/E2E#6/docs#1 merged; source tree sama dengan candidate teruji.
Bukti17Oktober:97unit/5smoke/30live/2outage+13native PASS exit0; config63/infra31 offlinePASS.
CVE image diterima untuk fase ini; kandidat DHI hanya untuk evaluasi masa depan:
dhi.io/postgres:16.15-alpine3.23 dan dhi.io/redis:7.4.11-debian13.
Pengguna memilih VM GCP/default/HTTP awal dan keamanan bertahap; deploy belum diverifikasi.
Snapshot/backup dan biaya dibahas manager; jangan mengarang jadwal atau approval perusahaan.
TTLRedis24jam adalah target, belum diterapkan. YAML runtime belum mengaktifkan nativecache.
Belum ada pembatasan pengguna Redis tambahan yang diputuskan; jangan membuka port Redis.
Pilot nyata/peserta/PIC ditundaO-07. Phase2/3 NOT_STARTED, jangan mulai otomatis.
Nama versi v0.0.1 dipilih; tag belum dibuat. Docs closeout dipublikasikan pada branch
docs/phase1-v0.0.1-closeout-20261018; periksa status merge/CI terbaru pada PR-nya.
Tugas sesi ini: <task yang diminta pengguna dan hasil yang diperlukan>.
Gunakan developer/panduan-penggunaan.md untuk alur operator/developer.
Bedakan keputusan/implementasi/bukti. Jangan jalankan live/outage dari tugas dokumentasi.
Jangan menanyakan ulang persetujuan yang sudah ada; scope major baru dijelaskan dahulu.
Sesudah bekerja, catat perubahan/tes aktual pada dokumen pemilik dan log.
```

## Saat konteks menyempit / pindah model

Ringkas enam hal: task aktif, keputusan yang mengikat, perubahan sudah dilakukan,
bukti/hasil tes, hal yang belum terverifikasi, next exact action dan status izinnya.
Tautkan file, jangan menyalin seluruh source. Jangan menghapus fakta kegagalan penting.
Jika tidak ada bukti, tandai UNKNOWN/NOT_VERIFIED lalu periksa; jangan menciptakan hasil.
