import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

DIAGNOSTIC_RULES = {
    404: {
        "status_title": "404 Not Found (Broken Page)",
        "client_impact": (
            "Users attempting to visit this link encounter a 'Page Not Found' error. "
            "If traffic is arriving from organic search or active marketing campaigns, "
            "conversions drop immediately and ad budget is wasted."
        ),
        "immediate_fix": "Deploy a 301 redirect to reroute users to the parent category or homepage.",
        "root_cause_fix": "Audit CMS slug update pipelines to ensure renamed URLs automatically generate redirect rules."
    },
    500: {
        "status_title": "500 Internal Server Error (System Crash)",
        "client_impact": (
            "The web server encountered an internal crash. Visitors cannot view or interact "
            "with this page, creating a complete disruption in user experience."
        ),
        "immediate_fix": "Restart the application worker process and inspect server error logs.",
        "root_cause_fix": "Add error boundary handling around unhandled exceptions and database connection timeouts."
    },
    200: {
        "status_title": "200 OK (Healthy)",
        "client_impact": "Page is fully operational and serving content normally to end users.",
        "immediate_fix": "None required.",
        "root_cause_fix": "Maintain standard uptime health-check intervals."
    }
}

class SiteHealthAgent:
    def __init__(self, client_name):
        self.client_name = client_name

    def audit_url(self, target_url):
        start_time = time.time()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = Request(target_url, headers=headers)
        
        try:
            with urlopen(req, timeout=10) as response:
                status_code = response.getcode()
        except HTTPError as e:
            status_code = e.code
        except Exception:
            status_code = 500

        latency_ms = round((time.time() - start_time) * 1000, 2)
        rules = DIAGNOSTIC_RULES.get(status_code, DIAGNOSTIC_RULES[500])

        return {
            "target_url": target_url,
            "http_status": status_code,
            "status_title": rules["status_title"],
            "latency_ms": f"{latency_ms}ms",
            "client_impact": rules["client_impact"],
            "immediate_fix": rules["immediate_fix"],
            "root_cause_fix": rules["root_cause_fix"]
        }

    def run(self, urls, output_filename="audit_report.txt"):
        banner = "=" * 70
        header_text = [
            banner,
            f"VIRTUAL NATION: SITE HEALTH & ROOT-CAUSE PROPOSER (CLUSTER D)",
            f"Account Target: {self.client_name}",
            banner
        ]
        
        # Print header to terminal
        print("\n" + "\n".join(header_text))

        report_lines = list(header_text)
        report_lines.append("")

        for idx, url in enumerate(urls, 1):
            res = self.audit_url(url)
            
            block = [
                f"[AUDIT RESULT #{idx}] URL: {res['target_url']}",
                f"Status: {res['status_title']} | Response Time: {res['latency_ms']}",
                "",
                "1. Client-Facing Impact Summary:",
                f"   {res['client_impact']}",
                "",
                "2. Technical Action Plan:",
                f"   * Hotfix:     {res['immediate_fix']}",
                f"   * Root Cause: {res['root_cause_fix']}",
                "-" * 70
            ]
            
            # Print to terminal
            print("\n" + "\n".join(block))
            
            # Add to file buffer
            report_lines.extend(block)
            report_lines.append("")

        # Save clean copy to file
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))
        
        print(f"\n[OK] Audit complete. Executive report saved to: {output_filename}\n")

if __name__ == "__main__":
    agent = SiteHealthAgent(client_name="Veycl / Sellable Marketing")
    test_urls = [
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404"
    ]
    agent.run(test_urls)