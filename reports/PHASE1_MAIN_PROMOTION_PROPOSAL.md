# Usulan promosi candidate ke main

**Pelaksanaan selesai:** pengguna melakukan review/merge sendiri. GitHub diperiksa
ulang18Oktober2026: config#4/infra#7/E2E#6/docs#1 merged dan main tree sama dengan
candidate. Detail proposal/status draft di bawah adalah riwayat sebelum merge.
[Refs terkini dan penutupan v0.0.1](PHASE1_V0_0_1_CLOSEOUT.md).

Status **APPROVED_OVERRIDE O-09**, 17 Oktober 2026. Pengguna menjawab
"Setuju, siapkan PR promosi main (disarankan)" atas opsi A di bawah.
Persetujuan mencakup penggabungan kedua history pada branch baru dan pembuatan
draft PR ke main. Main belum diubah; merge protected branch, force-push, tag dan
deploy tetap memerlukan otorisasi/gate masing-masing.

Tiga draft PR promosi sudah dibuat dan terpasang pada chat. Draft candidate ke
**develop existing** tetap terbuka sebagai jejak perubahan sebelumnya.
[Refs candidate](phase1-final-evidence/component-candidates.json) dan
[audit main](phase1-final-evidence/remote-main-audit.json) dipertahankan.

## Hasil penyiapan yang disetujui

| Repo | Draft PR aktif ke main | SHA promosi | Candidate sebelumnya ke develop |
|---|---|---|---|
| config | [#4](https://github.com/farhanpurdi/llm-gateway-config/pull/4) | `4cdc1ba1e555404010ab12f0f0b28e775fbea065` | [#3](https://github.com/farhanpurdi/llm-gateway-config/pull/3) |
| infra | [#7](https://github.com/farhanpurdi/llm-gateway-infra/pull/7) | `1289cbfafd0d8545053a221cb31fc16b1cd10f6d` | [#6](https://github.com/farhanpurdi/llm-gateway-infra/pull/6) |
| E2E | [#6](https://github.com/farhanpurdi/llm-gateway-e2e/pull/6) | `9eca7149d967c607146ab282421567eecd072626` | [#5](https://github.com/farhanpurdi/llm-gateway-e2e/pull/5) |

Branch ketiganya `release/phase1-main-review-20261017`. Setiap merge commit
mempunyai dua parent: candidate yang diuji dan initial main existing. Konflik
hanya README; isi candidate dipertahankan. Git tree hasil merge identik dengan
candidate, sehingga tidak ada perubahan kode/config/test dari penggabungan ini.
Inode dan byte config runtime juga tetap sama.
[Manifest pembuktian](phase1-final-evidence/main-promotion-candidates.json) mencatat
parent dan tree; [metadata PR](phase1-final-evidence/main-promotion-pull-requests.json)
menyimpan SHA/base/draft yang diperiksa. **Enam validate/security checks PASS**
pada SHA promosi tersebut; [bukti CI](phase1-final-evidence/main-promotion-ci-final.json).
Ketiga PR draft terverifikasi tanpa konflik merge; belum mendapat review/sign-off.
Dokumentasi direview pada [docs #1](https://github.com/farhanpurdi/llm-gateway-docs/pull/1).

## Fakta yang diperiksa

| Repo | main remote | Keadaan develop / riwayat |
|---|---|---|
| infra |4015f860bc5f5d78f8076e256840e9c155686a2a |PR#5merged kedevelop22ce39d; treeawal samaHEADlokal |
| config |89b2f099c00ab664e424678ba00461ed80c618ab |PR#2merged kedevelop0734b9c; treeawal samaHEADlokal |
| E2E |c234a7d9ec623d0ef5c28f00685d2a96016669e6 |PR#4merged kedevelop30a5b20; treeawal samaHEADlokal |
| docs |1d07d02ef942379263bd690c8dc3fe6a9f7c03a7 |main cocokHEADlokal; tidak memiliki masalah unrelated history |

Main tiga komponen masing-masing hanyaREADME/Initialcommit. Repo bukan shallow;
`git merge-base` membuktikan main tidak punya commonancestor dengan history kerja.
Ini gap jalur release keprotectedmain pada rancanganawal, bukan kegagalan gateway.

## Opsi yang diajukan dan keputusan

**A — DISETUJUI O-09: pertahankan kedua history pada branch promosi baru.**
Sesudah candidate direview dan CIhijau, buat branchpromosi dari candidate/develop,
merge main dengan `--allow-unrelated-histories`, selesaikan konflikREADME dengan
mempertahankan panduan proyek yang lengkap, lalu buat PRkemain. Jalankan CIoffline
padaSHA hasilmerge dan cocokkan filehash runtime/test terhadap bukti fulltest.
Jika sourceperilaku berubah, ulangi tes terkait; jangan menganggap merge metadata
sebagai bukti runtimebaru. Requiredreview/checks tidak dilewati.

```bash
# Contoh prosedur setelah persetujuan; jangan copy SHA/branch sebelum cek ref aktual.
git switch -c release/phase1-main-review <candidate-sha-yang-direview>
git merge --no-commit --no-ff --allow-unrelated-histories origin/main
# Review konflikREADME, pertahankan isi operasional dan asalhistory.
# Commit merge, push branchbaru tanpaforce, buat PRkemain dan tunggu review/CI.
```

Tidak ada forcepush, penggantian historymain, parentGit baru, migrasi repo atau
deployment. Risiko:PRpromosi awal besar karena main belum memuat source; reviewer
harus memeriksa isi dan kebijakan branch. Sebelum mergekeprotectedmain tetap perlu
approvalreview sesuai policy. Bila belummerge, rollback cukup menutup PRpromosi;
branch/historyexisting tetapada. Sesudahmerge gunakan revert yang direview, bukan
resetmain atau pemulihanDB.

**B — tunda promosi main dan handover candidate di develop.** Semua hasiltes tetap
berlaku sesuai hash; releaseformal/tag/sign-off belumditutup. Tidak mengubahbaseline
protectedmain menjadi develop secara diam-diam atau menyebut Phase1DONE.

Opsi B dipertahankan sebagai riwayat alternatif; pengguna memilih A. O-08 hanya
mengatur target CI. O-09 mengizinkan penyiapan PR promosi ini, bukan penerimaan
CVE/server, merge protected main, release tag atau sign-off Phase 1.
