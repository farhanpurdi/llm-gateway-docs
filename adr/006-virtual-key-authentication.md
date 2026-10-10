# ADR-006 — Virtual key dan pemisahan credential

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Developer/workload memakai virtual key scoped; master/provider key hanya sisi operator/server.

## Alasan dan konsekuensi

Atribusi dan revokasi per-user dimungkinkan. Jangan menyimpan secret di docs/Git atau memberikan master key ke browser/client.

## Keadaan aktual dan batas bukti

Pembuatan user dan team, virtual key, pembatasan akses, pencabutan credential serta retensi audit teruji. Freeze provisioning dibutuhkan ketika offboard; SSO belum ada.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
