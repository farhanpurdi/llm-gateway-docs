# ADR-015 — Hosting dan target release

Status: **APPROVED_OVERRIDE O-10 untuk arah VM GCP/keamanan bertahap; implementasi server NOT_VERIFIED**. Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md). Dievaluasi 2026-10-10; penulisan file individual
bukan persetujuan baru atau klaim fitur selesai.

## Keputusan / arah awal

Target kerja lokal tetap Docker existing4000. Pada18Oktober2026, O-10 memilih
VM GCP/default/HTTP awal sebagai arah deploy, dengan keamanan bertahap setelah
pengamatan trafik dan diskusi manager. Domain dan konfigurasi VM aktual belum dicatat.

## Alasan dan konsekuensi

Penghapusan staging lokal tidak menghapus security/release gate. CI hosted tidak dapat mengakses localhost laptop.

## Keadaan aktual dan batas bukti

O-01 membatalkan staging. Pada17Oktober2026 user memilih opsiA(O-08):hosted GitHubCI
offline tetap, workflow live staging dihapus, full live manual diDockerexisting4000
dengan bukti sourceSHA/hash/image/output/exit/cleanup dan review. [Prosedur](../operations/local-release-gate.md).
Tidak ada self-hostedrunner, secretsGitHub atau environment baru. CandidateCI/review
tetap harus sesuai source. Pada checkpoint17Oktober, target server/TLS/network/admin
boundary masih OPEN; keputusan arah VM dan penundaan18Oktober dicatat pada O-10 di bawah.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## O-10 — arah server dan penutupan dengan catatan

Pengguna memilih setup VM GCP apa adanya/default terlebih dahulu, mengamati trafik,
lalu menentukan HTTP/HTTPS, firewall dan pembatasan admin bertahap. Phase1 v0.0.1
ditutup atas pengecualian ini; source lokal teruji bukan bukti VM aman/berjalan.
HTTP melalui internet belum mengenkripsi key/prompt/source/response.

Snapshot VM GCP dipilih sebagai opsi backup paling mudah untuk dibahas dengan
manager. Jadwal, retensi, disk, akses dan uji restore belum diputuskan/dikerjakan.
Proposal backup harian dalam runbook tetap usulan, bukan job yang sudah aktif.
[Closeout dan tindak lanjut](../reports/PHASE1_V0_0_1_CLOSEOUT.md).
Pekerjaan dokumentasi ini tidak deploy VM, membuat container, mengubah firewall,
memasang proxy/TLS atau menambah runner/secrets GitHub.

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
