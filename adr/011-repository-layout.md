# ADR-011 — Tiga repo komponen dan repo dokumentasi

Status: **BASELINE + APPROVED_OVERRIDE O-04**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Pertahankan tiga repo infra/config/e2e. Atas instruksi user terbaru, pusatkan seluruh docs/report/context pada repo llm-gateway-docs existing.

## Alasan dan konsekuensi

Dokumentasi mempunyai satu pemilik dan navigasi; source/runtime tetap di repo komponen. Parent Git/submodule hanya bila diputuskan, bukan syarat pemindahan docs ini.

## Keadaan aktual dan batas bukti

Migrasi dokumentasi lokal diizinkan user dalam percakapan; empat repo sibling, root bukan Git. Tidak membuat repo/remote baru; commit/review/push migrasi belum dilakukan.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
