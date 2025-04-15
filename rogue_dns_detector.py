import dns.resolver

# Servidores DNS confiables para comparación
TRUSTED_DNS_SERVERS = ['8.8.8.8', '1.1.1.1', '9.9.9.9']

def resolve_domain(domain, dns_server):
    """Resuelve un dominio usando un servidor DNS específico."""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    try:
        answers = resolver.resolve(domain, 'A')
        return [answer.address for answer in answers]
    except Exception as e:
        print(f"[!] Error al resolver {domain} con {dns_server}: {e}")
        return []

def detect_rogue_dns(domain, suspicious_dns):
    """Compara la IP de un dominio entre un DNS sospechoso y servidores confiables."""
    rogue_ips = resolve_domain(domain, suspicious_dns)
    if not rogue_ips:
        print(f"[!] No se pudo resolver el dominio con el DNS sospechoso {suspicious_dns}.")
        return

    print(f"\n[*] Consultando dominio: {domain}")
    print(f"[*] DNS sospechoso ({suspicious_dns}) resuelve a: {', '.join(rogue_ips)}")

    # Comparar con DNS confiables
    discrepancies = False
    for trusted_server in TRUSTED_DNS_SERVERS:
        trusted_ips = resolve_domain(domain, trusted_server)
        if not trusted_ips:
            continue
        print(f"[+] DNS confiable ({trusted_server}) resuelve a: {', '.join(trusted_ips)}")
        if rogue_ips != trusted_ips:
            discrepancies = True

    if discrepancies:
        print("\n[!] ALERTA: Posible Rogue DNS y Pharming detectado.")
        print(f"    El DNS sospechoso {suspicious_dns} está resolviendo a una IP diferente: {', '.join(rogue_ips)}")
    else:
        print("\n[-] No se detectaron discrepancias. El DNS parece seguro.")

def main():
    print("\n=== Detector de Rogue DNS y Pharming ===")
    domain = input("\nIngrese el dominio a verificar (ej. banco.com): ").strip()
    rogue_dns = input("Ingrese la IP del DNS sospechoso (ej. 45.55.197.218): ").strip()

    if not domain or not rogue_dns:
        print("\n[!] Error: Debes ingresar un dominio y una IP de DNS válidos.")
        return

    detect_rogue_dns(domain, rogue_dns)

if __name__ == "__main__":
    main()