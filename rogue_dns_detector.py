import dns.resolver
import os
from datetime import datetime

# Configuración
TRUSTED_DNS_SERVERS = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
REPORTS_DIR = "reports"

def create_reports_dir():
    """Crea la carpeta de reportes si no existe."""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def save_to_txt(filename, data):
    """Guarda datos en un archivo TXT."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")

def resolve_domain(domain, dns_server):
    """Resuelve un dominio usando un servidor DNS específico."""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    try:
        answers = resolver.resolve(domain, 'A')
        return [answer.address for answer in answers]
    except Exception as e:
        return None

def analyze_domain(domain, rogue_dns, report_filename):
    rogue_ips = resolve_domain(domain, rogue_dns)
    if not rogue_ips:
        error_msg = f"[!] Error al resolver {domain} con el DNS sospechoso."
        print(error_msg)
        save_to_txt(report_filename, error_msg)
        return None

    # Generar comandos dig para verificación manual
    dig_commands = "\n[+] COMANDOS DIG PARA VERIFICACIÓN MANUAL:\n"
    dig_commands += f"  - DNS sospechoso: dig {domain} @{rogue_dns} +short\n"
    for trusted_server in TRUSTED_DNS_SERVERS:
        dig_commands += f"  - DNS confiable ({trusted_server}): dig {domain} @{trusted_server} +short\n"

    result = f"\n{'='*50}\n[*] DOMINIO: {domain}\n{'='*50}\n"
    result += f"[+] DNS SOSPECHOSO ({rogue_dns}):\n    → IP: {', '.join(rogue_ips)}\n\n"
    result += "[+] COMPARACIÓN CON DNS CONFIABLES:\n"

    discrepancies = False
    for trusted_server in TRUSTED_DNS_SERVERS:
        trusted_ips = resolve_domain(domain, trusted_server)
        if trusted_ips:
            result += f"  - {trusted_server}: {', '.join(trusted_ips)}\n"
            if rogue_ips != trusted_ips:
                discrepancies = True
        else:
            result += f"  - {trusted_server}: Error de resolución\n"

    conclusion = "\n[!] CONCLUSIÓN: " + ("POSIBLE PHARMING (IPs diferentes)" if discrepancies else "OK (IPs coincidentes)")
    result += conclusion + "\n"
    result += dig_commands  # 👈 Agrega los comandos dig al resultado

    save_to_txt(report_filename, result)
    return rogue_ips if discrepancies else None

def main():
    print("\n" + "="*50)
    print("=== DETECTOR AVANZADO DE ROGUE DNS Y PHARMING ===")
    print("="*50 + "\n")

    rogue_dns = input("Ingrese la IP del DNS sospechoso (ej. 45.55.197.218): ").strip()
    domains_input = input("Ingrese dominios a verificar (separados por coma, ej. banco.com,paypal.com): ").strip()
    domains = [domain.strip() for domain in domains_input.split(',') if domain.strip()]

    if not rogue_dns or not domains:
        print("\n[!] Error: Debes ingresar una IP de DNS y al menos un dominio.")
        return

    create_reports_dir()
    report_filename = f"{REPORTS_DIR}/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    malicious_ips = {}  # Ejemplo: {"182.189.112.153": ["banco.com", "paypal.com"]}

    for domain in domains:
        rogue_ips = analyze_domain(domain, rogue_dns, report_filename)
        if rogue_ips:
            for ip in rogue_ips:
                if ip not in malicious_ips:
                    malicious_ips[ip] = []
                malicious_ips[ip].append(domain)

    # Resumen de IPs maliciosas
    if malicious_ips:
        summary = "\n" + "="*50 + "\n[+] RESUMEN DE IPs MALICIOSAS:\n" + "="*50 + "\n"
        for ip, domains in malicious_ips.items():
            summary += f"  → IP {ip} afecta a: {', '.join(domains)}\n"
        print(summary)
        save_to_txt(report_filename, summary)

    print(f"\n[+] Reporte guardado en: {os.path.abspath(report_filename)}")

if __name__ == "__main__":
    main()