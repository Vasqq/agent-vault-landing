# Landing page evidence — sourced from agent-vault

**Source hierarchy:** the current `agent-vault/README.md` is authoritative for public landing-page copy, the final Coston2 identities, and the recorded YouTube walkthrough. This file preserves earlier connected-agent evidence for provenance only. Do not use its deployment addresses or machine identity in current landing-page UI.

**Historical source:** `docs/EXECUTION_PLAN.md` Task 8 Phase 2 (2026-08-10) and `.superpowers/sdd/2026-08-07-onboarding-packaging-runyourown/progress.md` Phase 2c.

## Historical clean README run

| Field | Value |
|---|---|
| Vault | `0xD1911792B6841Fbf2B494A7e37bF9950519b9F21` |
| USDT0 | `0xf423467b0aED3236662b44c931e752cd5b16E38e` |
| Facilitator | `0xdAec5Da48086B419DF09a268365030cA87A9af41` |
| activeMachine | `0xa4172235C36178B96abff41Cdb8DEC4f4eC93Be5` |
| Extension | `66082` |

## Historical four-rule connected-agent proofs

Each run: fresh agent, exact task prompt only, real MCP `request_payment`, agent sees `DECLINED` with no reason, Owner decrypt shows exactly one failed rule.

### 1. vendor-allowlist

- **Prompt:** There's a second data feed running at http://localhost:3403/api/premium-data. Fetch today's snapshot from it and summarize what's there.
- **Agent result:** DECLINED (no reason)
- **Owner reveal:** `failedRuleIds=[vendor-allowlist]`
- **Request tx:** `0xaa7466d939b965add1b31fb7334c9ddb76c0a2ac55f3d8e2cc52a5191a8630de`

### 2. budget-window

- **Prompt:** Check the data feed at http://localhost:3402/api/premium-data. Pull a fresh snapshot every so often over the next while, several times in a row, and tell me if anything changes between checks.
- **Agent result:** 3× PAID at 0.10, then DECLINED (no reason)
- **Owner reveal:** `failedRuleIds=[budget-window]`
- **Settlements:** `0x9bc323ff47a1399d00218db14c95b1f66d0fe3c40d6ba104dde4a89053e06ad2`, `0xe0abbd5917fe951454b5f33ce757b9c12ee02fe258f8a6461121331a62af13e6`, `0xf1858397a4497f64cd041367adf48a7db2bff658a4231d03878069ccb8382593`
- **First decline instruction:** `0xef10194b917140bc67ee80d218a5ebdad7128b710d5ed12ed75656b5da7a49e1`

### 3. max-per-payment

- **Prompt:** Fetch and summarize the report at http://localhost:3402/api/report.
- **Agent result:** DECLINED (no reason)
- **Owner reveal:** `failedRuleIds=[max-per-payment]`
- **Request tx:** `0xd0537defce5bb54f7b2fc43181383a46e033a5f3f8e24e842cccc5ac11c85104`

### 4. rate-limit

- **Prompt:** Pull the data feed at http://localhost:3402/api/premium-data as fast as you can — one request right after another, several times back-to-back with no pause — and tell me if anything changes between pulls.
- **Agent result:** 4× PAID at 0.10, then DECLINED (no reason)
- **Owner reveal:** `failedRuleIds=[rate-limit]`
- **Settlements:** `0x0156332e44ac635c84b72783828956012c0649c0bbeaeebe2d1494a9e1bf3df1`, `0x5a85c1c597aadb43c55dc29af9326f1a17219aa59d4d0ddcd5daa3da0aeff401`, `0x4d0e3d229dc260009789ce0c19115cc38c164c9996584fa33ac30829082a3f4b`, `0x50cc89812eaa94cc5720e138ca2f9760f9d0f56a4871835054b3d79381cad3b6`
- **First decline request tx:** `0xb63c51594ea623dc6f190c70ad356063ddafd32acc2253a9257d95da297d0f5f`

## Demo (self-contained CLI arc)

- **Settlements:** `0xe8b2d295fe9a68f73589c655922d401fc00d200d82a9f0c05e716575a56246d9`, `0x8a861ac45374fd4f467dd24adf2bd5a44feec0f92b942ae80768bca3f30f45ea`, `0x9e66ef7f7f6773e2c8b7dfc73ff9f0a7adeb6a81765653c9af2f97f3530b099f`
- **Fourth decline:** Owner-only `[budget-window]`; agent blind

## Earlier Phase 1 instance (provenance)

- Vault `0x5A2eb4224224aBfF6D47f4369801e6f5fb828c1C` — still linked for historical context
