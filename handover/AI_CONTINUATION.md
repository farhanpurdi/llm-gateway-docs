# Melanjutkan proyek dengan AI tanpa kehilangan konteks

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
4. Pilih satu task yang diminta user. Usulan `P1-06/F-01` tidak otomatis menjadi instruksi
   memulai coding ketika user sedang meminta dokumentasi.
5. Tunjukkan proposal/risiko sebelum perubahan major; jangan mengarang approval atau
   menyamakan isi ADR berstatus OPEN dengan keputusan final.
6. Gunakan Docker existing4000; tidak membuat staging/environment/container baru. Jangan
   menjalankan raw deployment/outage/provider request hanya karena contoh command tersedia.
7. Pertahankan OpenAI-only, exact dua alias, arsitektur satu client E2E, audit retention,
   dan koordinasi provisioning saat offboarding. Phase2/3 belum dimulai.
8. Catat pekerjaan/hasil aktual, failure, lokasi evidence, perubahan keputusan, commit/PR
   jika ada, dan next exact task di log. Update hanya status fase yang terkait.

## Prompt siap pakai

```text
Baca llm-gateway-docs/README.md lalu MASTER_CONTEXT.md di repo docs tersebut.
Baca architecture/phase-1.md, adr/README.md, dan checkpoint terbaru handover/WORK_LOG.md.
Jangan membaca arsip sebagai current state. Verifikasi source/HEAD/working tree.
H10D lokal selesai bukan Phase1 exit gate. Phase2/3 belum dimulai.
Gunakan Docker existing4000, OpenAI-only, company-fast dan company-coding sesuai mapping.
Jangan buat staging/container baru atau mengubah roadmap/ADR tanpa persetujuan.
Tugas sesi ini: <isi satu task dan hasil yang diminta>.
Jika perlu perubahan major, jelaskan opsi/dampak dahulu sebelum implementasi.
Sesudah bekerja, catat perubahan, tes nyata, risiko, commit jika ada, dan next action.
```

## Saat konteks menyempit / pindah model

Ringkas enam hal: task aktif, keputusan yang mengikat, perubahan sudah dilakukan,
bukti/hasil tes, hal yang belum terverifikasi, next exact action dan status izinnya.
Tautkan file, jangan menyalin seluruh source. Jangan menghapus fakta kegagalan penting.
Jika tidak ada bukti, tandai UNKNOWN/NOT_VERIFIED lalu periksa; jangan menciptakan hasil.
