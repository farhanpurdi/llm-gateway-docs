# ADR-005 — OpenCode client pertama

Status: **CONFIRMED**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Gunakan OpenCode sebagai client awal; client tambahan hanya dengan scope yang jelas.

## Alasan dan konsekuensi

Template harus mengikuti versi yang dipakai; adapter parity tidak diasumsikan hanya dari JSON contoh.

## Keadaan aktual dan batas bukti

Template providers/company-ai tersedia; fast smoke teruji. Coding/agent workflow lengkap belum dibuktikan dalam evidence terakhir.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
