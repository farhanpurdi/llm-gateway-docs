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
pada saat pemindahan docs. Klaim umum `OpenCode tool calling` perlu dibaca bersama
[bukti Phase1 yang tersedia](../architecture/phase-1.md): fast basic response dan API
forced tool calls terbukti; acceptance full coding agent kedua alias belum lengkap.
Versi yang benar-benar dipakai pada release berikutnya harus dicatat bersama source refs,
image digest, hasil tes dan batas adapter; jangan otomatis upgrade ke versi terbaru.
