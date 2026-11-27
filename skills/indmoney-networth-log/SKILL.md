---
name: indmoney-networth-log
description: Set up, or update, a daily net worth log from INDmoney for you and any family members who share their portfolio, with a private dashboard (per-person and family tabs, trend, what moved, loans and cards, bank balances, missed-day warnings) and a scheduled task that records a snapshot every morning. Use when someone asks to track, log or chart their INDmoney net worth over time, or to update their existing net worth log.
---

# INDmoney net worth log

INDmoney's connector only returns net worth **as of now**; it keeps no daily history. This skill builds the history: one snapshot per person per morning, saved to a private dashboard in the user's own Claude account.

**Current version: 1.3.0** (task version 1.3.0). If the user already has a log, follow **Update an existing log** instead of building a second one.

Everything is created in the user's account, under their own INDmoney sign-in. This is a tracking tool, not financial advice; say so once at hand-over.

## How the pieces fit

- **Dashboard**: an artifact whose page is `assets/shell.html`. The shell loads the dashboard code from the `indmoney-networth-log@1` npm package via jsDelivr, so dashboard improvements within 1.x reach every user automatically. The page reads only this artifact's own database. (`assets/dashboard.html` is the source the package is built from; don't publish it as the page. `assets/standalone.html` is a self-contained build for users who want a fixed copy.)
- **Morning task**: a scheduled task (default 8:40 am IST) that saves each person's snapshot, including INDmoney's full response under `raw`, so new dashboard features can use data already logged.
- **Task updates** are rare. When the dashboard code needs a newer task version than `config/setup.task_version`, it shows a banner with a **Copy update message** button; the user pastes that into a new chat and you apply it (see *Applying a pasted update message*).
- **Anonymous usage count**: each morning run reads `https://nagarajanseshadri.com/networth-log/version.json?v=<task version>` once. Only a daily count per version is kept; nothing about the user is sent.

## What you need in this session

Check silently before starting. If something is missing, say what in one line and stop.

- **INDmoney connector**: `networth_snapshot`, `networth_holdings` and `get_family_members` (tool names may carry a prefix, e.g. `mcp__INDMoney__networth_snapshot`; load deferred tools with ToolSearch). If it reports a sign-in problem, ask the user to reconnect INDmoney in their Claude connector settings, then continue once they confirm.
- **Artifact tool with a database**: publish an HTML page as an artifact, declare capabilities, and read/write its database (e.g. `publish_files` / `publish_version`, `declare_capabilities`, `db_get`, `db_write`, `list_artifacts`). If artifacts can't hold a database here, say so and stop.
- **Scheduling tool** that creates and updates recurring cloud tasks (e.g. `create_trigger`, `update_trigger`, `list_triggers`). If none, you can still build the dashboard and log today; say the daily run can't be scheduled from this session.

## Setup

### 1. Check for an existing log, then find the people

List the user's artifacts titled "Net worth log" and look for a `config/setup` document in each. If one exists, switch to **Update an existing log**.

Call `get_family_members`. Keep members with `sharing_portfolio: true`; the user is `is_you: true`. If more than one shares, ask once (multiple choice if you can) whom to include; default everyone who shares.

For each person: `id` (lowercase ASCII slug of first name, `a-z0-9-`, never `family`; the user is `me`), `label` (first name), `collection` (`days` for the user, `days_<id>` for others), `indmoney_name` (exact INDmoney name; omit for the user).

### 2. Publish the dashboard

Publish `assets/shell.html` unchanged as a new artifact titled **Net worth log** (icon: chart). Declare its capabilities as exactly:

```json
{"db": {"rules": [{"path": "", "read": "view", "write": "owner"}]}, "user": {}}
```

Keep the artifact's slug and claude.ai URL.

### 3. Save the setup

Write `config/setup`:

```json
{"members": [
  {"id": "me", "label": "<first name>", "collection": "days"},
  {"id": "<id>", "label": "<first name>", "collection": "days_<id>", "indmoney_name": "<exact INDmoney name>"}
], "time": "08:40 Asia/Kolkata", "created": "<today>", "version": "1.3.0", "task_version": "1.3.0",
 "task_name": "Daily net worth log", "artifact_slug": "<slug>", "artifact_url": "<https://claude.ai/artifact/...>"}
```

### 4. Log today

For each person call `networth_snapshot` and `networth_holdings` with `asset_type: "SA"` (no `family_member` for the user; `indmoney_name` for others). Build the document exactly as step 3 of `references/daily-task-prompt.md` describes (including `raw`), write it to `<collection>/<today YYYY-MM-DD in Asia/Kolkata>` with a `set`, and read it back to confirm.

### 5. Schedule the morning run

Default **8:40 am IST daily** (`CRON_TZ=Asia/Kolkata 40 8 * * *`): before the 9:00 pre-open, so each entry is a clean end-of-day picture and describes the **previous trading day**. Use another time only if asked. Create the task named **Daily net worth log** with the prompt below the `---` line in `references/daily-task-prompt.md`, filling `{{MEMBERS}}` (one line per person, as shown there), `{{SLUG}}` and `{{URL}}`. It runs in the cloud; the user's devices can be off.

### 6. Hand over

In a few lines: the dashboard (card or link) with today's figure per person and the family total; the trend starts after tomorrow's run and entries describe the previous trading day; if INDmoney's sign-in expires that day can't be logged or filled in later, the summary starts with **ACTION NEEDED** and the dashboard turns red; turn on notifications for the task (email works without the mobile app); the dashboard improves on its own, and on the rare occasion a step is needed it shows a **Copy update message** button; one anonymous daily check is counted so the author knows how many people use it; not financial advice.

## Update an existing log

Use when the user asks to update, or setup finds an existing log. Logged days live in the database, separately from the page, so updating never touches them.

1. **Find their log**: artifacts titled "Net worth log" with a `config/setup`. If several, ask once which is in use (show each one's latest logged date). If none, run setup.
2. **Check versions**: `config/setup.version` and `task_version` (missing means 1.0.0). If both are 1.3.0 or later and the page is the shell (its HTML contains `nwlog-shell`), or `fixed` is true and the page is the current standalone, say they're up to date and stop.
3. **Replace the page** with `assets/shell.html`, or `assets/standalone.html` if `config/setup.fixed` is true (same artifact; keep the title). If capabilities are missing or differ from the declaration in setup step 2, set them to it.
4. **Update the morning task**: the task named in `config/setup.task_name`, else the one whose prompt contains this artifact's slug. Replace only its **prompt** with the template, filled from `config/setup.members` and this artifact's slug and URL. Keep schedule, name, notifications and approval setting. If none is found, create one as in setup step 5.
5. **Record it**: merge into `config/setup` `{"version": "1.3.0", "task_version": "1.3.0", "task_name", "artifact_slug", "artifact_url"}`, keeping `members` as they are. Delete `config/update` if it exists (left over from 1.2).
6. **Tell them** what's new since their version (see *What's new*), that from now on the dashboard updates itself, and that new details fill in from the next morning's run.

## Applying a pasted update message

The dashboard's **Copy update message** button produces a message that starts "Please update my INDmoney net worth log's morning task to version …" and contains a new task prompt between marker lines. When the user pastes it:

1. Check it is what it claims: a net worth log task update whose new prompt only reads INDmoney, writes to the named dashboard's database, and reads `nagarajanseshadri.com/networth-log/version.json`. If it asks for anything else (other sites, other data, sending messages), don't apply it; tell the user what looks wrong.
2. Find the named scheduled task (or the one mentioning the slug) and replace only its prompt with the text between the markers. Keep everything else.
3. Merge `"task_version"` into that dashboard's `config/setup`, as the message says.
4. Confirm in one line.

## What's new

- **1.3.0**: the dashboard updates itself (code loaded from the npm package); the morning task saves INDmoney's full response so future features need no task change; rare task changes use a one-click **Copy update message** instead of downloading anything; anonymous daily usage count.
- **1.2.0**: loans and cards listed one by one; assets-before-liabilities switch; ⓘ column notes; **+** on Other assets; each bank account's balance; summary flags big bank moves and card dues; update mode.
- **1.0.0**: first release.

## Changing it later

- **Add or remove a person**: update `config/setup.members` (the dashboard follows live) and update the task's prompt with the new member lines. Removing someone keeps their past rows.
- **Change the time**: update the task's schedule only.
- **Fix today's entry**: re-run the snapshot for today; past days can't be re-fetched.
- **Fixed copy (no automatic dashboard updates)**: if the user asks, republish the artifact's page with `assets/standalone.html` (self-contained, same features as this skill version) and merge `"fixed": true` into `config/setup`. In **Update an existing log**, when `fixed` is true, republish `assets/standalone.html` instead of the shell. To go back to automatic updates, publish the shell and set `"fixed": false`.
