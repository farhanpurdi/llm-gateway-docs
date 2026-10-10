> **Laporan historis:** hasil dan potongan source mengikuti sesi yang tercantum, bukan status current setelah migrasi.
> Baca [master aktif](../MASTER_CONTEXT.md) dan [Phase1](../architecture/phase-1.md); path pada blok kode/log bisa merupakan path lama.
> Tautan navigasi disesuaikan saat migrasi; hasil tes dan isi blok kode tidak diubah.

# Laporan Phase 1 — H1 sampai H10D

Tanggal pengujian: **10 Oktober 2026**. Target: **Docker existing, http://localhost:4000**.

**H10B–H10D selesai untuk implementasi dan verifikasi lokal.** Semua pengujian akhir
lulus. Beberapa bug dan celah verifikasi ditemukan lalu diperbaiki, sehingga hasilnya
bukan sekadar mengulang tes lama. Belum ada deploy server, commit/push, atau eksekusi
CI remote pada perubahan ini.

**Keputusan:** layak melanjutkan persiapan deploy Phase 1 secara bersyarat. Belum
menyatakan siap go-live tanpa review temuan keamanan, CI candidate final, serta
konfigurasi server. Lulus baseline keamanan tidak berarti bebas kerentanan.

[Seluruh kode perubahan dan konfigurasi acuan](PHASE1_CODE_APPENDIX.md) tersedia
sebagai blok kode lengkap, disertai path file dan checksum. Handoff juga diperbarui.

## Ringkasan hasil

| Pemeriksaan | Hasil akhir |
|---|---|
| Validator infra | 7/7 tahap PASS, termasuk 12 tes regresi operasional |
| Validator config | 6/6 tahap PASS |
| Validator E2E | 8/8 tahap PASS |
| E2E/unit akhir | **37 PASS: 22 unit + 3 smoke + 12 live** |
| OpenCode existing | PASS, respons `OPENCODE_E2E_OK` lewat company-fast |
| Backup/restore | PASS, **83 tabel** sama jumlah baris dan sidik datanya |
| Release + rollback config | PASS; smoke 3/3 pada tiap tahap, config awal pulih persis |
| Outage Redis dan PostgreSQL | Terdeteksi, masing-masing pulih, health akhir PASS |
| Secret scan | Ketiga repo PASS: canary, riwayat Git, file kerja |
| Audit dependensi Python | Ketiga repo PASS, tidak ditemukan kerentanan dikenal oleh auditor |
| Scan image | PASS terhadap baseline existing; rincian temuan ada pada H7 |
| Lingkungan | Hanya 3 container asli, ID tidak berubah, port gateway 4000 |

Tes live mencakup inference kedua alias, streaming, tool calling kedua alias, perubahan
policy tanpa mengganti key, RPM, budget, blocked key, multi-key/offboarding, serta
spend/histori. Hasil live akhir: **12 PASS dalam 50,64 detik**. Tidak ada error teardown.

## H1 — Versi runtime jelas

**Dipertahankan:** LiteLLM `1.104.0`, PostgreSQL `16.15`, Redis `7.4.11-alpine`.
Tidak mengganti image atau membuat container. Audit mencocokkan image yang dipindai
dengan image container yang benar-benar berjalan. Manifest release kini menyimpan
ID image dan ID container, selain commit/checksum source.

```yaml
image: ghcr.io/berriai/litellm:1.104.0
# Service database:
image: postgres:16.15
# Service cache:
image: redis:7.4.11-alpine
```

**Hasil:** PASS. Container asli tetap `9c77da1dea53`, `2abff28af371`, `04c48e8f579d`.
Bukti: [runtime-audit.txt](phase1-evidence/runtime-audit.txt).

## H2 — Perlindungan secret

**Pembaruan:** izin `.env` existing diperketat dari 644 menjadi **600**. Backup sekarang
menyimpan pasangan environment yang diperlukan untuk recovery (termasuk salt), dengan
izin file 600/folder 700. Nilai secret tidak dimasukkan ke laporan. `.env`, backup,
dan manifest release tidak ikut Git. Secret penting di `.env` cocok dengan container.

```bash
umask 077
chmod 700 "$BACKUP_DIR"
cp "$ENV_FILE" "$BACKUP_FILE.env"
chmod 600 "$BACKUP_FILE" "$BACKUP_FILE.env"
```

**Hasil:** PASS untuk izin, pengecualian Git, dan scan secret. Backup `.env` tetap data
sensitif: perlu storage terenkripsi di luar host sebelum operasional server.

## H3 — Jaringan dan mount config

**Dipertahankan:** PostgreSQL/Redis tidak memublikasikan port host. Gateway existing
memakai port 4000. Bind mount config read-only dan Compose menolak membuat folder
pengganti ketika file config tidak ditemukan. Path contoh environment juga dibetulkan.

```yaml
volumes:
  - type: bind
    source: ${LITELLM_CONFIG_PATH:-../llm-gateway-config/config/litellm_config.yaml}
    target: /app/config.yaml
    read_only: true
    bind:
      create_host_path: false
```

**Hasil:** PASS. Catatan server: gateway existing terikat ke `0.0.0.0`/IPv6, bukan hanya
loopback; pembatasan firewall dan TLS harus disiapkan sebelum diakses pengguna server.
Hardening deklarasi Compose diperiksa statis; container tidak di-recreate. Mount yang
sedang berjalan telah diverifikasi menuju file config yang benar dan read-only.

## H4 — Kesehatan layanan dan pemulihan gangguan

**Bug yang ditemukan:** endpoint HTTP readiness masih memberi 200 ketika Redis atau
PostgreSQL dimatikan. Monitoring yang hanya membaca status HTTP dapat salah memberi
status sehat.

**Perbaikan:** script readiness ikut menguji dependency secara langsung. Liveness,
readiness dan functional catalog request diberi timeout. Nama container tersedia
melalui common script dengan default container existing.

```bash
# Sesudah HTTP readiness berhasil:
"$SCRIPT_DIR/dependencies.sh" >/dev/null
echo "LiteLLM readiness (HTTP + dependencies): OK"
```

**Hasil:** outage Redis dan PostgreSQL diuji satu per satu, stop/start pada container
asli. Setelah perbaikan, script readiness gagal saat dependency mati dan kembali lulus
sesudah pulih. Provider inference juga lulus pada regresi setelah recovery. Endpoint
upstream sendiri tidak diubah; monitor server perlu memakai pemeriksaan setara.
Bukti: [failure-recovery-final.txt](phase1-evidence/failure-recovery-final.txt).

## H5 — Backup benar-benar dapat dipakai

**Penambahan:** checksum SHA256 dump + environment, metadata sumber, verifikasi arsip,
pembatasan target restore, dan perbandingan isi seluruh tabel hasil restore. Wrapper
restore lama kini memakai jalur aman yang sama. Backup gagal tidak ditinggalkan
sebagai arsip seolah-olah lengkap.

**Pengaman penting:** hanya `<POSTGRES_DB>_restore_test` yang boleh ditimpa. Nama lebih
dari 63 karakter ditolak agar pemotongan identifier PostgreSQL tidak mengarah ke
nama database utama. Tes negatif membuktikan penolakan terjadi sebelum Docker dipanggil.

```bash
RESTORE_DB="${RESTORE_DB:-${POSTGRES_DB}_restore_test}"
# Script juga memeriksa format, panjang <=63, dan kecocokan suffix khusus.
./scripts/backup/drill.sh --quiesce
```

**Hasil:** **83 tabel PASS**, jumlah baris dan fingerprint isi identik. Database test
dibuat dalam PostgreSQL yang sama; tidak ada container/volume baru. Database aplikasi
utama tidak direstore. Gateway berhenti sebentar agar data tidak berubah selama
perbandingan, lalu menyala kembali. Database test ditinggalkan untuk pemeriksaan.

Bukti: [backup-restore.txt](phase1-evidence/backup-restore.txt). Drill membuktikan
integritas restore DB, bukan boot aplikasi terhadap DB restore atau downgrade schema.

## H6 — Validasi dan pemeriksaan regresi

**Perbaikan:** folder kosong lama `llm-gateway-config/litellm_config.yaml` menyebabkan
validator YAML crash. Folder kosong itu dihapus; validator sekarang memberi pesan jelas
jika menemukan direktori dengan nama YAML. Common script juga tidak lagi menimpa
`SCRIPT_DIR` milik pemanggil, yang bisa menyebabkan script mencari helper di folder salah.
Onboarding kini mewajibkan tiga argumen sebelum membuat user/key.

**Penambahan:** 12 tes operasional untuk target restore, identifier terlalu panjang,
backup rusak, readiness palsu, argumen onboarding, direktori script, checksum/identitas
release, alias/credential config, penulisan mount, dan recovery deploy yang gagal.
Workflow infra memasang dependensi validator sebelum menjalankan tes.

```bash
if [ "$#" -ne 3 ]; then
    echo "  $0 <user-id> <team-id> <team-policy-name>"
    exit 1
fi
```

**Hasil:** infra 7/7, config 6/6, E2E 8/8 PASS. Bukti tersimpan pada
[infra](phase1-evidence/infra-validation.txt), [config](phase1-evidence/config-validation.txt),
dan [E2E](phase1-evidence/e2e-validation.txt). Hasil ini lokal, belum CI remote.

## H7 — Scan keamanan

**Pembaruan:** scan secret kini memeriksa file kerja tracked/untracked yang tidak
 di-ignore, selain riwayat Git. Sebelumnya file baru/belum commit bisa lolos dari cakupan
scan history. Scanner dapat memakai binary native melalui `GITLEAKS_BIN`, `TRIVY_BIN`,
dan `PIP_AUDIT_BIN`; tidak membuat container scanner tambahan pada sesi ini.

```bash
GITLEAKS_BIN=/path/to/gitleaks ./scripts/security/scan-secrets.sh
TRIVY_BIN=/path/to/trivy ./scripts/security/scan-containers.sh
PIP_AUDIT_BIN=/path/to/pip-audit ./scripts/security/audit-python.sh scripts/requirements.txt
```

Gitleaks 8.28.0 dan Trivy 0.74.0 diunduh dari rilis resmi dan checksum arsip diverifikasi.
pip-audit 2.10.1 dijalankan dengan Python existing, paket tool di folder sementara.

| Image existing | Critical fixable | High fixable | Baseline C/H | Hasil |
|---|---:|---:|---:|---|
| LiteLLM 1.104.0 | 0 | 0 | 0 / 0 | PASS |
| PostgreSQL 16.15 | **1** | **28** | 2 / 28 | PASS dengan temuan tersisa |
| Redis 7.4.11-alpine | 0 | **2** | 0 / 4 | PASS dengan temuan tersisa |

Critical PostgreSQL yang terdeteksi scanner: **CVE-2025-68121**, paket Go `stdlib`
versi `v1.24.6`. Ini temuan di image, bukan pernyataan bahwa engine PostgreSQL pasti
bisa dieksploitasi dari deployment ini. Review paparan dan perbaikan image perlu
keputusan keamanan sebelum go-live. **Baseline tidak dinaikkan dan image tidak diganti.**

Ketiga audit Python dan ketiga secret scan PASS. H7 merge gate GitHub tetap dianggap
terverifikasi berdasarkan konfirmasi user sebelumnya; tidak diklaim diperiksa ulang
remote pada sesi ini. Bukti: [scan image](phase1-evidence/containers-security.txt),
[rincian CVE/paket/perbaikan](phase1-evidence/vulnerability-details.json).

## H8 — Pembatasan pemakaian dan integrasi

**Dipertahankan dan diuji ulang:** RPM, budget, blocked key, perubahan policy team
 tanpa rotasi key, inference dan streaming. **Ditambahkan:** dua kasus tool calling,
masing-masing company-fast dan company-coding, karena belum tercakup eksplisit oleh
suite lama. Tool hanya dikembalikan model sebagai data; tidak mengeksekusi aksi eksternal.

```python
assert calls[0]["function"]["name"] == "lookup_ticket"
assert json.loads(calls[0]["function"]["arguments"]) == {"ticket_id": "TICKET-123"}
```

**Hasil:** seluruh kasus PASS. OpenCode existing dengan template project juga PASS
menggunakan virtual key healthcheck, bukan master/provider key. Bukti:
[regresi akhir](phase1-evidence/full-regression-final.txt), [OpenCode](phase1-evidence/opencode.txt).

## H9A–H9E — Multi-key, offboarding, dan histori

**Pekerjaan user H9A–H9D dipertahankan.** H9E dari checkpoint sebelumnya tetap aktif:
22 unit test, dua tes lifecycle wajib pada validator, serta pemisahan unit/smoke/live.
Arsitektur HTTP client tetap memakai `LiteLLMClient`.

```python
result = admin_client.offboard_user_keys(user_id)
# Helper discovery seluruh halaman -> block seluruh snapshot -> validasi respons.
# Tes lifecycle kemudian membuktikan key lama ditolak dan histori tetap ada.
```

**Hasil:** dua tes lifecycle live dan seluruh regresi unit PASS. Key fixture diblokir,
record audit tidak dihapus. H9D memeriksa retensi request/spend/user/team sebelum dan
sesudah offboarding dalam skenario tes.

**Batasan yang tetap ada:** snapshot key bukan locking otomatis. Key baru yang dibuat
bersamaan dapat terlewat. Runbook H10D mewajibkan freeze/serialisasi provisioning dan
pemeriksaan ulang semua key sebelum offboarding dinyatakan selesai. Jangan memblokir
shared team sebagai jalan pintas; kontrol HR/SSO dan hak menerbitkan key perlu dikelola
operator. Ini batasan operasional yang diketahui, bukan klaim sudah diperbaiki oleh tes.

## H10A — Environment existing, sesuai instruksi terbaru

Compose staging, script init/compose/verify staging, validator dan dokumen staging
dihapus. README tidak lagi mengarahkan ke staging. Hanya Docker asli port 4000 yang
dipakai. Tiga ID container sama sejak awal sampai akhir.

Sisa `.env.staging`, snapshot config dan data volume lama tidak dipakai dan tidak
 dihapus secara destruktif. Tidak ada container staging. Tidak membuat environment
aplikasi, container, network atau volume baru. Database restore-test pada H5 berada
di PostgreSQL existing.

## H10B — Release yang bisa ditelusuri

**Ditambahkan:** `scripts/release/release.sh` dan `manage.py`. Capture menyimpan config,
checksum, source revision/status dirty, checksum file source tiga repo, serta identitas
runtime. Deploy melakukan backup, menulis config pada inode yang sama, restart existing
gateway, membandingkan config dari dalam container, menunggu readiness, health dan smoke.
File lock menghindari dua release bersamaan.
Candidate final dicatat sebagai `phase1-h10d-local-20261010-final` sesudah perbaikan;
bukti capture ada di [final-candidate.txt](phase1-evidence/final-candidate.txt).
Manifest final mencatat source lokal yang masih dirty, bukan rilis Git yang sudah dipublikasikan.

```bash
./scripts/release/release.sh capture baseline-01
./scripts/release/release.sh capture candidate-01 --config /absolute/path/candidate.yaml
./scripts/release/release.sh deploy candidate-01
```

**Uji nyata:** request timeout sementara 180 → 181, lalu verifikasi container membaca
perubahan dan smoke 3/3 PASS. Bukan sekadar restart config yang identik.

## H10C — Rollback dan recovery

**Ditambahkan:** rollback dengan guard checksum/ID/image, backup sebelum perubahan,
catatan operasi, salinan config sebelum penulisan, dan pemulihan otomatis jika verifikasi
gagal. Error tetap dikembalikan walaupun recovery berhasil. Kondisi gagal diverifikasi
melalui unit test yang menjalankan alur deploy/recovery dengan kegagalan simulasi.

```bash
./scripts/release/release.sh rollback baseline-01
# Kode menjaga inode bind mount:
```

```python
with Path(path).open('r+b') as stream:
    stream.write(data)
    stream.truncate()
    stream.flush()
    os.fsync(stream.fileno())
```

**Uji nyata:** rollback ke timeout 180, config kembali identik byte demi byte, health
PASS, smoke 3/3 PASS, ID image/container sama. Bukti:
[release-rollback.txt](phase1-evidence/release-rollback.txt).

Batas rollback yang sudah terbukti adalah **config pada image/schema yang sama**.
Downgrade image, migrasi schema, serta pemulihan server total belum diuji pada sesi ini.
Script sengaja menolak runtime berbeda. File `.env` yang diedit tidak otomatis masuk
ke environment container hanya melalui `docker restart`.

## H10D — Runbook dan kesiapan pilot

**Ditambahkan/diperbarui:** empat dokumen operator:

- [Release dan rollback](../operations/deployment.md): langkah candidate, baseline, verifikasi dan kegagalan.
- [Backup/restore](../operations/backup.md): format backup, perlindungan salt, recovery dan batas drill.
- [Operasional](../operations/incident.md): onboarding, offboarding, incident, dan pilot kecil.
- [Checklist server](../operations/phase1-checklist.md): keputusan go-live yang harus diperiksa operator.

**Hasil:** runbook H10D selesai dan alur lokal terkait diuji. Kesiapan server masih
bersyarat: commit/push+CI candidate, review Critical/High, TLS/firewall, storage backup
terenkripsi di luar host, jadwal backup/alarm, PIC, budget pilot, serta tes target server.
Usulan retensi/RPO/RTO pada runbook belum merupakan layanan terjadwal atau SLA terukur.

## Temuan yang diperbaiki

| Temuan | Dampak praktis | Penyelesaian |
|---|---|---|
| Readiness HTTP false-positive saat dependency mati | Monitoring bisa memberi status sehat palsu | Script memeriksa DB/Redis; tes outage ulang PASS |
| `.env` berizin 644 | Akun lokal lain dapat membaca file sesuai akses direktori | Izin 600, diverifikasi |
| Folder kosong bernama config YAML | Validator berhenti dengan traceback | Folder kosong dihapus, pesan error diperjelas |
| Common script menimpa `SCRIPT_DIR` | Helper dapat dicari di folder yang salah | Gunakan `COMMON_DIR`, unit test |
| Onboarding menerima argumen kurang | Gagal pada variabel policy setelah alur dimulai | Wajib 3 argumen sebelum operasi |
| Restore belum ketat pada identitas target/arsip | Risiko salah target atau arsip rusak | Guard nama/panjang, metadata dan checksum |
| Backup tidak membuktikan semua isi hasil restore | Tabel ada belum tentu data utuh | Bandingkan 83 tabel pada drill |
| Scanner hanya melihat history | File baru/belum commit tidak ikut diperiksa | Tambah scan working tree non-ignored |
| Belum ada tes tool calling | Integrasi coding client kurang terlindungi | Dua kasus live, keduanya PASS |

Tidak ditemukan kegagalan yang tersisa pada skenario akhir yang diuji. Risiko/batas
operasional yang masih terbuka dijelaskan pada H7, H9 dan H10; pengujian ini tidak
menjamin semua kemungkinan bug atau kondisi server sudah tercakup.
