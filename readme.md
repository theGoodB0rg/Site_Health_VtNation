# Cluster D: Site Health & Root-Cause Proposer

A lightweight, zero-dependency diagnostic agent designed for Virtual Nation to monitor site health across Veycl, Sellable Marketing, and client domains.

Rather than outputting raw, cryptic HTTP error codes, the agent automatically translates detected breakages into two operational streams:
1. **Executive Impact Summary:** Plain-English business context explaining how an issue affects user conversion, ad spend, and brand reputation (written for non-technical stakeholders and clients).
2. **Actionable Remediation Plan:** Immediate hotfix guidance and permanent root-cause prevention steps (written for development teams).

---

## Key Features

* **Zero External Dependencies:** Built entirely with the Python Standard Library (`urllib`, `time`). Runs out of the box on Python 3 without requiring `pip install` or virtual environments.
* **Dual Output Mode:** Streams real-time diagnostic logs directly to the terminal while simultaneously generating a clean executive summary in `audit_report.txt`.
* **1-Click Execution (Windows):** Includes a `run_site_audit.bat` launcher that executes the audit, keeps the terminal open for inspection, and automatically displays the generated report in Notepad.
* **Deterministic & Cost-Efficient:** Eliminates unnecessary third-party LLM latency and API token costs on standard HTTP status inspections (<1500ms response cycles).
* **Multi-Client Parameterization:** Accepts target configurations by client account name and endpoints for rapid scaling without rebuilding workflows.

---

## Requirements / Python Dependencies

No third-party packages required.

* **Python:** 3.8+ (tested on Python 3.12.9 on Windows)
* **Standard library only:**
  * `time` – response-time measurement
  * `urllib.request` (`Request`, `urlopen`) – HTTP checks
  * `urllib.error` (`HTTPError`, `URLError`) – error handling
* **OS:** Windows, macOS, or Linux. Windows includes a 1-click `.bat` launcher; macOS/Linux use `python3`.

Verify your setup:

```bash
python --version
# Windows: Python 3.8+ expected
# macOS/Linux: python3 --version
```

No `pip install`, no `requirements.txt`, no virtualenv needed. If Python is installed, you can run this project.

Optional: if `python` is not on your PATH on Windows, install from [python.org](https://www.python.org/downloads/) and check “Add python.exe to PATH” during setup.

---

## How to Clone

```bash
# Clone the repository (replace with your actual repo URL)
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
```

Example once published:

```bash
git clone https://github.com/theGoodB0rg/Site_Health_VtNation.git
cd Site_Health_VtNation
```

No install step after cloning – just run it (see below).

---

## How to Use

### Option 1: Windows 1-Click (easiest)

1. Double-click `run_site_audit.bat`.
2. A terminal window runs the audit live.
3. When finished, `audit_report.txt` opens automatically in Notepad.
4. Press any key to close the terminal.

What the batch file does:

```bat
python Site_Health_Agent.py
start audit_report.txt
pause
```

> Note: if you have both `python` and `py` launchers, either works. If `python` is not recognized, try `py Site_Health_Agent.py`.

### Option 2: Command line (Windows / macOS / Linux)

Windows (PowerShell / CMD):

```bash
python Site_Health_Agent.py
```

macOS / Linux:

```bash
python3 Site_Health_Agent.py
```

Output goes to:
* Terminal (live logs)
* `audit_report.txt` (clean executive report, overwritten on each run)

### Option 3: Just view the last report (no run needed)

Open `audit_report.txt` in Notepad / any text editor. No Python required for this.

See also `HOW_TO_USE.txt` for a non-technical walkthrough for clients and account managers.

### Customize target URLs

Edit the bottom of `Site_Health_Agent.py`:

```python
if __name__ == "__main__":
    agent = SiteHealthAgent(client_name="Veycl / Sellable Marketing")
    test_urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404"
    ]
    agent.run(test_urls)
```

Replace `test_urls` with any client domains you want to audit, e.g.:

```python
test_urls = [
    "https://veycl.com/",
    "https://sellablemarketing.com/",
    "https://client-site.com/pricing",
]
```

Then re-run. You can also reuse the class in your own code:

```python
from Site_Health_Agent import SiteHealthAgent

agent = SiteHealthAgent(client_name="Acme Corp")
agent.run(["https://example.com/"], output_filename="acme_report.txt")
```

---

## File Structure

```text
├── Site_Health_Agent.py   # Core audit engine and diagnostic rules
├── run_site_audit.bat     # 1-click Windows launcher (terminal + Notepad popup)
├── audit_report.txt       # Auto-generated clean executive report (overwritten each run)
├── HOW_TO_USE.txt         # Non-technical guide for clients / account managers
└── readme.md              # Project documentation and usage guide
```

---

## Example Output (`audit_report.txt`)

```text
======================================================================
VIRTUAL NATION: SITE HEALTH & ROOT-CAUSE PROPOSER (CLUSTER D)
Account Target: Veycl / Sellable Marketing
======================================================================

[AUDIT RESULT #1] URL: https://httpbin.org/status/200
Status: 200 OK (Healthy) | Response Time: 2506.02ms

1. Client-Facing Impact Summary:
   Page is fully operational and serving content normally to end users.

2. Technical Action Plan:
   * Hotfix:     None required.
   * Root Cause: Maintain standard uptime health-check intervals.
----------------------------------------------------------------------
```

Each URL produces:
1. **Client-Facing Impact Summary** – business impact in plain English.
2. **Technical Action Plan** – `Hotfix` (immediate) + `Root Cause` (permanent fix).

Currently handled status codes: `200 OK`, `404 Not Found`, `500 Internal Server Error` (fallback for timeouts / DNS / unknown codes). Extend `DIAGNOSTIC_RULES` in `Site_Health_Agent.py` to add more.

---

## Troubleshooting

* `'python' is not recognized` (Windows): reinstall Python with “Add to PATH”, or use `py Site_Health_Agent.py`.
* `python3 not found` (Windows): use `python` instead – `python3` is macOS/Linux convention.
* No internet / slow sites: requests time out after 10s and are reported as 500-class errors by design.
* Report not updating: ensure you have write permission in the folder; `audit_report.txt` is overwritten each run.

---

Prepared by: John Olorunfemi
Email: theregalstarlite@gmail.com
