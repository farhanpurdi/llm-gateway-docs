# Compatibility Matrix

Last verified: 2026-10-02

| Component | Tested Version |
|---|---|
| LiteLLM | 1.104.0 |
| PostgreSQL | 16.15 |
| Redis | 7.4.11 |
| OpenCode | 2.0.18 |
| Python | 3.12.15 |
| Docker | 29.7.2 |
| Docker Compose | 5.3.1 |

## Verified capabilities

- LiteLLM startup
- PostgreSQL persistence
- Redis connectivity
- company-fast inference
- company-coding inference
- streaming
- virtual keys
- user/team policy
- dynamic team model policy
- spend attribution
- policy-driven provisioning
- OpenCode integration
- OpenCode tool calling

## Cara membaca matriks historis ini

Tanggal di atas adalah catatan kompatibilitas sebelumnya, bukan hasil pengujian baru
pada saat pemindahan docs. Klaim umum `OpenCode tool calling` pada snapshot lama
belum merinci workflow agent; baca [status Phase1 aktif](../architecture/phase-1.md)
dan verifikasi tambahan di bawah untuk bukti yang lebih baru.
Versi yang benar-benar dipakai pada release berikutnya harus dicatat bersama source refs,
image digest, hasil tes dan batas adapter; jangan otomatis upgrade ke versi terbaru.

## Verifikasi tambahan 2026-10-17

OpenCode existing **2.0.18** dan LiteLLM existing **1.104.0** kini juga terbukti untuk
onboarding operator/policy pilot, agent read→edit→shell→hasil tool kedua alias, dan
API streaming/tool calling kedua alias. Enam tes live terfokus dan lima smoke PASS;
[laporan dan batas](../reports/P1_11_P1_12_OPENCODE_REPORT.md).
Tidak mengubah versi, template bersama, adapter atau mapping model.
