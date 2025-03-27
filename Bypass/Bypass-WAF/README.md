# 🔍 Bypass-WAF

**Bypass-WAF** is a Bash tool designed to help you discover real origin IP addresses behind services protected by WAFs (Web Application Firewalls) like Cloudflare, Akamai, Imperva, etc.

It combines public sources like `dnshistory.org` with APIs like Shodan, Censys, and SecurityTrails to retrieve historical A records, then performs active HTTPS connectivity checks by IP using a manipulated `Host` header.

---

## 🚀 Features

- 🔎 Fetches historical A records (DNS history)
- 🔐 Optional API queries to:
  - [Shodan](https://www.shodan.io/)
  - [Censys](https://search.censys.io/)
  - [SecurityTrails](https://securitytrails.com/)
- 💥 Automatic WAF detection via `whois`
- ⚡ Fast, parallel HTTPS scanning by IP
- 📊 Final report with reachable, ignored (WAF), and unresponsive IPs
- ✅ Supports `verbose` mode

---

## 📦 Requirements

- `curl`
- `grep`, `cut`, `sort`, `xargs`, `whois`
- GNU `bash`
- Internet connection 😄

---

## 🛠 Usage

```bash
./bypass-waf.sh -d 'example.com' [options]
```

### Available options:

| Option                     | Description                                           |
|---------------------------|-------------------------------------------------------|
| `-d, --domain`            | Target domain **(required)**                         |
| `-s, --shodan-api`        | Shodan API key (optional)                            |
| `-c, --censys-api`        | Censys API key in format `UID:SECRET` (optional)     |
| `-t, --security-trails`   | SecurityTrails API key (optional)                    |
| `-v, --verbose`           | Show detailed output for ignored/unreachable IPs     |
| `-h, --help`              | Show this help message                               |

---

## 🧪 Usage Examples

### Basic scan using only DNS history:
```bash
./bypass-waf.sh -d 'vulnerable.site'
```

### Including Shodan, SecurityTrails and Censys:
```bash
./bypass-waf.sh -d 'vulnerable.site' -s 'SHODAN_API_KEY' -t 'SECURITYTRAILS_API_KEY' -c 'UID:SECRET'
```

### Verbose mode:
```bash
./bypass-waf.sh -d 'vulnerable.site' -v
```

---

## 📤 Output

Once finished, you'll see something like:

```bash
[*] Fetching historical A records for: vulnerable.site
[*] Querying Shodan...
[*] Querying Censys...
[*] Querying SecurityTrails...
[*] Checking direct HTTPS access to IPs (parallel)…
[+] Possible origin IP: 10.10.10.10

[*] Scan completed.
[*] Total IPs checked: 77
[+] Reachable: 1
[!] Ignored (Akamai): 69
[-] Unresponsive: 7
```

These results indicate how many IPs seem **directly reachable** via HTTPS using the `Host: domain` header, which may suggest access to the actual backend server.

---

## 🧠 How It Works

1. 🔎 **Fetches historical IPs** from `dnshistory.org`
2. 🛰️ **Optionally enriches results** using external APIs
3. 🔍 **Identifies WAF-owned IPs** via `whois`
4. 🌐 **Performs active HTTPS requests** to each IP with `Host` header set
5. 📊 **Categorizes results** as reachable, WAF-owned or unresponsive

---

## ❗ Disclaimer

> **This script is for educational purposes and authorized auditing only.**  
> Use it only on domains you own or have explicit permission to test.

---

Hack responsibly! 🔐
