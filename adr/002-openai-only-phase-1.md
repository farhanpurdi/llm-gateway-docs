# ADR-002 — OpenAI saja pada Phase1

Status: **CONFIRMED**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Phase1 hanya memakai OpenAI API; tidak ada provider lain atau cross-provider fallback.

## Alasan dan konsekuensi

Batas scope dan data handling tetap jelas. Desain multi-provider-ready tidak sama dengan izin mengaktifkan vendor baru.

## Keadaan aktual dan batas bukti

Runtime sesuai. Validator masih menerima wrong provider/upstream pada salinan tes; F-01 tetap terbuka.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
