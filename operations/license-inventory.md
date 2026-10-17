# Inventaris lisensi Phase 1

Diperiksa17Oktober2026. Ini inventaris komponen yang dipakai, bukan persetujuan
pengadaan/perusahaan atau SBOM lengkap seluruh paket image. Pemilik keputusan:
[ADR-017](../adr/017-licensing.md). Tidak ada fitur enterprise baru diaktifkan.

| Komponen existing | Sumber resmi / lisensi | Dampak pada handover |
|---|---|---|
| LiteLLM1.104.0 |[LICENSE pada tag yang sama](https://github.com/BerriAI/litellm/blob/v1.104.0/LICENSE):MIT di luar direktori enterprise; enterprise memiliki ketentuan terpisah |Jangan menyebut seluruh image/semua fitur bebas lisensi enterprise. Native user/team/key/budget/spend yang dipakai dibuktikan berjalan pada runtime existing; SSO/custom control plane tidak diaktifkan |
| PostgreSQL16.15 |[PostgreSQL License](https://www.postgresql.org/about/licence/) |Pertahankan pemberitahuan lisensi pada distribusi; inventaris ini tidak mencakup setiap paketOS/helper dalam image |
| Redis7.4.11 |[LICENSE tag7.4.11](https://github.com/redis/redis/blob/7.4.11/LICENSE.txt) dan [tabel versi resmi](https://redis.io/legal/licenses/):pilihanRSALv2/SSPLv1 |Jangan melabeli7.4 sebagaiBSD3 atau menerapkan opsiAGPLv3 dariRedis8. Pemilihan/penerimaan lisensi perusahaan belum dicatat |
| OpenCode2.0.18 dan dependencies Python |Versi CLI diuji; pin Python ada pada lock masing-masing repo |Review lisensi distribusi CLI dan seluruh dependency transitif tetap diperlukan bila dibundel/didistribusikan; tidak diasumsikan selesai dari tes fungsional |

Keputusan pemilik masihOPEN untuk penggunaan/distribusi yang direncanakan. Penundaan
pilot/PIC padaO-07 tidak mengubah status tersebut. Perubahan versi/image untuk alasan
lisensi harus melalui review kompatibilitas, backup/rollback dan persetujuan dahulu.
