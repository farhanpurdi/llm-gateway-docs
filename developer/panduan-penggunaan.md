# Panduan penggunaan LLM Gateway — v0.0.1

Panduan untuk operator dan developer. **Phase 1 ditutup dengan catatan pada
18 Oktober 2026**; [keputusan lengkap](../reports/PHASE1_V0_0_1_CLOSEOUT.md).
Gateway lokal sudah diuji. Alamat VM GCP belum dicatat dan deployment VM belum
diverifikasi dalam dokumen ini. Ganti placeholder alamat/identitas dengan data operator.

## 1. Apa yang akan digunakan?

Alurnya: **OpenCode → gateway LiteLLM → OpenAI**. Developer memakai virtual key
miliknya; gateway memeriksa izin model, limit dan mencatat pemakaian.

| Nama yang dipilih developer | Kegunaan praktis | Mapping yang disepakati |
|---|---|---|
| `company-fast` | Mulai dari sini untuk pertanyaan singkat dan pekerjaan ringan | `openai/gpt-5.6-terra` |
| `company-coding` | Pekerjaan coding yang memerlukan pembacaan/perubahan file | `openai/gpt-5.6-sol` |

Nama model perusahaan tetap sama di laptop dan VM. Akses akhir mengikuti izin key/team.
Versi yang diuji: LiteLLM 1.104.0, PostgreSQL 16.15, Redis 7.4.11-alpine,
OpenCode 2.0.18; [batas kompatibilitas](compatibility.md). Ini bukan instruksi upgrade.

## 2. Bedakan tugas operator dan developer

| Operator | Developer |
|---|---|
| Menjaga gateway, membuat team/pengguna/key, memonitor biaya, menangani backup/incident | Memasang config OpenCode dan memakai model dengan virtual key sendiri |
| Menyimpan master/provider key di lingkungan server yang dikelola | Menerima alamat gateway dan virtual key; tidak menerima master/provider key |

Operator perlu memberi developer tiga informasi: **alamat API**, **virtual key pribadi**,
dan **model/limit yang boleh dipakai**. Bagikan key melalui jalur privat; jangan masukkan
ke Git, screenshot, tiket atau laporan.

## 3. Operator: periksa gateway yang sudah berjalan

Empat repo harus berdampingan di folder `company-ai-platform`. Perintah berikut dari
root workspace, pada host yang memang sudah mempunyai runtime dan environment Python:

```bash
source .venv/bin/activate
cd llm-gateway-infra
./scripts/health/check-all.sh
```

Hasil health yang lulus menunjukkan layanan/dependency/catalog siap pada host tersebut.
Belum membuktikan satu request provider berhasil. Jangan menyalin `.venv` macOS ke VM
Linux; setup dependency VM mengikuti README komponen dan perlu diperiksa di VM.
Runbook [deployment](../operations/deployment.md) yang ada adalah release/rollback
**konfigurasi pada runtime existing**, bukan installer VM GCP baru.

Alamat lokal developer: `http://localhost:4000/v1` jika gateway berada di laptop yang
sama. Untuk VM, operator memberi alamat seperti `http://ALAMAT_VM:4000/v1`.
`localhost` pada laptop tidak menunjuk VM. Keputusan HTTP/default firewall adalah
pendekatan awal pengguna; akses VM dan aturan firewall aktual tetap perlu diverifikasi.
Jangan membuka PostgreSQL/Redis ke internet untuk membuat OpenCode terhubung.

## 4. Operator: membuat akses developer

Jalankan dari repo `llm-gateway-infra`, dengan `.env` operator existing yang menunjuk
gateway tujuan. Script memuat `.env` itu sendiri; tidak perlu menempel master key
ke command di bawah. Periksa target sebelum membuat data pengguna.

**A. Gunakan team pilot yang sudah ada, atau buat sekali jika memang belum ada.**

```bash
./scripts/teams/create-team.sh pilot
```

Perintah tersebut membuat team baru; jangan diulang untuk setiap developer. Ambil
`team_id` dari respons dan simpan sebagai identitas team kerja. Jika team sudah ada,
gunakan ID yang dicatat operator. Jangan menebak ID dari nama team.

**B. Ganti dua placeholder berikut, lalu lakukan onboarding sekali untuk pengguna itu.**

```bash
TEAM_ID="GANTI_DENGAN_TEAM_ID"
USER_ID="developer@perusahaan.example"
./scripts/onboard-developer.sh "$USER_ID" "$TEAM_ID" pilot
```

Script membuat user, memasukkan user ke team dengan budget anggota dan menerbitkan
virtual key. Output terakhir berisi key sensitif. Serahkan kepada pemiliknya secara
privat, jangan simpan output mentah sebagai log. Jika gagal sebagian, periksa user/team
sebelum mengulang agar tidak menerbitkan key tambahan tanpa sengaja.

Policy yang dipakai tetap [pilot.yaml](../../llm-gateway-config/policies/teams/pilot.yaml):

| Batas | Nilai |
|---|---|
| Model team | `company-fast` dan `company-coding` |
| Budget team | US$10 untuk periode budget; dipakai bersama seluruh anggota |
| Budget anggota | US$2 per anggota untuk periode budget |
| Request/token | RPM30 dan TPM100000 pada team |
| Durasi dari script | `30d`; pada versi teruji reset awal bulan berikutnya 00:00 UTC, scheduler sekitar 10 menit |

Budget adalah batas, bukan saldo prepaid atau target belanja. Ini bukan persetujuan
budget perusahaan dari manager. User/team lama tidak otomatis dimigrasikan hanya
karena script atau YAML berubah.

## 5. Developer: siapkan credential tanpa menaruhnya di config

Di terminal yang akan dipakai OpenCode, tempel **virtual key pribadi** setelah
menjalankan baris pertama, lalu tekan Enter. Input tidak ditampilkan di layar:

```bash
read -r -s COMPANY_LLM_API_KEY
export COMPANY_LLM_API_KEY
printf '\n'
export COMPANY_LLM_BASE_URL="http://localhost:4000/v1"
```

Ganti `COMPANY_LLM_BASE_URL` dengan alamat dari operator jika memakai VM. Variabel
ini dipakai contoh curl berikut. Untuk OpenCode, sesuaikan `settings.baseURL` pada
config juga; mengubah environment ini saja tidak mengubah template OpenCode existing.
Environment berlaku untuk terminal ini; jangan memakai `set -x` atau mencetak key.

## 6. Developer: periksa koneksi dan satu request kecil

Daftar model, tanpa request inference berbayar:

```bash
curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 30 \
  "${COMPANY_LLM_BASE_URL}/models" \
  -H "Authorization: Bearer ${COMPANY_LLM_API_KEY}"
```

Jika berhasil, uji satu request berikut. **Request ini menggunakan biaya provider.**

```bash
curl --fail-with-body --silent --show-error --connect-timeout 5 --max-time 180 \
  "${COMPANY_LLM_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer ${COMPANY_LLM_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"company-fast","messages":[{"role":"user","content":"Balas dengan OK"}]}'
```

Daftar model hanya pemeriksaan akses/catalog; keberhasilan request kedua membuktikan
satu inference. Jangan kirim dokumen rahasia untuk pengujian awal. Respons/request
berisi data pengguna; bagikan hanya error/request ID yang sudah disanitasi.

## 7. Developer: gunakan OpenCode

Gunakan [template OpenCode](../../llm-gateway-config/clients/opencode/opencode.jsonc)
sebagai `opencode.jsonc` di folder proyek yang akan dikerjakan. Jika sudah punya config,
gabungkan bagian provider perusahaan; jangan menimpa config pribadi.

Pada template tersebut, sesuaikan hanya alamat koneksi lokal Anda:

```json
"settings": {
  "baseURL": "http://ALAMAT_VM:4000/v1"
}
```

Potongan di atas bukan file config lengkap. Template lengkap sudah mempunyai
`providers.company-ai`, pembacaan `COMPANY_LLM_API_KEY`, dua alias dan default
`company-ai/company-coding`. Untuk gateway di laptop yang sama, alamatnya tetap
`http://localhost:4000/v1`. Jangan mengedit template bersama untuk satu laptop.

Jalankan dari proyek yang memuat config, di terminal yang sudah memuat virtual key:

```bash
opencode run --standalone --model company-ai/company-fast "Jelaskan tujuan proyek ini secara singkat"
opencode run --standalone --model company-ai/company-coding "Tinjau kode proyek ini dan jelaskan temuan; jangan ubah file dahulu"
```

Perintah tersebut memakai provider berbayar dan dapat membaca source proyek sesuai
permission client Anda. Mulai dari folder/proyek yang memang diizinkan. Periksa hasil
perubahan kode dan jalankan tes proyek Anda; model tetap dapat membuat kesalahan.
[Panduan OpenCode rinci](opencode.md) menjelaskan adapter dan batas pengujian.

## 8. Kalau muncul error

| Gejala | Langkah sederhana |
|---|---|
| Connection refused/timeout sebelum mendapat respons | Periksa gateway hidup, alamat VM, port dan jalur jaringan. Memakai localhost di laptop tidak mengakses VM. |
| 401 | Periksa virtual key benar, belum diblokir/expired dan environment sudah terisi di terminal yang dipakai. |
| 403 | Periksa izin key/team untuk model tersebut; minta operator memeriksa scope. |
| 429 | Tunggu pembatasan request/token pulih; kurangi request bersamaan. Jangan menaikkan limit sendiri. |
| 422 dengan pesan budget | Budget key/anggota/team habis; operator memeriksa scope dan waktu reset. Bukan semua 422 berarti budget. |
| 5xx atau timeout provider | Operator memeriksa health/dependency/provider. Jangan melakukan retry tanpa batas. |

Laporkan waktu, model, status/error dan request ID. Tidak perlu mengirim key, `.env`,
prompt atau source sensitif. Jangan memakai master key untuk melewati error developer.

## 9. Operator: pantau pemakaian dan cabut akses

Gunakan ID dari onboarding untuk membaca team/pengguna pada gateway yang dituju:

```bash
./scripts/teams/show-team.sh "$TEAM_ID"
./scripts/users/show-user.sh "$USER_ID"
```

Perintah ini dijalankan operator dari repo infra, bukan terminal developer. Baca
spend/budget yang tersedia pada respons; bukan perhitungan invoice akhir provider.
Untuk diskusi manager, catat periode, jumlah pengguna/request, spend, error, CPU/RAM
dan kebutuhan backup. Sensor output sebelum dibagikan. HTTP langsung melalui internet
belum mengenkripsi virtual key, prompt/source dan respons; penguatan ditunda O-10.

Jika key bocor atau pengguna keluar, operator memblokir **seluruh key pengguna tersebut**,
memverifikasi penolakan akses dan mempertahankan histori. Jangan hanya menghapus config
OpenCode, hard-delete audit, atau memblokir team bersama. Ikuti
[lifecycle/rotasi/offboarding](../operations/lifecycle.md).

## 10. Backup, snapshot dan Redis: apa yang sudah disepakati?

- Snapshot VM GCP menjadi pilihan awal yang akan dibahas dengan manager. Jadwal dan
  retensi belum dipilih. Pastikan disk yang menyimpan volume database dan konfigurasi
  tercakup, serta uji pemulihannya. [Runbook backup](../operations/backup.md).
- Dump PostgreSQL, metadata verifikasi dan `.env` pemulihan/salt sudah didukung script
  existing; semuanya sensitif dan tidak boleh masuk Git/chat. File permission bukan
  enkripsi file. Pemulihan lokal pernah diuji, snapshot GCP belum.
- TTL Redis yang diinginkan **24 jam** berarti masa simpan key tertentu ketika nanti
  diaktifkan. Redis belum menjadi cache LiteLLM pada YAML existing. TTL tidak
  menghapus riwayat PostgreSQL, mereset budget atau mengubah masa berlaku virtual key.
- Belum ada pembatasan pengguna Redis tambahan yang diputuskan. OpenCode berbicara
  dengan LiteLLM, tidak menghubungi Redis langsung; tidak perlu membagikan akses
  Redis kepada developer atau membuka port 6379.

## 11. Pekerjaan yang belum dijalankan oleh panduan ini

Penetapan v0.0.1 dan penutupan fase dicatat atas persetujuan pengguna. Panduan ini
tidak membuat tag, menjalankan deployment GCP, mengaktifkan TTL/cache atau jadwal
snapshot. Ikuti [catatan penutupan](../reports/PHASE1_V0_0_1_CLOSEOUT.md) untuk daftar
lanjutan. Phase 2/3 dimulai hanya setelah instruksi baru dari pengguna.
