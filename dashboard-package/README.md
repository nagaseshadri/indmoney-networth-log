# indmoney-networth-log (dashboard code)

The code behind the private dashboard created by the [INDmoney Net Worth Log](https://nagarajanseshadri.com/networth-log/) Claude skill.

Each user's dashboard is a small page in their own Claude account that loads `dist/dashboard.js` from jsDelivr (`indmoney-networth-log@1`), so improvements within version 1.x reach every dashboard automatically. The code only reads and displays the user's own logged data inside Claude; artifact pages can't send data to other sites.

Not affiliated with INDmoney or Anthropic. Not financial advice. MIT licensed.

**Publishing a release:** run `python3 build.py` at the repo root, bump `version` here (patch or minor for 1.x), then `npm publish` from this folder. jsDelivr picks up the new 1.x version, usually within a day.
