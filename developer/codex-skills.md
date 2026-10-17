# Skill Codex untuk Company AI Platform

Dipasang pada 17 Oktober 2026 (Asia/Jakarta), sesuai permintaan user. Buka workspace
`company-ai-platform` di Codex untuk menggunakan skill lokal dalam `.agents/skills/`.
Skill baru tersedia pada turn berikutnya; jika belum muncul, buka ulang chat atau
restart Codex. Lihat [panduan resmi skill](https://learn.chatgpt.com/docs/build-skills).

## Inventaris

| Skill | Sumber | Kegunaan |
|---|---|---|
| `gateway-acceptance` | Dibuat khusus proyek | Acceptance per-task, onboarding/agent OpenCode, streaming, policy, failure semantics dan evidence |
| `gateway-release-check` | Dibuat khusus proyek | Review candidate lintas repo, CI, kontrak, rollback dan gate pilot/release |
| `gateway-handover` | Dibuat khusus proyek | Konteks kelanjutan, status fase dan work log berbasis bukti |
| `security-threat-model` | Katalog resmi OpenAI | Threat model berbasis source untuk permintaan review ancaman |
| `security-best-practices` | Katalog resmi OpenAI | Review keamanan bahasa/framework yang didukung |
| `gh-fix-ci` | Katalog resmi OpenAI | Diagnosis dan perbaikan GitHub Actions PR checks yang gagal |
| `gh-address-comments` | Katalog resmi OpenAI | Penanganan komentar review pada PR GitHub |

Empat skill resmi disalin dengan installer dari
[openai/skills, direktori curated](https://github.com/openai/skills/tree/main/skills/.curated)
pada ref `main` saat pemasangan; ref itu dapat berubah. Script/referensi pendukung ikut
dipasang. `openai-docs`, `skill-creator`, dan `skill-installer` sudah tersedia dalam
instalasi Codex pada sesi ini dan tidak diduplikasi ke proyek.

## Contoh penggunaan

Pilih skill melalui pemilih skill atau sebut namanya secara eksplisit dalam prompt.

```text
Gunakan $gateway-acceptance untuk menyusun rencana pengujian P1-11/P1-12.

Gunakan $gateway-release-check untuk memeriksa gate Phase 1 yang masih terbuka.

Gunakan $gateway-handover untuk memperbarui handover dari pekerjaan sesi ini.

Gunakan $security-threat-model untuk menilai ancaman gateway sebelum pilot.

Gunakan $security-best-practices untuk mereview keamanan kode Python gateway.

Gunakan $gh-fix-ci untuk mendiagnosis check yang gagal pada PR yang saya berikan.

Gunakan $gh-address-comments untuk merangkum komentar reviewer pada PR yang saya berikan.
```

Skill GitHub memerlukan akses repo/PR dan autentikasi `gh` yang sesuai. Pemasangan
skill tidak menyiapkan autentikasi tersebut atau menjalankan workflow-nya.

Skill khusus membaca master, ADR dan dokumen fase aktif, sehingga nilai model/policy
dan status tidak dibekukan dalam salinan instruksi. Hasil review/laporan tetap berada
di repo docs. Pemasangan skill tidak mengubah status acceptance Phase 1 atau mengizinkan
tes berbayar, deployment maupun perubahan major di luar permintaan user.

## Lokasi dan batas distribusi

Folder skill berada di root workspace yang **bukan repo Git**. Folder itu belum
tercakup commit/push empat repo; salin `.agents/skills/` bersama workspace saat
handover ke mesin lain. Dokumen ini menyimpan inventaris, bukan salinan paket skill.

Jika membuka salah satu repo komponen sebagai proyek terpisah, jangan mengasumsikan
skill pada root workspace ikut ditemukan: discovery repo dapat berhenti di root
Git komponen. Gunakan workspace `company-ai-platform` untuk konfigurasi ini.

Validasi struktur skill memakai `quick_validate.py` bawaan `skill-creator`.
Validasi ini memeriksa format instruksi dan metadata, bukan bukti runtime gateway
atau bukti bahwa semua workflow skill telah dijalankan.
