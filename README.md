# LinkLurker

**Still very much a work in progress**

**LinkLurker** is a minimalist, self-hosted tool designed to streamline the process of investigating potentially malicious domains. Whether you're analyzing suspicious links in phishing emails or reviewing security alerts, LinkLurker provides comprehensive details to help identify threats on a single, user-friendly page.

---

## Features

- **Blocklist Status**: Check if the domain is blocked by any known blocklists.
- **Domain Ownership**: Retrieve ownership details (if available).
- **Domain Age**: See how old the domain is.
- **Domain Update Timeline**:
  - Time since the domain was last updated.
  - Time until the domain expires.
- **DNS Records**: Display all DNS records associated with the domain.
- **Unicode Check**: Highlight any non-ASCII characters in the domain name.
- **Impersonation Detection**: Identify domains the current domain might be impersonating using string similarity analysis.
- **Integration with Security APIs** _(upcoming)_:
  - VirusTotal
  - AbuseIPDB
- **Blocklist Database**: Build a local database of blocked domains for easier future reference.

---

## Purpose

LinkLurker was created to serve as a one-stop tool for investigating domains quickly and efficiently. It simplifies the often tedious process of consolidating data from multiple sources, making it ideal for:

- **Security Analysts**: Investigate malicious domains in phishing emails and security alerts.
- **Incident Responders**: Quickly gather relevant information about suspicious URLs.
- **IT Teams**: Add an additional layer of security to your analysis workflows.

---
