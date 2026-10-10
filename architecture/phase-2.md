# Phase 2 — Control Plane (belum dimulai)

Baca [master](../MASTER_CONTEXT.md). Fase ini mempertahankan rancangan
[baseline §9](../archive/PROJECT_MASTER_CONTEXT.md#9-roadmap-phase-2--control-plane).
**Semua P2 berstatus NOT_STARTED.** Selesaikan/terima Phase1 gate dan dapatkan instruksi
user memulai fase ini. Kode helper admin E2E/onboarding bukan backend Control Plane.

## 1. Tujuan dan boundary

Admin/team lead mengelola user/team/model/key/budget dengan policy konsisten dan audit.
Control Plane mengatur akses melalui LiteLLM APIs; LiteLLM tetap menjalankan inference.
Frontend tidak pernah menerima master/provider key. Jangan menulis langsung schema
internal LiteLLM untuk provisioning. Database/schema app dikelola sendiri secara logis.

Repo baru yang **baru dibuat ketika fase ini dimulai**: `llm-control-plane`,
`llm-admin-portal`. Repo `llm-gateway-docs` sudah ada sejak penataan Phase1;
portal dokumentasi berhosting tetap opsional dan belum dibangun. FastAPI+SQLAlchemy/Alembic dan Next.js/React
adalah **usulan awal**, bukan pilihan final. SSO/IdP, RBAC, stack, license dan deployment
perlu ADR. Master aktif berada di `llm-gateway-docs/MASTER_CONTEXT.md`; portal hanya menautkan sumbernya.

## 2. Roadmap asli dan acceptance

| ID | Pekerjaan | Syarat penerimaan |
|---|---|---|
| P2-00 | Stack, IdP, RBAC, schema, licensing | ADR + kontrak API + lifecycle; tidak mengasumsikan fitur berbayar |
| P2-01 | Bootstrap backend + migrasi app | Health/test/CI; schema logis terpisah dari internal LiteLLM |
| P2-02 | SSO/OIDC admin | Login/logout, backend authorization dan role tests |
| P2-03 | User/team + membership IdP sync | Stable identifier, join/leave dan mapping teruji |
| P2-04 | Logical catalog/upstream deployment | CRUD/approval, alias stabil, secret tetap server |
| P2-05 | Policy ACL/precedence/default deny | Enforcement di LiteLLM, tes negatif lintas user/team/role |
| P2-06 | Key create/revoke/self-service | Raw key ditampilkan sekali lewat jalur aman, tidak plaintext di app DB |
| P2-07 | Budget/RPM/TPM user vs team | Semantik inheritance eksplisit dan enforcement teruji |
| P2-08 | Usage/cost API + reconciliation | Rollup user/team/model; source-of-truth dan akurasi jelas |
| P2-09 | Admin portal | Workflow users/teams/models/keys/cost, UI accessible, no master key in browser |
| P2-10 | Audit terbatas akses | Actor/action/time/old-new/ref, sensitive values redacted, append-oriented |
| P2-11 | Reconciler drift/retry/idempotency | Desired→actual policy, satu writer per domain, approval/version/rollback |
| P2-12 | Deprovision/acceptance | Disable IdP→revoke seluruh key relevan→deny traffic, audit dan tes |

Urutan ketergantungan: keputusan P2-00 → backend/auth/identity → policy/keys/budget/usage →
portal/audit/reconciler → penerimaan lifecycle. UI tidak mendahului kontrol authorization.

## 3. Data ownership: keputusan wajib

Phase1 memakai config Git + native LiteLLM DB/APIs secara manual. Phase2 wajib memilih
**satu desired-state writer per domain**, misalnya catalog Git atau app DB, bukan dua
penulis bebas. Adapter mengeksekusi melalui LiteLLM APIs. Tetapkan reconciliation,
idempotency, retry, drift detection, approval, rollback dan migrasi policy yang aman.

H9 saat ini hanya snapshot semua key + block, dengan freeze provisioning manual.
Jangan mengklaim itu sudah menutup disable SSO, session revocation, concurrent key
issuance, atau distribusi lintas replika. Penutupan itu bagian P2-12, dengan desain
otorisasi penerbitan key dan tes end-to-end; jangan membawa race lama tanpa penanganan.

## 4. Exit gate

- [ ] Self-service key scoped dengan backend authorization.
- [ ] Admin mengelola user/team/model/budget tanpa privilege escalation.
- [ ] Disable user benar-benar menghentikan akses seluruh key relevan.
- [ ] Audit dan reconciliation dapat diuji; satu writer per domain.
- [ ] Licensing, migration, review/CI/source refs dan operasi disetujui.

**Next ketika user mengizinkan fase ini:** P2-00. Saat ini tidak ada implementasi P2,
dan master tidak memberikan izin otomatis membuat repo/environment baru.
