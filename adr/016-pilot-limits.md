# ADR-016 — Budget, rate limits dan peserta pilot

Status: **PARTIAL — policy CONFIRMED, enforcement/accounting LOCAL_VERIFIED; peserta/PIC/provider cap masih OPEN**.
Pada17Oktober, O-07 mengizinkan menunda pilot nyata dan penentuan peserta/PIC yang
ditanyakan agar pengujian teknis diteruskan. Item tersebut **ditunda sementara**,
bukan diverifikasi atau diisi dengan identitas fixture. Policy O-06 tetap berlaku.
Sumber: [baseline awal §2](../archive/PROJECT_MASTER_CONTEXT.md#2-architecture-decision-registry),
[register konsolidasi](README.md), serta koreksi user 2026-10-13 untuk memakai
`pilot.yaml` yang sudah disediakan bagi pengerjaan dan pengetesan final pilot (O-06).
Pilihan `default.yaml` sebelumnya (O-05) telah digantikan; bukan acuan pilot aktif.

## Keputusan / arah awal

Nilai limit/budget/jumlah user pilot ditetapkan pemilik project/billing berdasarkan kebutuhan dan penggunaan.

## Keputusan user — 2026-10-13

Policy pengerjaan dan pengujian final pilot memakai
[policies/teams/pilot.yaml](../../llm-gateway-config/policies/teams/pilot.yaml).
Nilai berikut dibaca dari source saat keputusan dicatat; file policy tidak diubah.

| Setting | Nilai yang disetujui | Cakupan pada source existing |
|---|---|---|
| Model yang boleh dipakai | `company-fast`, `company-coding` | Kedua alias tersedia untuk pengerjaan dan pengujian final pilot |
| Budget team | US$10 | `limits.team.monthly_budget_usd` → `max_budget` |
| Budget anggota | US$2 | `limits.member.monthly_budget_usd` → `max_budget_in_team`; bukan budget per key |
| Request team per menit | 30 RPM | `limits.team.rpm` → `rpm_limit` |
| Token team per menit | 100.000 TPM | `limits.team.tpm` → `tpm_limit` |
| Durasi budget team dan anggota | `30d` | Pada LiteLLM1.104.0 existing: awal bulan berikutnya, pukul 00:00 UTC |

Snapshot bagian policy yang disetujui:

```yaml
name: pilot
models:
  - company-fast
  - company-coding
limits:
  team:
    monthly_budget_usd: 10
    rpm: 30
    tpm: 100000
  member:
    monthly_budget_usd: 2
```

[create-team.sh](../../llm-gateway-infra/scripts/teams/create-team.sh) mengirim durasi
team `30d`. [add-member.sh](../../llm-gateway-infra/scripts/teams/add-member.sh) kini juga
mengirim `budget_duration: "30d"`; bug durasi anggota null direproduksi dan diperbaiki
pada P1-09. Tes kalender/persistence, shared limits, interaksi key/member/team dan
reset otomatis telah PASS. Scheduler existing memeriksa reset setiap 597–605 detik;
expiry/reset tidak harus terjadi persis saat boundary. Pemilihan policy
pilot tidak mengubah kontrak runtime Phase 1 yang tetap mempunyai dua alias.

## Alasan dan konsekuensi

Nilai `pilot.yaml` merupakan keputusan eksplisit user untuk pengerjaan dan pengujian
final pilot. Angka budget/RPM/TPM sama dengan pilihan sebelumnya; akses model sekarang
mencakup kedua alias. Tiny fixture budget tetap hanya untuk tes. PIC/billing corporate,
cap/alert provider dan peserta pilot belum ditetapkan oleh keputusan ini.
Siapkan skenario tes dengan jumlah request dan `max_tokens` terbatas sesuai policy
pilot; budget adalah batas penggunaan, bukan target yang harus dihabiskan.

## Keadaan aktual dan batas bukti

P1-09/P1-10: persistence policy, shared RPM/TPM/recovery, budget key/member/team,
reset anggota dengan cumulative spend retained dan rekonsiliasi token/biaya kedua
alias **LOCAL_VERIFIED**, 11 live +4 smoke PASS. [Laporan/kode/batas](../reports/P1_09_P1_10_LIMITS_COST_REPORT.md).
Biaya dibandingkan dengan token respons provider dan harga standar resmi, bukan invoice
billing; peserta pilot2–5/cap provider/PIC tetap belum ditetapkan. YAML merupakan input
provisioning; seluruh identitas tes diblokir, team/anggota lama tidak dimigrasikan.
Anggota existing dengan durasi null perlu ditentukan targetnya sebelum update terarah.

Lihat [Phase1](../architecture/phase-1.md) untuk acceptance/test dan
[work log](../handover/WORK_LOG.md) untuk perubahan terbaru.

## O-10 — keputusan biaya setelah penutupan

18Oktober2026: pengguna menutup Phase1 v0.0.1 dengan catatan dan akan membahas biaya
dengan manager. Policy pilot O-06 tetap sama. Belum ada keputusan cap/alert provider,
budget perusahaan atau rekonsiliasi invoice; hasil accounting lokal tetap dibedakan
dari persetujuan billing perusahaan. Pilot nyata/peserta/PIC tetap ditunda O-07.
[Catatan penutupan](../reports/PHASE1_V0_0_1_CLOSEOUT.md).

## Aturan perubahan

Catat alasan, opsi, security/cost, kompatibilitas, migrasi/rollback, pengujian,
pemilik/tanggal persetujuan dan PR/commit. Jika belum disetujui, tulis PROPOSED;
jangan menimpa keputusan lama atau menganggap contoh implementasi sebagai approval.
