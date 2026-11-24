# business-memory

A Claude skill and a starter vault that give Claude a lasting memory of your business. The memory is a plain folder of Markdown files: an index that says which file to open for which job, a page of facts that do not change, a table of open items, your rules, and 1 card per client or project. Claude reads only what the job needs at the start of a session, and a short close routine at the end keeps the files current. Old versions go to an archive. Nothing is ever deleted.

Works with Obsidian or any folder. Works with Claude Code and with Claude.ai projects.

Built by Neel Jadhav, Hyalith AI. More free tools: https://hyalith.ai/resources

## Set it up in 10 minutes

1. **Copy the vault (1 minute).** Copy the `templates` folder to wherever you keep notes and rename it, for example `My-Business`. In Obsidian, open that folder as a vault. Any other folder works the same way.
2. **Write your rules (3 minutes).** Open `Context\instructions.md` and fill in the lines marked FILL: your business, the codes for your clients and areas of work, and what must never go in the vault.
3. **Write your settled facts (3 minutes).** Open `Context\00-settled.md` and replace the fictional lines with the 5 facts you get asked for most: legal name, what you sell, your standard price, payment terms, anything you never offer. Each line names its source.
4. **Make your first card (2 minutes).** Copy `Context\example-co_client-card_v1.md`, rename it for your biggest client or project, and fill in who decides, the scope and the constraints. Point the first row of `Context\00-index.md` at it, as a pattern (`acme_client-card_v*.md`). Replace the fictional rows in `Context\00-state.md` with your real open items.
5. **Connect Claude (1 minute).** See Install below. Then start a session with: "start from the vault: <the job>". End it with: "close the session".

The example files are fictional. Sample Studio is the business and Example Co. is its client. Replace or retire them as you go.

## Install

**Claude Code:** copy this folder into `~/.claude/skills/business-memory/` (or your project's `.claude/skills/`). Open Claude Code in your vault folder, or add the folder to the session. Claude Code reads and writes the files directly, so the close routine updates them for you.

**Claude.ai:** Settings > Capabilities > Skills > Upload skill, and upload a zip of this folder. Create a project, paste `Context\instructions.md` into the project instructions, and add the files in `Context\` to the project knowledge. A project can read its files but cannot change them, so at the close Claude gives you each changed file in full. You keep a copy of the old file in `Context\_archive\` and upload the new one in its place.

## Check the vault

Needs Python 3, no other installs. Read-only: it changes nothing.

```
python scripts/vault_check.py path/to/My-Business
```

It checks file sizes against the caps, rows over their word limits, rows nobody has touched in 14 days, 2 versions of a file side by side, router pointers that match no file, and cards no router row reaches.

## What is inside

- `SKILL.md`: the instructions Claude follows: the read order, how it writes, the close routine and the caps.
- `scripts/vault_check.py`: the read-only check. Reads the caps from `SKILL.md`, so they live in 1 place.
- `templates/`: the starter vault: `Context\` (index, settled facts, open items, closed items, your rules, 1 example card), `Context\_archive\`, `Projects\` and `Daily\`, each with a 2-line README.

## Licence

MIT. Use it, change it, share it.
