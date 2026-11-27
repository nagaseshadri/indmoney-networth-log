# INDmoney Net Worth Log: a Claude skill

**Free · unofficial · read-only · not financial advice**

INDmoney shows your net worth as it is *right now*, but it keeps no day-by-day history. This Claude skill builds that history for you. Every morning it takes one snapshot from your INDmoney account, for you and for any family members who share their portfolio with you, and saves it to a private dashboard in your own Claude account.

Install and update guide: [nagarajanseshadri.com/networth-log](https://nagarajanseshadri.com/networth-log/)

## What you get

- **A private dashboard** with Family and per-person tabs, net worth on the latest day, change since the previous day and since the first log, assets and liabilities.
- **A trend chart** of net worth over the days, with a tooltip for any day, and a switch to show assets **before liabilities**.
- **What moved**: which part of your net worth (mutual funds, bonds, Indian stocks, US stocks, NPS, savings, vehicle, other, loans, card dues) changed the most.
- **Loans and credit cards**, one by one, with what's owed and the change since the previous day.
- **Bank accounts**: each savings account's balance and change, so you can see which one moved.
- **A day-by-day ledger** of values as INDmoney reported them each morning, with **+** to expand "Other assets" and ⓘ notes on the columns.
- **Missed-day warnings**: the status line turns red if a morning wasn't logged, for example because your INDmoney sign-in expired.
- **A daily scheduled task** that runs in the cloud at 8:40 am IST, so your computer and phone can be off. Its summary flags big bank-balance moves and any credit card dues.
- **Updates that come to you**: the dashboard updates itself; rare task changes take one click and one paste.

Why 8:40 am? It's before the 9:00 pre-open, so each entry is a clean end-of-day picture: Indian stocks at the previous close, mutual fund NAVs from the previous evening, and US stocks after their overnight close. Each entry describes the **previous trading day**.

## What you need

- A Claude account with **Skills** and **code execution** turned on
- The **official INDmoney connector** for Claude: `https://mcp.indmoney.com/mcp` (setup guide: [indmoney.com/mcp](https://www.indmoney.com/mcp))
- Claude features that let a dashboard keep its own data, and **scheduled tasks**. Availability can depend on your plan. If scheduled tasks aren't available, the skill still builds the dashboard and logs today, and tells you the daily run can't be scheduled.

## Install

1. Download `indmoney-networth-log.zip` from the [latest release](../../releases/latest) (or from [nagarajanseshadri.com/networth-log](https://nagarajanseshadri.com/networth-log/)).
2. Add it to Claude. In the Claude app: **Plugins → Add → Upload plugin**. On the web: **Customize → Skills**, click **+**, then **Create skill → Upload a skill**. Choose the zip.
3. Connect INDmoney: **Settings → Connectors → Add custom connector**, paste `https://mcp.indmoney.com/mcp`, and sign in on INDmoney's own page.
4. In a new chat, say: **"Set up my INDmoney net worth log."**

Claude will ask which family members to include, publish your private dashboard, log today, and schedule the morning run.

To try it before committing to a daily run, say: *"Set up my INDmoney net worth log. This is a test: schedule the run once, 10 minutes from now, instead of daily."*

## Updating

**Installed before 1.3 (for example, from the first release)?** Do one last manual update:

1. Download the new `indmoney-networth-log.zip` from the [latest release](../../releases/latest).
2. Add it to Claude the same way as above. It replaces the old copy.
3. In a new chat, say: **"Update my INDmoney net worth log."** Claude updates your dashboard and morning task in place. Your logged history is kept and nothing is duplicated.

**From 1.3 on, updates come to you:**

- **Most updates need nothing.** Your dashboard loads its code from this project's published package (`indmoney-networth-log@1` on npm, via jsDelivr), so improvements appear the next time you open it.
- **Rarely, the morning task needs a change.** Your dashboard then shows a yellow **ONE STEP** banner with a **Copy update message** button. Click it, open a new chat in Claude, paste and press Enter.
- Prefer a dashboard that never changes on its own? Say *"Switch my net worth log dashboard to a fixed copy."*

## What's new

- **1.3.0**: the dashboard updates itself; the morning task saves everything INDmoney reports, so new features can use days already logged; rare task changes take one click and one paste; anonymous daily usage count.
- **1.2.0**: loans and credit cards listed one by one; net worth with or without liabilities; bank-by-bank balances; **+** and ⓘ details in the table; big-move and card-due notes in the morning summary; update mode.
- **1.0.0**: first release.

## Privacy

- Everything is created **in your own Claude account**, under **your own INDmoney sign-in**. Your figures are never sent anywhere else.
- The INDmoney connector is **read-only**: no trades, no transfers, no changes to your account.
- The dashboard is **private to you** by default. Only you, the owner, can write to it, and the page itself never writes.
- **Anonymous usage count:** each morning your task reads one small public file on nagarajanseshadri.com, and those reads are counted per day and version. No names, figures or IP addresses are kept.
- **The dashboard runs this project's code**, loaded from the published npm package. Dashboard pages in Claude can't send data to other websites.

## Things to know

- **Missed days can't be filled in later.** INDmoney has no history, so if a morning's run fails (most often because the INDmoney sign-in expired), that day is lost. The run's summary starts with **ACTION NEEDED** when that happens. To hear about it the same day, turn on notifications for the task in its scheduled-task settings.
- **The trend line starts on day two.**
- **Changing it later**: ask Claude to add or remove a family member, or change the time. Removing someone keeps their past rows.

## What's in this repo

```
skills/indmoney-networth-log/
├── SKILL.md                         # instructions Claude follows to set up or update everything
├── assets/shell.html                # the page each dashboard is published as (loads the package)
├── assets/dashboard.html            # dashboard source
├── assets/standalone.html           # self-contained build, for a fixed copy
└── references/daily-task-prompt.md  # template for the daily scheduled task
dashboard-package/                   # npm package every dashboard loads (dist/dashboard.js)
build.py                             # builds dashboard-package and the shell from the source
.claude-plugin/                      # plugin + marketplace files for Claude Code
```

**Releasing:** run `python3 build.py`, bump `dashboard-package/package.json`, `npm publish` from `dashboard-package/`, and attach the new skill zip to a GitHub release. When the task prompt changes, also bump `TASK_VERSION` in `assets/dashboard.html` and the version in `daily-task-prompt.md`.

## Disclaimer

This is an independent, unofficial project. It is not affiliated with, endorsed by, or supported by INDmoney or Anthropic. It is a tracking tool, not financial advice. Figures are shown as INDmoney reports them and may differ from your statements.

## Author

**Nagarajan Seshadri**, an ecommerce technology consultant in Chennai
[nagarajanseshadri.com](https://nagarajanseshadri.com) · [LinkedIn](https://www.linkedin.com/in/nagarajanseshadri/)

Issues and suggestions are welcome. Open an issue in this repo.

## License

[MIT](LICENSE)
