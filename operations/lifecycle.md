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

Alur konseptual: identifikasi pemilik → terbitkan key pengganti dengan scope yang sama
sesuai policy → serahkan aman → verifikasi client → block key lama → verifikasi deny
 dan histori → catat audit. **Drill rotasi lengkap belum tercatat sebagai PASS.**
Rotasi master/provider/salt berbeda dampaknya dan memerlukan rencana terpisah; jangan
mengubah salt tanpa menilai data terenkripsi dan recovery.
