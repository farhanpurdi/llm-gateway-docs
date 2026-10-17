# Lifecycle user dan virtual key

Panduan ini adalah pintu masuk lifecycle; langkah rinci yang sudah ada dipertahankan
pada [runbook operator: onboarding](incident.md#onboarding) dan
[offboarding multi-key](incident.md#offboarding-multi-key).

## Alur dan pemilik

Operator memilih policy → membuat user/team → menerbitkan virtual key scoped →
menyerahkan key secara privat → memonitor pemakaian → rotate/block bila diperlukan →
menjaga audit. Developer hanya menggunakan virtual key. Corporate SSO belum dibangun.

Script existing ada di repo infra (`users/`, `teams/`, `keys/`, `onboard-developer.sh`).
Helper `offboard_user_keys` berada di **client E2E**; jangan menganggapnya service HR/SSO
atau CLI production dengan locking global. Gunakan arsitektur client existing bila
mengembangkan alur operasional selanjutnya.

## Batas yang wajib dipahami sebelum offboarding

- Hentikan/serialisasikan semua jalur provisioning user target selama proses.
- Temukan seluruh halaman key, block semuanya, tangani kegagalan parsial.
- Baca ulang hasil dan buktikan credential lama ditolak sebelum menyatakan selesai.
- Pertahankan user/key/spend/history; jangan hard-delete atau block team bersama.
- Snapshot key tidak mencegah key baru diterbitkan bersamaan. Pencabutan hak menerbitkan
  key dan disable IdP menyeluruh akan ditangani pada Phase2, bukan klaim H9 sekarang.

## Rotasi

1. Identifikasi pemilik dan hentikan provisioning bersamaan selama cutover.
2. Terbitkan key pengganti untuk user/team sama. Salin izin model, RPM/TPM, budget
   dan durasinya; jangan memperlebar scope. Distribusikan lewat jalur privat.
3. Verifikasi akses model/inference dengan key baru sebelum memblokir key lama.
4. Block key lama, baca ulang statusnya dan buktikan credential lama ditolak401/403.
5. Ulangi inference dengan key baru; periksa kedua record key, user/team dan histori
   spend tetap ada. Counter native dapat terlambat dibanding rowspend; tunggu flush
   dengan batas waktu, jangan menyimpulkan data hilang dari satu pembacaan awal.
6. Catat waktu/pemilik/hasil tanpa rawkey. Jangan hard-delete keylama/audit.

**Drill disposable17Oktober2026 PASS untuk kedua alias:** scope sama, old deny,
new inference200 sebelum/sesudah cutover, kedua key+spend retained. Keycap pengganti
memulai counter baru; budget user/team tetap sama. Ini bukan migrasi/rotasi seluruh
credential developer nyata atau pengganti distribusi credential aman.
[Tes aktual](../../llm-gateway-e2e/tests/test_key_rotation.py) dan
[bukti](../reports/phase1-final-evidence/key-rotation-final.txt).
Rotasi master/provider/salt berbeda dampaknya dan memerlukan rencana terpisah; jangan
mengubah salt tanpa menilai data terenkripsi dan recovery.
