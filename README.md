# INDmoney Net Worth Log: a Claude skill

**Free · unofficial · read-only · not financial advice**

INDmoney shows your net worth as it is *right now*, but it keeps no day-by-day history. This Claude skill builds that history for you. Every morning it takes one snapshot from your INDmoney account, for you and for any family members who share their portfolio with you, and saves it to a private dashboard in your own Claude account.

## What you get

- **A private dashboard** with Family and per-person tabs, net worth on the latest day, change since the previous day and since the first log, assets and home loan.
- **A trend chart** of net worth over the days, with a tooltip for any day.
- **What moved**: which part of your net worth (mutual funds, bonds, Indian stocks, US stocks, NPS, savings, vehicle, other, home loan) changed the most.
- **A day-by-day ledger** of values as INDmoney reported them each morning.
- **Missed-day warnings**: the status line turns red if a morning wasn't logged, for example because your INDmoney sign-in expired.
- **A daily scheduled task** that runs in the cloud at 8:40 am IST, so your computer and phone can be off.

Why 8:40 am? It's before the 9:00 pre-open, so each entry is a clean end-of-day picture: Indian stocks at the previous close, mutual fund NAVs from the previous evening, and US stocks after their overnight close. Each entry describes the **previous trading day**.

## What you need

- A Claude account with **Skills** and **code execution** turned on
- The **official INDmoney connector** for Claude: `https://mcp.indmoney.com/mcp` (setup guide: [indmoney.com/mcp](https://www.indmoney.com/mcp))
- Claude features that let a dashboard keep its own data, and **scheduled tasks**. Availability can depend on your plan. If scheduled tasks aren't available, the skill still builds the dashboard and logs today, and tells you the daily run can't be scheduled.

## Install

1. Download `indmoney-networth-log.zip` from the [latest release](../../releases/latest).
2. In Claude, go to **Customize → Skills**, click **+**, then **Create skill → Upload a skill**, and choose the zip.
3. Connect INDmoney: **Settings → Connectors → Add custom connector**, paste `https://mcp.indmoney.com/mcp`, and sign in on INDmoney's own page.
4. In a new chat, say: **"Set up my INDmoney net worth log."**

Claude will ask which family members to include, publish your private dashboard, log today, and schedule the morning run.

To try it before committing to a daily run, say: *"Set up my INDmoney net worth log. This is a test: schedule the run once, 10 minutes from now, instead of daily."*

## Privacy

- Everything is created **in your own Claude account**, under **your own INDmoney sign-in**. Nothing is sent anywhere else.
- The INDmoney connector is **read-only**: no trades, no transfers, no changes to your account.
- The dashboard is **private to you** by default. Only you, the owner, can write to it, and the page itself never writes.

## Things to know

- **Missed days can't be filled in later.** INDmoney has no history, so if a morning's run fails (most often because the INDmoney sign-in expired), that day is lost. The run's summary starts with **ACTION NEEDED** when that happens. To hear about it the same day, turn on notifications for the task in its scheduled-task settings.
- **The trend line starts on day two.**
- **Changing it later**: ask Claude to add or remove a family member, or change the time. Removing someone keeps their past rows.

## What's in this repo

```
indmoney-networth-log/
├── SKILL.md                         # instructions Claude follows to set everything up
├── assets/dashboard.html            # the private dashboard page
└── references/daily-task-prompt.md  # template for the daily scheduled task
```

## Disclaimer

This is an independent, unofficial project. It is not affiliated with, endorsed by, or supported by INDmoney or Anthropic. It is a tracking tool, not financial advice. Figures are shown as INDmoney reports them and may differ from your statements.

## Author

**Nagarajan Seshadri**, an ecommerce technology consultant in Chennai
[nagarajanseshadri.com](https://nagarajanseshadri.com) · [LinkedIn](https://www.linkedin.com/in/nagarajanseshadri/)

Issues and suggestions are welcome. Open an issue in this repo.

## License

[MIT](LICENSE)
