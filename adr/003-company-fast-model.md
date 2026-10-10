# ADR-003 — Mapping company-fast

Status: **CONFIRMED**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

company-fast memetakan ke openai/gpt-5.6-terra.

## Alasan dan konsekuensi

Client memakai alias; perubahan backend memerlukan persetujuan dan tes kompatibilitas, biaya serta data policy.

## Keadaan aktual dan batas bukti

Inference/streaming API dan tool calling fast teruji; jangan melakukan silent substitution saat permission gagal.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
