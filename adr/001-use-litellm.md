# ADR-001 — LiteLLM sebagai Data Plane

Status: **CONFIRMED**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Gunakan LiteLLM Proxy sebagai endpoint OpenAI-compatible dan penegak routing/access/budget runtime.

## Alasan dan konsekuensi

Menghindari membangun inference gateway ulang. Custom Control Plane kelak mengatur administrasi melalui API, bukan memproksi inference ulang.

## Keadaan aktual dan batas bukti

LiteLLM existing1.104.0; fitur lokal diuji. HA dan seluruh failure semantics belum terbukti.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
