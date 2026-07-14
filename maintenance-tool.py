#!/usr/bin/env python3
"""
Casbeghen Stack Maintenance Tool — Quadlet Era
Checks all 12 services, podman resources, logs, SSL.
Suggests actions, executes them interactively.
One tool. Python. No bash wrappers.
"""

import subprocess, json, sys, os, re
from datetime import datetime, timedelta
from pathlib import Path

# ── Configuration ──
SERVICES = [
    "postgres", "opensearch-node1", "opensearch-node2", "opensearch-dashboards",
    "rules-engine", "n8n", "twenty-redis", "twenty-api", "twenty-worker",
    "listmonk", "email-sender", "astro",
]

IMAGES = {
    "postgres": {"local": "localhost/oci-postgres", "dockerfile": "build-images/oci-postgres"},
    "astro": {"local": "localhost/oci-astro-site", "dockerfile": "stacks/casbeghen.com/astro"},
    "rules-engine": {"local": "localhost/oci-rules-engine", "dockerfile": "stacks/casbeghen.com/rules-engine"},
    "email-sender": {"local": "localhost/oci-oci-email-sender", "dockerfile": "build-images/oci-email-sender"},
    "whatsapp": {"local": "localhost/oci-whatsapp", "dockerfile": "build-images/oci-whatsapp"},
}

# ── Helpers ──
def run(cmd, check=False):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return r.stdout.strip()
    except:
        return None

def green(s): return f"\033[92m{s}\033[0m"
def red(s): return f"\033[91m{s}\033[0m"
def yellow(s): return f"\033[93m{s}\033[0m"
def bold(s): return f"\033[1m{s}\033[0m"
def confirm(p): return input(f"  {p} [y/N]: ").strip().lower() in ('y','yes')

# ── Checks ──
def check_services():
    print(bold("\n🔍 SERVICE HEALTH"))
    print("─" * 60)
    ok = True
    for svc in SERVICES:
        status = run(f"systemctl --user is-active {svc}.service 2>/dev/null")
        if status == "active": print(f"  {green('✅')} {svc}")
        else:
            print(f"  {red('❌')} {svc} ({status or 'not found'})")
            ok = False
    return ok

def check_resources():
    print(bold("\n📦 PODMAN RESOURCES"))
    print("─" * 60)
    dangling = run("podman images -f 'dangling=true' --format '{{.ID}}'")
    count = len(dangling.splitlines()) if dangling else 0
    print(f"  {'⚠️' if count else '✅'} Dangling images: {count}")
    disk = run("du -sh /home/opc/.local/share/containers/storage 2>/dev/null")
    if disk: print(f"  📊 Podman storage: {disk.split()[0]}")

def check_logs():
    print(bold("\n📋 RECENT ERRORS (last 24h)"))
    print("─" * 60)
    since = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M")
    for svc in SERVICES:
        logs = run(f"journalctl --user -u {svc}.service --since '{since}' --no-pager -p err 2>/dev/null | tail -3")
        if logs and logs.strip():
            print(f"  {red('❌')} {svc}:")
            for line in logs.splitlines(): print(f"      {line[:120]}")

def check_ssl():
    print(bold("\n🔒 SSL"))
    print("─" * 60)
    expiry = run("echo | openssl s_client -connect casbeghen.com:443 -servername casbeghen.com 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null")
    if expiry: print(f"  📅 casbeghen.com expires: {expiry.replace('notAfter=', '')}")
    else: print(f"  {yellow('⚠️')} Could not check")

# ── Actions ──
def prune_images():
    if confirm("Remove all dangling images?"):
        run("podman image prune -f")
        print(f"  {green('✅')} Done")

def restart_service(svc):
    if confirm(f"Restart {svc}?"):
        run(f"systemctl --user restart {svc}.service")
        print(f"  {green('✅')} {svc} restarted")

def build_image(name):
    info = IMAGES.get(name)
    if not info: return
    path = f"/home/opc/{info['dockerfile']}"
    tag = info['local']
    print(f"  🔨 Building {tag}...")
    r = run(f"podman build -t {tag}:latest {path}")
    print(f"  {green('✅')} Built" if r is not None else f"  {red('❌')} Failed")

# ── Main ──
def main():
    print(bold("=" * 60))
    print(bold("  CASBEGHEN STACK MAINTENANCE"))
    print(bold(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}"))
    print(bold("=" * 60))
    
    ok = check_services()
    check_resources()
    check_logs()
    check_ssl()
    
    print(bold("\n🔧 ACTIONS"))
    print("─" * 60)
    
    if confirm("Prune dangling images?"): prune_images()
    
    for svc in SERVICES:
        status = run(f"systemctl --user is-active {svc}.service 2>/dev/null")
        if status != "active": restart_service(svc)
    
    if confirm("Rebuild all custom images?"):
        for name in IMAGES: build_image(name)
    
    print(bold(f"\n✅ MAINTENANCE COMPLETE — Services: {'ALL GREEN' if ok else 'NEEDS ATTENTION'}"))

if __name__ == "__main__":
    main()
