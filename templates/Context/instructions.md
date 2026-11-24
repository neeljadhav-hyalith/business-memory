---
file: instructions.md
version: 1
changed: 2026-11-24 - starter version from the business-memory skill.
---

# Instructions: the rules Claude follows in this vault

_Fill in the lines marked FILL. The examples are fictional: Sample Studio is the business, Example Co. is its client. In a Claude.ai project, paste this whole file into the project instructions field, and paste it again every time you change it._

## 1. Who this vault is for
- Business: FILL (for example: "Sample Studio, a 4-person design studio. Fictional.")
- Owner: FILL (your name and role)
- What Claude is here to do: FILL (for example: "draft proposals, keep track of clients, prepare calls")

## 2. Read order
Start at `Context\00-index.md` and follow its routing. Then `00-settled.md` section 1, then the rows in `00-state.md` for the job, then the card the router names. The highest version on disk is the truth. The business-memory skill carries the full read order and the close routine.

## 3. Domains and row prefixes
Every row id in `00-state.md` starts with 1 of these codes. Add a code when you add a client or an area of work.

| Code | Domain |
|---|---|
| `EXC-` | Example Co., a fictional client |
| `OPS-` | Running the business: tools, admin, this vault |
| `FIN-` | Invoices, payments, tax |
| FILL | FILL |

## 4. Naming
- Cards: `<client-or-project>_<kind>-card_v<N>.md`, for example `example-co_client-card_v1.md`. Lowercase, hyphens, no spaces.
- Daily logs: `Daily\YYYY-MM-DD.md`, 1 file per date.
- Drafts: `Projects\<client-or-project>\YYYY-MM-DD_<short-description>.md`.
- Nothing loose in the vault root.

## 5. Hard rules
1. Never delete anything in this vault. Retire old versions to `Context\_archive\`.
2. Retire the current version before every edit, then bump the version. 1 retire and 1 bump per file per session.
3. 1 fact, 1 home. Point to it from everywhere else.
4. Never ask me for something that `00-settled.md` or the card already holds. Check them first and name what you checked.
5. Never report "not sent", "unpaid" or "no reply" without opening the email, invoice or file. If you cannot, say it is unverified.
6. The size caps live only in the business-memory skill. Never copy a cap number into this file or a card.

## 6. Never in this vault
Passwords, API keys, card or bank account numbers, identity numbers of people, health details. FILL (anything else you keep elsewhere, for example signed contracts, which live in your shared drive and are linked from the card).

## 7. Who writes
FILL (for example: "Only Claude Code on my laptop writes to this vault. Other sessions read and propose.") 1 writer keeps 2 sessions from overwriting each other.

## 8. How to answer me
FILL (for example: "Short. Tables and bullets. Name the row you worked from on line 1.")

## 9. When files disagree
1. This file  2. `00-settled.md`  3. The card  4. `00-state.md`  5. `Daily\` (an event log only).
