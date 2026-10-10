# ADR-015 — Hosting dan target release

Status: **OPEN; target lokal ditetapkan O-01**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Target kerja saat ini Docker existing4000; jangan staging/container baru. Hosting/domain/server final belum diputuskan dalam bukti.

## Alasan dan konsekuensi

Penghapusan staging lokal tidak menghapus security/release gate. CI hosted tidak dapat mengakses localhost laptop.

## Keadaan aktual dan batas bukti

O-01 membatalkan staging. Workflow live masih menyebut staging; M-01 perlu keputusan target/runner/TLS/network sebelum perubahan.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
