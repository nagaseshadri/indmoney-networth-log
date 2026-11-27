#!/usr/bin/env python3
"""Build the dashboard from one source.

Source:  skills/indmoney-networth-log/assets/dashboard.html  (self-contained, edit this)
         skills/indmoney-networth-log/references/daily-task-prompt.md (task template)
Outputs: dashboard-package/dist/dashboard.js   npm package file, loaded by every user's dashboard
         dashboard-package/dist/standalone.html self-contained copy (no CDN), for testing or fallback
         skills/indmoney-networth-log/assets/shell.html  the small page published as each user's dashboard
         skills/indmoney-networth-log/assets/standalone.html  fixed copy for users who opt out of auto-updates

Usage: python3 build.py   (then bump dashboard-package/package.json "version" and `npm publish`)
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
SKILL = ROOT / "skills" / "indmoney-networth-log"
SRC = SKILL / "assets" / "dashboard.html"
TPL = SKILL / "references" / "daily-task-prompt.md"
PKG = ROOT / "dashboard-package"
CDN = "https://cdn.jsdelivr.net/npm/indmoney-networth-log@1/dist/dashboard.js"


def task_template() -> str:
    text = TPL.read_text()
    parts = re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) != 2:
        raise SystemExit("daily-task-prompt.md needs a '---' line before the prompt")
    return parts[1].strip() + "\n"


def main() -> None:
    src = SRC.read_text()
    tpl = task_template()
    if '"__TASK_TEMPLATE__"' not in src:
        raise SystemExit("dashboard.html must contain const TASK_TEMPLATE = \"__TASK_TEMPLATE__\";")
    filled = src.replace('"__TASK_TEMPLATE__"', json.dumps(tpl, ensure_ascii=False).replace("</", "<\\/"))
    version = re.search(r'name="nwlog-version" content="([\d.]+)"', src).group(1)

    css = re.search(r"<style>\n(.*?)</style>", filled, re.S).group(1)
    body = re.search(r"<body>\n(.*?)<script>\n\{", filled, re.S).group(1)
    script = re.search(r"<script>\n\{\n(.*)\n\}\n</script>", filled, re.S).group(1)

    js = (
        f"/*! INDmoney Net Worth Log dashboard v{version} | MIT | https://nagarajanseshadri.com/networth-log/ */\n"
        "(function () {\n"
        "  var root = document.getElementById('nwlog-root');\n"
        "  if (!root || root.getAttribute('data-loaded')) return;\n"
        "  root.setAttribute('data-loaded', '1');\n"
        f"  window.NWLOG_VERSION = {json.dumps(version)};\n"
        f"  var css = {json.dumps(css)};\n"
        "  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);\n"
        f"  root.innerHTML = {json.dumps(body)};\n"
        "  {\n" + script + "\n  }\n"
        "})();\n"
    )
    (PKG / "dist").mkdir(parents=True, exist_ok=True)
    (PKG / "dist" / "dashboard.js").write_text(js)
    (PKG / "dist" / "standalone.html").write_text(filled)
    (SKILL / "assets" / "standalone.html").write_text(filled)

    shell = f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Net worth log</title>
<meta name="nwlog-shell" content="1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:light dark}}
body{{margin:0;font:16px/1.55 Manrope,system-ui,sans-serif;background:light-dark(#fff,#101418);color:light-dark(#101418,#eef1f4)}}
.nwlog-wait{{max-width:640px;margin:0 auto;padding:clamp(28px,6vw,64px) max(5vw,16px)}}
.nwlog-wait p{{margin:0 0 10px}}.nwlog-wait .muted{{color:light-dark(#56616b,#9aa6b1);font-size:14px}}
</style>
</head>
<body>
<div id="nwlog-root"><div class="nwlog-wait" id="nwlog-wait"><p>Loading your net worth log…</p></div></div>
<script>
{{
  // The dashboard's code is published as an npm package and served by jsDelivr, so every
  // dashboard picks up 1.x improvements automatically. Your data never leaves Claude.
  const src = {json.dumps(CDN)};
  const fail = () => {{
    const root = document.getElementById('nwlog-root');
    if (!root || root.getAttribute('data-loaded')) return;
    root.innerHTML = '<div class="nwlog-wait"><p><b>The dashboard couldn’t load.</b></p>' +
      '<p>Check your internet connection and refresh. Your logged days are safe: they are stored separately and the morning task keeps saving them.</p>' +
      '<p class="muted">If this keeps happening, see https://nagarajanseshadri.com/networth-log/</p></div>';
  }};
  const s = document.createElement('script');
  s.src = src; s.async = true; s.crossOrigin = 'anonymous';
  s.addEventListener('error', fail);
  document.body.appendChild(s);
  setTimeout(fail, 20000);
}}
</script>
</body>
</html>
"""
    (SKILL / "assets" / "shell.html").write_text(shell)
    print(f"built v{version}: dashboard.js {len(js)//1024} KB, standalone.html, shell.html")


if __name__ == "__main__":
    main()
