---
file: 00-index.md
version: 1
changed: 2026-11-24 - starter version from the business-memory skill.
---

# 00 - Index (router)

_This file only says which file to open for which job. Rules live in `instructions.md`; open items live in `00-state.md`. Every pointer is a pattern: the highest version on disk wins. Example Co. is fictional._

## Read order
1. `00-settled.md`: section 1 every session; other sections when the job touches them.
2. `00-state.md`: search by row prefix and name; read those rows only.
3. The card in the table below.
4. `Projects\`: only when the card or a row names the file.

`Daily\` is the event log. Read it for events since the `last_close:` date in `00-state.md`. Never quote it as current state.

## Router: job to file

| Job | Read |
|---|---|
| Example Co.: proposals, calls, the website project, anything about this client | `example-co_client-card_v*.md`, highest on disk; status = `EXC-` rows |
| A new client or lead | Copy `example-co_client-card_v*.md` to a new card, add a row here and a code in `instructions.md` |
| Prices, legal name, registration numbers, "do we already have X" | `00-settled.md`, always |
| Invoices, payments, tax | `00-settled.md` section 2, then `FIN-` rows |
| This vault: where a file goes, how Claude writes | `instructions.md` |
| A dated reminder | Your task app or calendar. The vault holds no dates to chase |
