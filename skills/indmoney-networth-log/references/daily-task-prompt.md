# Daily task prompt (template, task version 1.3.0)

Fill in the three placeholders, then use everything below the line as the scheduled task's prompt. Each run starts fresh with no memory, so the prompt must stand alone. The dashboard builds the same text for its "Copy update message" button, so keep the two in step (`build.py` copies this file into the dashboard code).

- `{{MEMBERS}}`: one line per person, e.g.
  `- the user (Asha): no family_member -> "days/<date>"`
  `- Ravi: family_member = "Ravi Kumar" -> "days_ravi/<date>"`
- `{{SLUG}}`: the dashboard artifact's slug
- `{{URL}}`: the dashboard's claude.ai link

---

Log today's net worth snapshots from INDmoney into the user's "Net worth log" dashboard. This is an unattended daily run; do not ask questions. (Task version 1.3.0)

MEMBERS (family_member argument -> document path):
{{MEMBERS}}

1. Load the tools with ToolSearch: the INDmoney tools networth_snapshot and networth_holdings, the artifact database tools db_get and db_write, and WebFetch. If the INDmoney tools are missing, or a call fails because INDmoney needs signing in again, write nothing and finish with exactly: "ACTION NEEDED: INDmoney needs you to sign in again (claude.ai connector settings). Today's net worth wasn't logged." Then stop.

2. For each member: call networth_snapshot, then networth_holdings with asset_type = "SA" (same family_member argument; none for the user). RETRIES: if a call fails for any reason other than sign-in (timeout, server error, empty or malformed result, total_networth missing), wait 60 seconds (run `sleep 60` in Bash) and try again, up to 3 attempts in all. If only networth_holdings keeps failing, still log that member without sa_accounts and raw.sa. If a family member's snapshot still fails, or they no longer share their portfolio, still log the others and say so in the summary. If the user's own snapshot fails after 3 attempts, say so in the summary starting with "ACTION NEEDED:".

3. From each successful snapshot, build one document (INR as returned; never estimate or invent a value):
   - date: today's date in Asia/Kolkata time, "YYYY-MM-DD"
   - captured_at: now, ISO 8601 with +05:30
   - source: "INDmoney networth_snapshot"
   - net_worth: total_networth
   - assets: total_current_value
   - invested: total_invested
   - liabilities: liabilities.total
   - home_loan: liabilities.total_loan_balance
   - credit_card_due: liabilities.total_credit_card_due
   - loans: liabilities.loans as [{"lender", "type": loan_type, "balance": current_balance}], [] if none
   - cards: liabilities.credit_cards as [{"name": name exactly as returned (masked), "due": total_due}], [] if none
   - mf, bond, stock, us_stock, nps, sa, vehicle: current_value of the investments rows with asset_type MF, BOND, STOCK, US_STOCK, NPS, SA, VEHICLE (0 if missing)
   - other: sum of current_value of every other asset_type, 0 if none
   - sa_accounts: from networth_holdings SA, [{"name": investment, "balance": market_value}]; if a bank name repeats, name the later ones "<bank> (2)", "<bank> (3)"
   - raw: {"snapshot": the investments, assets, market_cap and liabilities parts of the networth_snapshot result exactly as returned, "sa": the holdings list from networth_holdings exactly as returned}. This keeps everything INDmoney reported so future dashboard features can use it. Never add card numbers, account numbers or anything not in those results.

4. Dashboard slug: {{SLUG}}. For each path, db_get first. If it does not exist, db_write one op {op:"set", path, data}. If it exists, db_write {op:"set", path, data, ifVersion: <its version>} so that day's row is replaced, never duplicated. One db_write at a time. If a db_write fails with a transient error, wait 10 seconds and retry once (re-read the version first). Then db_get each path to confirm it saved with today's date. If a document would be over 200 KB, drop raw from it and say so in the summary. Write nothing else in the database.

5. Usage count (anonymous, never let it affect logging): WebFetch https://nagarajanseshadri.com/networth-log/version.json?v=1.3.0 once and ignore the result. If it fails, skip it silently. Send nothing else.

6. Finish with a one-line summary starting "Logged:", with the family total (sum of all members) in lakhs and each person's figure, e.g. "Logged: Family ₹68.22 L (Asha ₹60.66 L, Ravi ₹7.55 L)". If any bank account changed by more than ₹10,000 since the previous logged day (compare with that day's sa_accounts, if you read it), add a short note naming it and the change. If any credit card due is above ₹0, add a short note with the card and amount. Link: {{URL}}
