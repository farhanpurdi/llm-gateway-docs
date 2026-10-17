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
Baca llm-gateway-docs/README.md lalu MASTER_CONTEXT.md di repo docs tersebut.
Baca architecture/phase-1.md, adr/README.md, dan checkpoint terbaru handover/WORK_LOG.md.
Jangan membaca arsip sebagai current state. Verifikasi source/HEAD/working tree.
H10D lokal selesai bukan Phase1 exit gate. Phase2/3 belum dimulai.
Gunakan Docker existing4000, OpenAI-only, company-fast dan company-coding sesuai mapping.
Pengerjaan/tes final pilot memakai pilot.yaml sesuai O-06/ADR-016; pilot memakai kedua alias.
P1-09/P1-10 LOCAL_VERIFIED13Oktober; P1-11/P1-12 LOCAL_VERIFIED17Oktober.
Agent kedua alias membaca/mengedit kode, menjalankan verifier dan menggunakan receipt hasil tool;
SSE/API tools kedua alias PASS.79unit/5smoke/6live terfokus, bukan seluruh suite/candidate.
Task aktifP1-FINAL: user meminta sampai akhir dan full cross-check/test; lanjut dari checkpointP1-FINAL,
bukan mengulang pekerjaan dariP1-13. Native13, HTTPguard6, outage2, rotasikey2 dan configrollbackPASS.
CI lokalconfig63/infra31/E2E97unitPASS; fullrun97unit/5smoke/30live/2outage+13nativePASS,exit0.
Baca reports/PHASE1_FINAL_CROSSCHECK_REPORT.md dan WORK_LOG untuk hasil/proses terbaru.
Pilot nyata/peserta/PIC ditundaO-07, bukan pilotPASS atau waiver gate teknis/server/CVE.
O-08 menyetujui hostedoffline + live manual4000; workflowstaging dihapus.
Tiga draftPRcandidate kedevelop ada; CI/review/docsPR dituntaskan. Main3komponen unrelated;
jangan merge/forcepushmain tanpa keputusan reports/PHASE1_MAIN_PROMOTION_PROPOSAL.md.
Jangan outage dari tugas dokumentasi atau menjalankan gatewaytests paralel.
Reset30d ke awal bulan UTC; scheduler sekitar10menit. Batasi jumlah request/token tes.
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
