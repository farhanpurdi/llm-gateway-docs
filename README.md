# Company AI Platform — pusat dokumentasi LLM Gateway

**Mulai di sini untuk handover ke manusia atau AI.** Repository ini menjelaskan tujuan,
rancangan, pekerjaan yang sudah terbukti, batasan, dan langkah yang belum dikerjakan.
Tidak berisi secret, database backup, atau deployment environment.

## Apa yang dibangun?

Satu pintu akses AI untuk developer perusahaan. Developer menggunakan **OpenCode** dan
virtual key miliknya; **LiteLLM** mengatur akses model, batas pemakaian dan pencatatan
biaya, lalu meneruskan request ke **OpenAI**. Provider key tetap di server.

Manfaat yang dituju: akses bisa dicabut per pengguna, biaya bisa ditelusuri, dan tools
client memakai nama model perusahaan yang stabil. Backend administrasi dan portal
custom baru direncanakan pada Phase2; keandalan enterprise dikembangkan pada Phase3.

**Posisi sekarang:** fungsi Phase1 teruji lokal sampai H10D, tetapi seluruh acceptance
Phase1, pilot, release dan sign-off **belum selesai**. Phase2/3 belum dimulai.
Constraint user tetap: **Docker existing port4000; jangan membuat staging/container baru.**

## Jalur baca sesuai kebutuhan

| Pembaca | Urutan yang disarankan |
|---|---|
| Orang baru / pemilik project | [Overview](architecture/overview.md) → [master](MASTER_CONTEXT.md) → [Phase1](architecture/phase-1.md) |
| AI yang melanjutkan pekerjaan | [Master](MASTER_CONTEXT.md) → [Phase1](architecture/phase-1.md) → [keputusan/drift](adr/README.md) → [log](handover/WORK_LOG.md) → [protokol AI](handover/AI_CONTINUATION.md) |
| Developer pengguna gateway | [Model catalog](developer/model-catalog.md) → [OpenCode](developer/opencode.md) → [API](developer/api.md) |
| Operator | [Panduan operasi](operations/README.md) → [deployment](operations/deployment.md) / [backup](operations/backup.md) / [incident](operations/incident.md) / [rollback](operations/rollback.md) |
| Engineer pengganti | [Checklist handover](handover/HUMAN_HANDOVER.md) → source terkait → bukti pada [reports](reports/README.md) |
| Reviewer arsitektur | [Indeks ADR](adr/INDEX.md) → [drift/open decisions](adr/README.md) → dokumen fase yang relevan |

Jangan membaca seluruh arsip/kode laporan sekaligus. Baca bagian inti di atas, kemudian
ikuti tautan item tugas aktif. Ini mengurangi kehilangan konteks di dokumen panjang.

## Struktur dan pemilik informasi

```text
llm-gateway-docs/
├── README.md                  # navigasi untuk manusia dan AI
├── MASTER_CONTEXT.md          # aturan/posisi lintas fase, satu master aktif
├── architecture/              # overview + roadmap/status Phase1–3
├── adr/                       # ADR001–017 + drift/override/keputusan terbuka
├── operations/                # deployment, rollback, backup, incident, lifecycle
├── developer/                 # OpenCode, API, model catalog, compatibility
├── handover/                  # log, protokol AI, checklist manusia
├── reports/                   # hasil milestone, kode snapshot dan evidence historis
├── archive/                   # rancangan awal dan handoff panjang
└── scripts/validate-docs.py    # validasi tautan, struktur dan integritas migrasi
```

- Rancangan/kontrak: master + ADR. Status acceptance: file fase terkait.
- Keputusan major belum disetujui: register ADR/drift; tidak boleh dianggap izin coding.
- Log adalah riwayat sesi, bukan master kedua. Laporan adalah bukti bertanggal.
- Source implementasi tetap di tiga repo komponen; **docs bukan runtime config**.
- Semua dokumen operasional sekarang dipusatkan di repo ini. README komponen hanya
  memberi navigasi/petunjuk menjalankan repo masing-masing.
- File context root lama hanya penunjuk. Tidak ada master aktif kedua di root workspace.

## Cara menyimpan workspace untuk handover

```text
company-ai-platform/            # folder biasa; bukan parent Git yang dibuat sesi ini
├── llm-gateway-docs/           # repo docs existing
├── llm-gateway-infra/          # repo Docker dan script operasi
├── llm-gateway-config/         # repo config/model/policy/client template
└── llm-gateway-e2e/            # repo pengujian
```

Tautan antarrepo memakai layout sibling ini. Pada Git web viewer repo terpisah, tautan
ke source sibling mungkin tidak dapat dinavigasi; clone berdampingan atau gunakan URL
commit repo yang disepakati saat rilis. Jangan mengarang remote/organization.
Validasi repo docs sendiri boleh melewati tautan source sibling yang belum di-checkout;
validasi handover lengkap memerlukan empat repo dan mode `--workspace`.

```bash
# Dari llm-gateway-docs; tidak mengakses Docker/provider:
python3 scripts/validate-docs.py --workspace
```

Migrasi lokal **belum commit/push**. Tidak membuat repo/remote/submodule baru. Jangan
hanya menyerahkan commit HEAD lama: perubahan source dan dokumen masih perlu dipublikasikan
sesuai review/gate masing-masing. Data rahasia diserahkan lewat jalur terpisah yang aman.
