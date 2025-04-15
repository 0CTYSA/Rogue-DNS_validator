import dns.resolver
import requests
import difflib
import os
from datetime import datetime

TRUSTED_DNS_SERVERS = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
REPORTS_DIR = "reports"
TIMEOUT = 5

def create_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)

def save_to_txt(filename, data):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")

def resolve_domain(domain, dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    try:
        answers = resolver.resolve(domain, 'A')
        return [answer.address for answer in answers]
    except Exception:
        return None

def get_http_diff(domain, malicious_ip):
    try:
        legit = requests.get(f"https://{domain}", timeout=TIMEOUT, verify=False).text
        fake = requests.get(f"http://{malicious_ip}", headers={"Host": domain}, timeout=TIMEOUT, verify=False).text
        
        # Solo comparamos líneas clave que contengan:
        keywords = ["<form", "action=", "login", "password", "submit"]
        legit_lines = [line for line in legit.splitlines() if any(kw in line.lower() for kw in keywords)]
        fake_lines = [line for line in fake.splitlines() if any(kw in line.lower() for kw in keywords)]
        
        return "\n".join(difflib.unified_diff(
            legit_lines,
            fake_lines,
            fromfile="LEGITIMO",
            tofile="FRAUDULENTO",
            lineterm=""
        ))
    except Exception as e:
        return f"Error en comparación: {str(e)}"

def analyze_domain(domain, rogue_dns, report_filename):
    result = []
    
    # Resolución DNS
    rogue_ips = resolve_domain(domain, rogue_dns)
    if not rogue_ips:
        return None

    result.append(f"\n{'='*50}")
    result.append(f"[*] DOMINIO: {domain}")
    result.append(f"{'='*50}")
    result.append(f"[+] DNS SOSPECHOSO ({rogue_dns}):")
    result.append(f"    → IP: {', '.join(rogue_ips)}\n")
    result.append("[+] COMPARACIÓN CON DNS CONFIABLES:")

    discrepancies = False
    for trusted_server in TRUSTED_DNS_SERVERS:
        trusted_ips = resolve_domain(domain, trusted_server)
        if trusted_ips:
            result.append(f"  - {trusted_server}: {', '.join(trusted_ips)}")
            if rogue_ips != trusted_ips:
                discrepancies = True

    # Solo si hay discrepancia DNS
    if discrepancies:
        result.append("\n[!] CONCLUSIÓN: POSIBLE PHARMING (IPs diferentes)")
        
        # Comandos DIG
        result.append("\n[+] COMANDOS DIG PARA VERIFICACIÓN MANUAL:")
        result.append(f"  - DNS sospechoso: dig {domain} @{rogue_dns} +short")
        for server in TRUSTED_DNS_SERVERS:
            result.append(f"  - DNS confiable ({server}): dig {domain} @{server} +short")

        # Comparación HTTP mínima
        result.append("\n[!] DETECTANDO DIFERENCIAS CLAVE EN HTML...")
        diff = get_http_diff(domain, rogue_ips[0])
        result.append("\n[diferencias en formularios/login]:")
        result.append(diff if diff else "  - No se detectaron diferencias clave")

        # Comandos CURL
        result.append("\n[+] COMANDOS PARA VERIFICACIÓN MANUAL:")
        result.append(f"  - curl --header 'Host: {domain}' http://{rogue_ips[0]}")
    
    full_result = "\n".join(result)
    print(full_result)
    save_to_txt(report_filename, full_result)
    
    return rogue_ips if discrepancies else None

def main():
    print("\n=== ANALIZADOR DE PHARMING (FOCALIZADO) ===")
    rogue_dns = input("\nIngrese IP del DNS sospechoso: ").strip()
    domains = input("Ingrese dominios (separados por coma): ").strip().split(',')
    
    create_reports_dir()
    report_file = f"{REPORTS_DIR}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    malicious_ips = {}

    for domain in domains:
        domain = domain.strip()
        if domain:
            ips = analyze_domain(domain, rogue_dns, report_file)
            if ips:
                for ip in ips:
                    malicious_ips.setdefault(ip, []).append(domain)

    # Resumen ejecutivo
    if malicious_ips:
        summary = [
            "\n" + "="*50,
            "[+] RESUMEN DE IPs MALICIOSAS:",
            "="*50
        ]
        for ip, domains in malicious_ips.items():
            summary.append(f"  → IP {ip} afecta a: {', '.join(domains)}")
        
        full_summary = "\n".join(summary)
        print(full_summary)
        save_to_txt(report_file, full_summary)

    print(f"\n[+] Reporte guardado en: {report_file}")

if __name__ == "__main__":
    main()