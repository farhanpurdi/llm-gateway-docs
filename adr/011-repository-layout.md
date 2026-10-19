# ADR-011 — Tiga repo komponen dan repo dokumentasi

Status: **BASELINE + APPROVED_OVERRIDE O-04/O-09**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Pertahankan tiga repo infra/config/e2e. Atas instruksi user terbaru, pusatkan seluruh docs/report/context pada repo llm-gateway-docs existing.

## Alasan dan konsekuensi

Dokumentasi mempunyai satu pemilik dan navigasi; source/runtime tetap di repo komponen. Parent Git/submodule hanya bila diputuskan, bukan syarat pemindahan docs ini.

## Keadaan aktual dan batas bukti

Migrasi dokumentasi diizinkan user dalam percakapan; empat repo sibling, root bukan Git.
Commit migrasi docs `1d07d02` terverifikasi 2026-10-12. Pada 17 Oktober, docs telah
dipublikasikan melalui [draft PR #1](https://github.com/farhanpurdi/llm-gateway-docs/pull/1);
CI dokumentasi pada `5bfd9d9` PASS. Review/merge tetap terpisah.
Tiga file context root sudah tidak ada; sumber awal tetap di `archive/`. Tidak membuat
repo/remote baru. Source komponen telah disimpan pada candidate commit dan draft PR
ke develop; enam validate/security checks pada SHA candidate PASS.

## O-09 — penyiapan promosi ke main, 17 Oktober 2026

Main ketiga komponen hanya initial README dan history-nya terpisah dari develop.
Pengguna menyetujui opsi A pada [proposal promosi](../reports/PHASE1_MAIN_PROMOTION_PROPOSAL.md):
"Setuju, siapkan PR promosi main (disarankan)". Kedua history digabung pada branch
promosi baru melalui `merge --allow-unrelated-histories`; konflik README diselesaikan
dengan mempertahankan panduan candidate. Tree hasil sama persis dengan candidate.
Draft PR ke main: config #4, infra #7, E2E #6; refs dan bukti ada pada proposal.

Ini tidak membentuk parent repository/monorepo atau menulis ulang protected main.
Main belum di-merge; required review/checks tetap berlaku. Sebelum merge, pembatalan
cukup menutup PR promosi. Setelah merge, gunakan revert yang direview. O-09 tidak
mengizinkan force-push, merge protected branch, tag, deploy atau perubahan image.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Review/merge yang dilakukan pengguna

Pengguna kemudian mengonfirmasi telah review/merge; GitHub diverifikasi ulang
18Oktober2026: config#4, infra#7, E2E#6 dan docs#1 merged17Oktober. Main keempat
repo memiliki Git tree sama dengan candidate. Status draft/initial main pada bagian
O-09 di atas adalah riwayat sebelum tindakan pengguna. Tidak perlu mengulang merge
unrelated history untuk melanjutkan proyek. [Refs](../reports/PHASE1_V0_0_1_CLOSEOUT.md).

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
