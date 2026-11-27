# Daily task prompt (template)

Fill in `{{SLUG}}`, `{{URL}}` and the MEMBERS block, then use the whole text below the line as the scheduled task's prompt. Each run starts fresh with no memory, so the prompt must stand alone.

---

Log today's net worth snapshots from INDmoney into the user's "Net worth log" artifact. This is an unattended daily run; do not ask questions.

MEMBERS (call -> document path):
- the user: networth_snapshot with no arguments -> "days/<date>"
- {{Label}}: networth_snapshot with family_member = "{{exact INDmoney name}}" -> "days_{{id}}/<date>"
(repeat the second line for each family member; remove it if only the user is logged)

1. Load the tools with ToolSearch: the INDmoney `networth_snapshot` tool and the artifact database tools `db_get` and `db_write`. If the INDmoney tools are missing, or a call fails because INDmoney needs signing in again, write nothing and finish with exactly: "ACTION NEEDED: INDmoney needs you to sign in again (claude.ai connector settings). Today's net worth wasn't logged." Then stop.

2. Call networth_snapshot once per member as listed. RETRIES: if a call fails for any reason other than sign-in (timeout, server error, empty or malformed result, total_networth missing), wait 60 seconds (run `sleep 60` in Bash) and try again, up to 3 attempts in all. If a family member's call still fails, or they no longer share their portfolio, still log the others and say so in the summary. If the user's own call fails after 3 attempts, say so in the summary starting with "ACTION NEEDED:".

3. From each successful result, build one document (all numbers in INR, as returned; never estimate or invent a value):
   - date: today's date in Asia/Kolkata time, "YYYY-MM-DD"
   - captured_at: the current time, ISO 8601 with +05:30
   - source: "INDmoney networth_snapshot"
   - net_worth: total_networth
   - assets: total_current_value
   - invested: total_invested
   - liabilities: liabilities.total
   - home_loan: liabilities.total_loan_balance
   - credit_card_due: liabilities.total_credit_card_due
   - from the investments list, by asset_type, its current_value: mf = MF, bond = BOND, stock = STOCK, us_stock = US_STOCK, nps = NPS, sa = SA, vehicle = VEHICLE
   - other: the sum of current_value of every other asset_type in investments (e.g. US_STOCK_WALLET, CRYPTO, FD, EPF, PPF, GOLD), 0 if none
   Missing asset types are 0.

4. Artifact slug: {{SLUG}}. For each path, call db_get first. If it does not exist, db_write one op {op:"set", path, data}. If it exists, db_write {op:"set", path, data, ifVersion: <its version>} so that day's row is replaced, never duplicated. Send one db_write at a time. If a db_write fails with a transient error, wait 10 seconds and retry once (re-read the version first). Then db_get each path to confirm it saved with today's date. Write nothing else in the database.

5. Finish with a one-line summary starting "Logged:", with the family total (sum of all members) in lakhs and each person's figure, e.g. "Logged: Family ₹88.68 L (Asha ₹80.94 L, Ravi ₹7.74 L)". Link: {{URL}}
