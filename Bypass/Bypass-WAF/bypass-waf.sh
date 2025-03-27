#!/bin/bash

# Colors
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
RESET="\e[0m"

# ASCII Banner
echo -e "${YELLOW}"
cat << "EOF"
 __       __        __   __                ___ 
|__) \ / |__)  /\  /__` /__` __ |  |  /\  |__  
|__)  |  |    /~~\ .__/ .__/    |/\| /~~\ |    
                                               
    Written by: x4v1l0k   -   Version: 1.0
EOF
echo -e "${RESET}"

print_help() {
    echo -e "${BLUE}Usage:${RESET} $0 [options]"
    echo -e "${BLUE}Options:${RESET}"
    echo -e "  -d, --domain             Target domain (required)"
    echo -e "  -s, --shodan-api         Shodan API key (optional)"
    echo -e "  -c, --censys-api         Censys API key (optional, format: USER:SECRET)"
    echo -e "  -t, --security-trails    SecurityTrails API key (optional)"
    echo -e "  -v, --verbose            Show all tests"
    echo -e "  -h, --help               Show this help message"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -d|--domain)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo -e "${RED}[!] Missing value for --domain${RESET}"
                exit 1
            fi
            domain="$2"
            shift 2
            ;;
        -s|--shodan-api)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo -e "${RED}[!] Missing value for --shodan-api${RESET}"
                exit 1
            fi
            shodan_key="$2"
            shift 2
            ;;
        -c|--censys-api)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo -e "${RED}[!] Missing value for --censys-api${RESET}"
                exit 1
            fi
            censys_key="$2"
            shift 2
            ;;
        -t|--security-trails)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo -e "${RED}[!] Missing value for --security-trails${RESET}"
                exit 1
            fi
            trails_key="$2"
            shift 2
            ;;
        -v|--verbose)
            verbose_mode=true
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}[!] Unknown option: $1${RESET}"
            print_help
            exit 1
            ;;
    esac
done

if [ -z "$domain" ]; then
    echo -e "${RED}[!] You must provide a domain with -d or --domain${RESET}"
    print_help
    exit 1
fi

# TMPs
tmpdir=$(mktemp -d)
ignored_file="$tmpdir/ignored.txt"
unresponsive_file="$tmpdir/unresponsive.txt"
valid_file="$tmpdir/valid.txt"
all_ips_file="$tmpdir/all_ips.txt"

# Init result files
touch "$ignored_file" "$valid_file" "$unresponsive_file" "$all_ips_file"

echo -e "${BLUE}[*] Fetching historical A records for: $domain${RESET}"

# DNS history
curl -k -s "https://dnshistory.org/historical-dns-records/a/$domain" \
    | grep -Eo '[0-9]{1,3}(\.[0-9]{1,3}){3}' >> "$all_ips_file"

# SHODAN
if [ -n "$shodan_key" ]; then
    echo -e "${BLUE}[*] Querying Shodan...${RESET}"
    while read -r ip; do
        response=$(curl -s "https://api.shodan.io/shodan/host/$ip?key=$shodan_key")
        if echo "$response" | grep -qi "$domain"; then
            echo -e "${GREEN}[+] Shodan match: $ip${RESET}"
            echo "$ip" >> "$all_ips_file"
        fi
    done < <(sort -u "$all_ips_file")
fi

# CENSYS
if [ -n "$censys_key" ]; then
    echo -e "${BLUE}[*] Querying Censys...${RESET}"
    while read -r ip; do
        auth=$(echo -n "$censys_key" | base64)
        response=$(curl -s "https://search.censys.io/api/v2/hosts/$ip" -H "Authorization: Basic $auth")
        if echo "$response" | grep -qi "$domain"; then
            echo -e "${GREEN}[+] Censys match: $ip${RESET}"
            echo "$ip" >> "$all_ips_file"
        fi
    done < <(sort -u "$all_ips_file")
fi

# SECURITYTRAILS
if [ -n "$trails_key" ]; then
    echo -e "${BLUE}[*] Querying SecurityTrails...${RESET}"
    response=$(curl -s -H "APIKEY: $trails_key" "https://api.securitytrails.com/v1/history/$domain/dns/a")
    echo "$response" | grep -oE '"ip":"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"' \
        | cut -d'"' -f4 >> "$all_ips_file"
fi

# Function to detect WAF via WHOIS
is_known_waf() {
    local ip="$1"
    local whois_data
    whois_data=$(whois "$ip")

    declare -A waf_patterns=(
        ["Cloudflare"]="Cloudflare"
        ["Akamai"]="akamai"
        ["Sucuri"]="Sucuri"
        ["Imperva"]="Incapsula"
        ["Fastly"]="Fastly"
        ["StackPath"]="StackPath"
    )

    for waf in "${!waf_patterns[@]}"; do
        if echo "$whois_data" | grep -iq "${waf_patterns[$waf]}"; then
            echo "$waf"
            return 0
        fi
    done

    return 1
}

# Function to analyze an IP
check_ip() {
    ip="$1"

    waf_name=$(is_known_waf "$ip")
    if [ -n "$waf_name" ]; then
        if [ -n "$verbose_mode" ]; then
            echo -e "${YELLOW}[!] Ignoring $waf_name IP: $ip${RESET}" >&2
        fi
        echo "$ip" >> "$ignored_file"
        return
    fi

    if curl -k -I -s --connect-timeout 10 --max-time 15 "https://$ip" -H "Host: $domain" > /dev/null; then
        echo -e "${GREEN}[+] Possible origin IP: $ip${RESET}"
        echo "$ip" >> "$valid_file"
    else
        if [ -n "$verbose_mode" ]; then
            echo -e "${RED}[-] Unresponsive IP: $ip${RESET}" >&2
        fi
        echo "$ip" >> "$unresponsive_file"
    fi
}

export -f check_ip is_known_waf
export domain RED GREEN YELLOW BLUE RESET valid_file ignored_file unresponsive_file verbose_mode

echo -e "${BLUE}[*] Checking direct HTTPS access to IPs (parallel)...${RESET}"

sort -u "$all_ips_file" | xargs -P 10 -I{} bash -c 'check_ip "$@"' _ {}

# Counters
total=$(sort -u "$all_ips_file" | wc -l)
valid=$(wc -l < "$valid_file")
ignored=$(wc -l < "$ignored_file")
unresponsive=$(wc -l < "$unresponsive_file")

echo -e "\n${BLUE}[*] Scan completed.${RESET}"
echo -e "${BLUE}[*] Total IPs checked:${RESET} $total"
echo -e "${GREEN}[+] Reachable:${RESET} $valid"
echo -e "${YELLOW}[!] Ignored (WAF):${RESET} $ignored"
echo -e "${RED}[-] Unresponsive:${RESET} $unresponsive"

rm -rf "$tmpdir"
