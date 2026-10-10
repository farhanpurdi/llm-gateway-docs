# ADR-014 — Pilihan IdP SSO

Status: **OPEN**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Pilih identity provider sesuai corporate identity pada Phase2 melalui keputusan yang disetujui.

## Alasan dan konsekuensi

SSO disable harus dihubungkan ke revocation seluruh key; login saja tidak menyelesaikan deprovision.

## Keadaan aktual dan batas bukti

Belum dipilih; jangan mengasumsikan Entra/Google atau membangun integrasi pada Phase1.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
