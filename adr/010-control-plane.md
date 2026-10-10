# ADR-010 — Pisahkan Control Plane

Status: **BASELINE**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Custom backend/UI administrasi baru Phase2, terpisah dari LiteLLM Data Plane.

## Alasan dan konsekuensi

Native API/script cukup untuk P1. Jangan membuat custom billing/auth/portal tanpa kebutuhan yang disepakati.

## Keadaan aktual dan batas bukti

Belum ada llm-control-plane/llm-admin-portal. Helper E2E bukan service control plane atau SSO deprovision.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
