# INDmoney Net Worth Log for Claude

A free Claude skill that keeps a **daily history of your net worth** from INDmoney, for you and any family members who share their portfolio with you, and charts how it moves.

INDmoney shows your net worth for today. This skill records it every morning, so after a few days you can see the trend, what moved it (mutual funds, stocks, bonds, loans…), and where to improve.

Made by [Nagarajan Seshadri](https://nagarajanseshadri.com). Install and update guide: [nagarajanseshadri.com/networth-log](https://nagarajanseshadri.com/networth-log/).

## What you get

- **A private dashboard** in your Claude account with:
  - a Family tab (everyone added together) and a tab per person
  - today's net worth, the change since the previous day and since the first log
  - a trend chart (point at any day to see its value)
  - **What moved:** how much each part (mutual funds, stocks, US stocks, bonds, savings, loans) added or took away
  - net worth with or without liabilities (one click to switch)
  - each loan and credit card listed separately
  - each bank account's balance and change, so you can see which one moved
  - a day-by-day table
  - a red warning if a day was missed
- **A daily scheduled task** that runs at 8:40 am IST in Anthropic's cloud. Your laptop and phone can be off. It retries temporary errors and tells you clearly when INDmoney needs you to sign in again.

## What you need

- A Claude plan that supports skills, artifacts and scheduled tasks
- The **INDmoney connector** connected in Claude
- To include family members: their portfolios shared with you in INDmoney's family feature

## Install

1. Download **indmoney-networth-log.zip**.
2. In Claude, open **Customize → Skills**, click **+**, choose **Upload a skill**, and select the zip.
3. Turn the skill on, then start a chat with: *"Set up my INDmoney net worth log."*

Claude will check your connection, ask which family members to include, build the dashboard, log today and schedule the morning run.

**Claude Code users** can add this repository as a plugin marketplace and install `indmoney-networth-log` from it.

## Updating

**Most updates need nothing from you.** Your dashboard loads its code from this project's published package, so improvements appear the next time you open it.

**On the rare occasion the morning task needs a change**, your dashboard shows a yellow banner with a **Copy update message** button. Click it, open a new chat in Claude, paste and press Enter. Claude updates your task in a minute; your history is kept. No downloads.

Using a version before 1.3? Do one last manual update: install the new zip (Plugins → Add → Upload plugin), then say *"Update my INDmoney net worth log."* After that, updates come to you.

## What's new

- **1.3.0**
  - The dashboard updates itself
  - The morning task saves everything INDmoney reports, so new features can use days already logged
  - Rare task changes: one click to copy, one paste into Claude
  - Anonymous daily usage count (see below)
- **1.2.0**: loans and cards listed one by one; net worth with or without liabilities; bank-by-bank balances; **+** and ⓘ details in the table; big-move and card-due notes in the morning summary; update mode
- **1.0.0**: first release

## Good to know

- **Entries describe the previous trading day.** The run happens before the 9:00 am pre-open, so stocks show the previous close and mutual funds the previous evening's NAV.
- **A missed day can't be filled in later.** INDmoney's connector only gives today's figures. If your INDmoney sign-in expires, sign in again the same day.
- **Turn on notifications** for the task (in its scheduled-task settings) so you hear about a failed day. Phone alerts need the Claude mobile app; email works without it.
- **Your data stays yours.** Everything is created in your own Claude account under your own INDmoney sign-in. Your figures are never sent to the author or anyone else. The dashboard is private unless you share it.
- **Anonymous usage count.** Each morning your task reads one public file on nagarajanseshadri.com, and that read is counted (per day and version only: no names, no figures, no IP addresses) so the author knows how many people use it.
- **The dashboard runs code from this project.** Its page loads the published package (`indmoney-networth-log@1` on npm, via jsDelivr). Dashboard pages can't send data to other sites.

## Disclaimer

This is an independent, free tool. It is **not affiliated with, endorsed by or supported by INDmoney or Anthropic**. It only records figures INDmoney reports and is **not financial advice**. Figures can be wrong if INDmoney's data is wrong; check important numbers in the INDmoney app. Provided as is, without warranty (see LICENSE).

## For maintainers

- `skills/indmoney-networth-log/`: the skill (SKILL.md, `references/daily-task-prompt.md`, `assets/dashboard.html` source, `assets/shell.html` page)
- `dashboard-package/`: the npm package each dashboard loads. Release: `python3 build.py`, bump `dashboard-package/package.json`, `npm publish` from that folder
- When the task prompt changes, bump `TASK_VERSION` in `dashboard.html` and the version in `daily-task-prompt.md`; dashboards then show the Copy update message banner

## License

MIT
