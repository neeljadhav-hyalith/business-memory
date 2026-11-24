The event log: 1 file per date (`YYYY-MM-DD.md`), what happened, each line tagged with its row id.
Claude reads it for events since the last close and never quotes it as current state. That is the job of `Context\00-state.md`.
