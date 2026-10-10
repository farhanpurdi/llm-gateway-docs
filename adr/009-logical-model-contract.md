# ADR-009 — Alias sebagai kontrak client

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Client hanya bergantung pada company-fast/company-coding; identitas file models berasal dari filename.

## Alasan dan konsekuensi

Katalog deskriptif dan runtime YAML harus konsisten; perubahan alias/backend melalui ADR dan uji regresi.

## Keadaan aktual dan batas bukti

Runtime benar; F-01/F-02 pada exact alias/upstream/cross-catalog validation belum diperbaiki.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
