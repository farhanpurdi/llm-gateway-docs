# Usulan promosi candidate ke main

Status **PROPOSED**,17Oktober2026. Tidak ada merge/force-push/reset history.
Source candidate saat ini direview lewat draftPR pada **develop existing**, mengikuti
jalur PRH7/H8 yang sudah dipakai pengguna. [Refs](phase1-final-evidence/component-candidates.json)
dan [auditmain](phase1-final-evidence/remote-main-audit.json).

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

## Opsi yang dapat disetujui

**A — pertahankan kedua history melalui merge biasa pada branch promosi baru.**
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

Rekomendasi teknis:A bila pengguna ingin menutup jalur release main sekarang;
B bila ingin meninjau candidate dan keputusan server/CVE terlebihdahulu.
Persetujuan O-08 hanya targetCI, bukan persetujuan menyatukan historymain.
