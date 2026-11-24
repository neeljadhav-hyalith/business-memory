---
name: business-memory
description: Gives Claude a lasting memory of a business, kept in a plain folder of Markdown files (an Obsidian vault or any folder). Use at the start of any session about the owner's work, and whenever the owner says "close the session", "save this", "update the vault", "what is open", "what did we decide", or asks Claude to remember a client, project, price or decision. Reads the index, the settled facts, the open items and the right card before it answers, writes by retiring old versions to an archive and never deleting, and closes each session with a short routine that logs, updates and checks sizes.
---

# Business memory

Claude starts every session knowing nothing about the business. This vault is the memory: a few small files that say what is true, what is open and where everything lives. Claude reads only what the job in hand needs, so the vault can grow for years without slowing a session down.

The owner's own rules for this vault (business name, domain codes, what never goes in it) are in `Context\instructions.md`. Read it first. Where it and this skill disagree, `instructions.md` wins for that vault.

## The vault

| File or folder | Job | Changes |
|---|---|---|
| `Context\00-index.md` | The router: 1 row per job, naming the file to open | When a card is added or renamed |
| `Context\00-settled.md` | Facts that do not change: proven, with a source. Outranks every other file | When a fact is proven |
| `Context\00-state.md` | Open items, 1 row each | Every close |
| `Context\_state-closed.md` | Closed rows, kept for search | Every close that closes a row |
| `Context\instructions.md` | The owner's rules for this vault | Rarely, on the owner's word |
| `Context\*_card_v*.md` | 1 operating card per client, project or area of the business | When something true about it changes |
| `Context\_archive\` | Every retired version. Nothing is ever deleted | Every time a file is retired |
| `Daily\YYYY-MM-DD.md` | Event log: what happened, in order. Never read as current state | Every close |
| `Projects\` | Drafts in progress and long session notes | Any time |

## 1 home per fact

A fact written in 2 places will disagree with itself within weeks. Put each fact in exactly 1 file and point to it from everywhere else.

| The fact | Its home |
|---|---|
| Proven and fixed: a legal name, a signed price, a registration number, a decision the owner has closed | `00-settled.md` |
| Where something stands: waiting on a reply, a draft sent, an invoice open | `00-state.md`, 1 row |
| True about the client or project: who decides, the scope, the constraints, what to never raise | The card |
| Where a file lives | `00-index.md` |
| What happened today | `Daily\` |
| A rule about how Claude should work | `instructions.md` |
| A dated reminder | The owner's task app or calendar. A vault row is no alarm clock |

## Start of a session: the read order

1. `Context\instructions.md`, unless it is already loaded as project instructions.
2. `Context\00-index.md`. Find the row for the job. If no row fits, say so and ask which card applies.
3. `Context\00-settled.md`. Section 1 every session. Other sections only when the job touches that domain.
4. `Context\00-state.md`. Search by the row prefix and the client or project name. Read only those rows, in full.
5. The card the router names. The highest version on disk is the truth.
6. `Daily\` files dated after the `last_close:` line in `00-state.md`, for events on the rows in hand. An event means: open the artifact before you act on it.

Stop reading when you have enough for the job. Open `Projects\` only when a card or a row names the file. Never browse it.

Line 1 of your first answer names the row you are working from (`EXC-WEBSITE`), or says "no row".

**The ask-gate.** Before asking the owner for a document, a figure or a confirmation, check `00-settled.md` and the card. Found: state it and ask only whether it is still current. Not found: name the files you checked.

**Never carry a negative forward unopened.** "Not sent", "unpaid", "no reply" go stale fastest and cost the most when wrong. Open the email, the invoice or the file the row names. If you cannot, say the row is unverified.

## How it writes

1. **Never delete.** Old versions are retired to `Context\_archive\`. A file that looks useless is named in your report and left where it is.
2. **Retire first, then edit.** Before changing a card, copy the current file into `Context\_archive\<card-name>\` under its original name. Then edit in place and bump the version in the filename and in the header line inside the file (`v3` to `v4`). For the files with fixed names (`00-index.md`, `00-settled.md`, `00-state.md`, `instructions.md`), put the date in front of the archive copy (`2026-11-24_00-state.md`) and bump the `version:` line inside.
3. **1 retire and 1 bump per file per session.** A second edit in the same session goes into the file you already bumped. No second archive copy.
4. **Never 2 versions side by side.** If you find 2, the lower one goes to the archive and you say so.
5. **Pointers name a pattern.** Write `example-co_client-card_v*.md, highest on disk`. A pointer naming `_v3` breaks silently the day v4 exists.
6. **Verify every write.** Re-read the file, quote the line you changed and give its size in bytes. A write you did not re-read is unverified, and you say so.
7. **Never change the owner's own words** in a draft, a message or a card's quoted instruction. Propose the change.
8. **Nothing secret goes in.** No passwords, card or bank numbers, API keys or identity numbers of people. If the owner pastes one, keep it out of every file and say so.

**If you cannot write files** (a Claude.ai project reads its knowledge files but cannot change them), do the same work as text: give each changed file in full under its new name, and list which old file the owner should move into `_archive\`.

## Close routine: end of every working session

Run it when the owner says "close", "save this" or "we are done", and offer it when a session moved real work and is ending.

**Nothing moved, nothing to close.** A session that only read, or only drafted something not yet sent, says "nothing to close" and stops. Most closes are small: 1 row rewritten and 3 lines of log. That is the normal case.

1. **Log.** Append to `Daily\YYYY-MM-DD.md` under `## Session - <topic>`: what happened, timestamped, 15 lines at most, each tagged with its row id. Create the file if today has none. Never a second file for the same date.
2. **Rows.** In `00-state.md`, rewrite the whole row for every item this session moved, within the caps below. Add a row only if it passes the admission test: *would a new session, not knowing this, say or do something wrong?* Money in flight, a person's position, a decision taken, a topic to avoid: all pass. "The owner must do X by Friday" fails: that belongs in the task app.
   - Each row carries a source grade: `doc` (you opened the artifact), `owner` (the owner said so), `log` (from a log, unverified). A `log` row never closes; it moves to `CONFIRM`.
   - A row untouched for 14 days moves to `CONFIRM`. List it for the owner. Never decide it yourself.
   - A closed row moves to `_state-closed.md`. Before it goes, every reference number in it (a contract number, a registration, an order id the business must keep) goes into `00-settled.md`. Closing a row is how references get lost.
   - Replace the 1 `last_close:` line at the top. Never append a second.
3. **Settled.** Add each fact proven this session to `00-settled.md`, 1 line, with its source (the file or message it came from). A wrong value that keeps coming back goes in the section for corrections, with the right value beside it.
4. **Card: add.** Add only what is true about the client or project and would make a session brief the owner wrong without it: a new person and their role, a price or scope ruling, a constraint, a resolved question. Where-it-stands belongs in the row. Long narrative goes to `Projects\<name>\YYYY-MM-DD_session-notes.md`, and the card gets 1 line pointing there.
5. **Card: subtract.** Every time you touch a card, test each line: *would a session brief the owner wrong without it?* These fail almost always: correction history, a figure already in `00-settled.md` (replace it with a pointer), and document detail that is 1 file-open away. Move each failed line, word for word, into the session notes before you remove it. A close that adds to a card and removes nothing has usually missed something. Say which lines you tested.
6. **Router.** A new or renamed card gets a row in `00-index.md` in the same close, as a pattern.
7. **Size gate.** Run `python scripts/vault_check.py <vault folder>` from this skill's folder, or measure by hand against the CAPS table. Over a cap and touched this session: cut now and measure again. Over a cap and untouched: report it. Under a cap by less than 200 bytes: report that too, because it breaks on the next edit.
8. **Report, 8 lines at most:** rows rewritten, added and closed; references moved into settled; cards changed, with bytes added and bytes removed; settled facts added; sizes against caps; anything you could not verify, named.

## CAPS: this table is the only home for these numbers

Do not restate them in a card, a row or `instructions.md`. Point here. `scripts/vault_check.py` reads them from this table.

| Key | What | Cap |
|---|---|---|
| `state_item_words` | `00-state.md` row, `item` column | 15 |
| `state_next_words` | `00-state.md` row, `next / blocker` column | 40 |
| `state_file_bytes` | `00-state.md`, whole file | 40960 |
| `card_bytes` | any operating card | 40960 |
| `headroom_bytes` | under cap by less than this: report it | 200 |
| `ageing_days` | row untouched this long moves to CONFIRM | 14 |

Sizes are bytes. `00-settled.md` has no byte cap: it is read by section, so its total size costs little. It is governed by 1 line per fact, and any section that no longer fits on 1 screen gets split. Report its size as a trend.

## Health check: on request, read-only

When the owner asks "check the vault", run `scripts/vault_check.py` and change nothing. An audit that also fixes things cannot report honestly on what it found. Report 1 table, worst first: what is wrong, where, and the 1 action that fixes it. Then the checks you could not run, and why. If everything passes, say so in 1 line.

The script checks sizes against the caps, rows over their word caps, 2 versions of a file side by side, router pointers that name a version or match no file, and cards no router row reaches. It cannot judge whether a card is stale. For that, compare each card's date with the newest row in its domain and name the specific facts missing.
