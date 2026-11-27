---
name: indmoney-networth-log
description: Set up a daily net worth log from INDmoney, for you and any family members who share their portfolio, with a private dashboard (per-person and family tabs, trend chart, what moved, missed-day warnings) and a scheduled task that records a snapshot every morning. Use when someone asks to track, log or chart their INDmoney net worth over time.
---

# INDmoney net worth log

INDmoney's connector only returns net worth **as of now**; it keeps no daily history. This skill builds the history: one snapshot per person per morning, saved to a private dashboard in the user's own Claude account.

Everything is created in the user's account, under their own INDmoney sign-in. Nothing is sent anywhere else. This is a tracking tool, not financial advice; say so once at hand-over.

## What you need in this session

Check silently before starting. If something is missing, say what in one line and stop.

- **INDmoney connector**: `networth_snapshot` and `get_family_members` (tool names may carry a prefix, e.g. `mcp__INDMoney__networth_snapshot`; load deferred tools with ToolSearch). If it reports a sign-in problem, ask the user to reconnect INDmoney in their Claude connector settings, then continue once they confirm.
- **Artifact tool with a database**: something that can publish an HTML page as an artifact, declare the `db` and `user` capabilities, and write documents to its database (e.g. `publish_files` / `publish_version`, `declare_capabilities`, `db_get`, `db_write`). If artifacts can't hold a database here, say so and stop.
- **Scheduling tool** that creates a recurring cloud task (e.g. `create_trigger`). If none, you can still build the dashboard and log today, and tell the user the daily run can't be scheduled from this session.

## Steps

### 1. Find the people

Call `get_family_members`. Keep members with `sharing_portfolio: true`. The user is the one with `is_you: true`.

If there is more than one sharing member, ask once (multiple choice if you can) which to include. Default: everyone who shares. Members who don't share can't be logged; mention them only if the user asks about someone missing.

Give each included person:
- `id`: lowercase ASCII slug of their first name (`a-z`, `0-9`, `-`; never `family`); the user is `me`
- `label`: their first name as INDmoney lists it
- `collection`: `days` for the user, `days_<id>` for others (letters, digits, `_`, `-` only)
- `indmoney_name`: their exact `name` from `get_family_members` (omit for the user)

### 2. Publish the dashboard

Publish `assets/dashboard.html` (in this skill's folder) unchanged as a new artifact titled **Net worth log** (icon: chart). Then declare its capabilities as exactly:

```json
{"db": {"rules": [{"path": "", "read": "view", "write": "owner"}]}, "user": {}}
```

Only the owner can write; the page itself never writes. Keep the artifact's slug and URL.

### 3. Save the setup

Write one document, `config/setup`:

```json
{"members": [
  {"id": "me", "label": "<user's first name>", "collection": "days"},
  {"id": "<id>", "label": "<first name>", "collection": "days_<id>", "indmoney_name": "<exact INDmoney name>"}
], "time": "08:40 Asia/Kolkata", "created": "<today YYYY-MM-DD>"}
```

### 4. Log today

For each person call `networth_snapshot` (the user with no arguments; others with `family_member` = their `indmoney_name`). Build each day's document with the mapping below and write it to `<collection>/<YYYY-MM-DD>` (today's date in Asia/Kolkata), using a `set`. Read it back with `db_get` to confirm.

**Document mapping** (INR as returned; never estimate, round or invent a value):

| Field | From `networth_snapshot` |
|---|---|
| `date` | today, `YYYY-MM-DD`, Asia/Kolkata |
| `captured_at` | now, ISO 8601 with `+05:30` |
| `source` | `"INDmoney networth_snapshot"` |
| `net_worth` | `total_networth` |
| `assets` | `total_current_value` |
| `invested` | `total_invested` |
| `liabilities` | `liabilities.total` |
| `home_loan` | `liabilities.total_loan_balance` (all loans) |
| `credit_card_due` | `liabilities.total_credit_card_due` |
| `mf`, `bond`, `stock`, `us_stock`, `nps`, `sa`, `vehicle` | `current_value` of `investments` rows with `asset_type` MF, BOND, STOCK, US_STOCK, NPS, SA, VEHICLE |
| `other` | sum of `current_value` of every other `asset_type` (US_STOCK_WALLET, CRYPTO, FD, EPF, PPF, GOLD, …), 0 if none |

Missing asset types are 0.

### 5. Schedule the morning run

Default time is **8:40 am IST daily** (`CRON_TZ=Asia/Kolkata 40 8 * * *`): before the 9:00 pre-open, so each entry is a clean end-of-day picture (Indian stocks at the previous close, mutual fund NAVs from the previous evening, US stocks after their overnight close). Each entry therefore describes the **previous trading day**. Use another time only if the user asks.

Create the recurring task named **Daily net worth log** with the prompt in `references/daily-task-prompt.md`, filling in the artifact slug, URL and the member list. It runs in the cloud; the user's computer and phone can be off.

### 6. Hand over

In a few lines:
- the dashboard link (or say the card is above), with today's figure per person and the family total
- the trend line starts after tomorrow's run; entries describe the previous trading day
- INDmoney sign-ins can expire; that day can't be logged and can't be filled in later, because INDmoney has no history. The run's summary starts with **ACTION NEEDED** when that happens, and the dashboard's status line turns red
- to hear about failures the same day: turn on notifications for the task (phone alerts need the Claude mobile app; email works without it) in its scheduled-task settings
- this is a tracking tool, not financial advice

## Changing it later

- **Add or remove a person**: update `config/setup` (the dashboard picks it up live) and update the scheduled task's prompt with the new member list. Removing someone keeps their past rows.
- **Change the time**: update the task's schedule only.
- **Fix a bad day**: re-run the snapshot for today only; past days can't be re-fetched.
