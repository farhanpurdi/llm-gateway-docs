# Runbook operator Phase 1 — H10D

> Jalankan perintah script dari `company-ai-platform/llm-gateway-infra`, bukan dari repo docs.
> Baca [panduan operasional](README.md) dan [status Phase1](../architecture/phase-1.md) sebelum eksekusi.

## Pemeriksaan awal

Dari repo infra: aktifkan PATH Python existing, jalankan `scripts/health/check-all.sh`.
Liveness menunjukkan proses HTTP hidup; readiness, dependency check, catalog check,
dan live inference adalah lapisan berbeda. Catalog check bukan inferensi berbayar.
Jangan menyimpulkan provider sehat hanya dari HTTP 200 `/health/liveliness`.
Endpoint HTTP readiness pernah tetap 200 saat DB/Redis dimatikan; script readiness
kini juga memeriksa kedua dependency secara langsung. Gunakan script ini untuk
monitor lokal; monitoring server harus menyediakan pemeriksaan setara.

## Onboarding

1. Pilih policy di repo config, validasi YAML dan policy. Buat/cek team dengan script
   `scripts/teams/create-team.sh <team-policy-name>` dan `get-team-id.sh`.
2. Jalankan `scripts/onboard-developer.sh <user-id> <team-id> <team-policy-name>`.
3. Output pembuatan key mengandung secret: serahkan lewat jalur privat, jangan tempel
   di tiket/log/report. Developer hanya menerima virtual key, tidak master/provider key.
4. Konfigurasikan OpenCode dengan template repo config. Gunakan `company-fast` atau
   `company-coding`. Verifikasi akses yang diizinkan dan atribusi user/team/spend.
5. Catat pemilik, tujuan, budget dan tanggal review key. Policy team harus disepakati.

## Offboarding multi-key

Hentikan dahulu semua jalur pembuatan key untuk user (operator, integrasi, sesi admin).
Koordinasikan provisioning agar tidak berjalan bersamaan sampai verifikasi selesai.
Helper `LiteLLMClient.offboard_user_keys(user_id)` di repo E2E mengambil snapshot semua
halaman key user, memblokir tiap key, melanjutkan pemblokiran jika ada kegagalan sebagian,
dan mengembalikan error jika hasil tidak lengkap. Gunakan client yang sama; jangan
membuat abstraksi HTTP admin kedua.

Verifikasi akhir: baca ulang semua halaman key user dan pastikan setiap key blocked,
cek key lama ditolak (401/403), dan pastikan spend/histori tetap ada. Jika ada key baru
atau error parsial, offboarding belum selesai: pertahankan freeze dan ulangi setelah
memperbaiki penyebab. Jangan hard-delete record dan jangan blokir team bersama.
Helper ini bukan kontrol HR/SSO dan tidak mencabut kemampuan menerbitkan key baru.
Freeze provisioning adalah kewajiban operasional; belum ada locking otomatis lintas
semua admin/integrasi. H9 E2E menguji user disposable terisolasi, bukan seluruh identitas
karyawan nyata.

## Incident

| Gejala | Tindakan |
|---|---|
| 401/403 pada key developer | Periksa key blocked/expired, kepemilikan user/team, dan akses alias; jangan berikan master key sebagai jalan pintas. |
| 429 | Periksa RPM/budget team/key dan waktu reset; jangan menaikkan limit otomatis. |
| 422budget | Native LiteLLMexisting memakai422 untuk budget habis. Periksa scopekey/member/team dan durasi/reset; jangan menganggap semua budgeterror429. |
| Provider timeout/5xx | Cek health/catalog lalu satu live inference; cek status provider, request ID dan durasi, tanpa merekam secret/prompt sensitif. |
| PostgreSQL mati | Pada drill17Oktober valid warm/cold503; blocked401, negative lain503. Gateway menolak request yang tidak dapat diverifikasi. Periksa disk/logDB, start container existing, tungguPG+gatewayready, lalu periksa deny dan keduaalias/spend. |
| Redis mati | Pada runtimeexisting Redis belum menjadi nativecache; valid tetap200, invalid/blocked401, deny403 dan budget422. Health operasional tetap gagal sampai Redis pulih. Startcontainer existing dan periksa keduanya; jangan mengklaim distributedlimit dari hasil ini. |
| Config release gagal | Baca operation JSON; pastikan recovery passed atau lakukan pemulihan config sesuai runbook release. |
| Secret bocor | Blokir virtual key terdampak, rotasi melalui jalur privat, evaluasi akses/spend, pertahankan audit; provider/master/salt membutuhkan rencana khusus. |
| Disk penuh/backup gagal | Jangan hapus histori untuk mendapat ruang; identifikasi log/arsip yang boleh dipindah sesuai retensi, verifikasi backup baru. |

Akhiri incident setelah dependency, health, smoke dan tes live relevan lulus. Catat
waktu mulai/pulih, penyebab, tindakan, hasil verifikasi, dan penanggung jawab.
`docker logs --since 10m llm-gateway` hanya untuk operator: redaksi sebelum membagikan.

Provider429/500/timeout408 dan retry2(3attempt) diperiksa lewatSDK/router/errorhandler
native terpasang dengan mock tanpa providerIO; HTTPmock berbahaya ditolak400 pada
gateway nyata. Ini simulasi terkontrol, bukan sengaja membanjiri provider untuk
memicu error. [Bukti/cakupan](../reports/phase1-final-evidence/README.md).

## Pilot

Mulai dari kelompok kecil yang disetujui, limit rendah yang cukup untuk pekerjaan,
dan review spend/error harian. Hentikan perluasan pilot jika ada bypass akses,
kehilangan audit, backup tak bisa direstore, atau security gate gagal. Penanggung
jawab server, budget, backup, dan incident harus ditetapkan sebelum menerima pengguna.
