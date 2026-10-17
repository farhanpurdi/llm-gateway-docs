# Evidence P1-06/F-01/F-02 — 2026-10-12

Bukti pengujian offline sesi implementasi, berbeda dari evidence H1–H10 tanggal
10 Oktober. Baca [laporan](../P1_06_MODEL_CONTRACT_REPORT.md) untuk hasil dan batas
klaim; [kode snapshot](../P1_06_CODE_APPENDIX.md) untuk source saat tes.

- [Config validation](config-validation.txt): 7 tahap, 63 tes.
- [Infra validation](infra-validation.txt): 7 tahap, 22 tes.
- [E2E validation](e2e-validation.txt): 8 tahap, 29 unit; 15 smoke/live deselected.
- [Contract matrix](contract-matrix.json): kedua CLI dan guard release runtime.
- [Scope verification](scope-verification.json): perubahan source dalam scope;
  asset config dan source lain dibandingkan hash sebelum sesi.
- [Docs validation](docs-validation.txt): tautan/roadmap/ADR, integritas evidence lama.

Matrix memakai salinan sementara. Tidak ada secret nyata, dump atau prompt sensitif.
Raw log adalah output aktual; tanggal sesi memakai Asia/Jakarta.
