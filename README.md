# **📌 Rogue DNS & Pharming Detector**

**🔍 Descripción**:  
Este script automatiza la detección de servidores **Rogue DNS** (DNS maliciosos) y posibles ataques de **Pharming** comparando las respuestas DNS de un servidor sospechoso con servidores confiables (Google, Cloudflare, Quad9).

---

## **🚀 Características**

✅ **Interactivo**: Pide los datos por terminal (dominios y IP del DNS sospechoso).  
✅ **Análisis detallado**: Muestra comparaciones lado a lado entre DNS maliciosos y legítimos.  
✅ **Comandos `dig`**: Genera automáticamente comandos para verificación manual en Linux/macOS.  
✅ **Reportes en TXT**: Guarda resultados en `./reports/` con marcas de tiempo.  
✅ **Detección masiva**: Analiza múltiples dominios en una sola ejecución.

---

## **🛠 Instalación**

1. **Requisitos**:

   - Python 3.8+
   - Biblioteca `dnspython`

2. **Instalar dependencias**:
   ```bash
   pip install dnspython
   ```

---

## **📋 Uso**

### **1. Ejecución básica**:

```bash
python rogue_dns_detector_pro.py
```

- **Ejemplo de entrada**:
  ```plaintext
  Ingrese la IP del DNS sospechoso (ej. 45.55.197.218): 45.55.197.218
  Ingrese dominios a verificar (separados por coma, ej. banco.com,paypal.com): banco.com,paypal.com
  ```

### **2. Salida en terminal**:

```plaintext
==================================================
[*] DOMINIO: banco.com
==================================================
[+] DNS SOSPECHOSO (45.55.197.218):
    → IP: 182.189.112.153

[+] COMPARACIÓN CON DNS CONFIABLES:
  - 8.8.8.8: 104.18.25.63
  - 1.1.1.1: 104.18.25.63
  - 9.9.9.9: 104.18.25.63

[!] CONCLUSIÓN: POSIBLE PHARMING (IPs diferentes)

[+] COMANDOS DIG PARA VERIFICACIÓN MANUAL:
  - DNS sospechoso: dig banco.com @45.55.197.218 +short
  - DNS confiable (8.8.8.8): dig banco.com @8.8.8.8 +short
  - DNS confiable (1.1.1.1): dig banco.com @1.1.1.1 +short
```

### **3. Reportes automáticos**:

Los resultados se guardan en:

```bash
./reports/report_20231025_143022.txt  # Formato: report_AAAAMMDD_HHMMSS.txt
```

---

## **🛡️ ¿Qué es un Rogue DNS?**

Un **DNS malicioso** redirige tráfico legítimo a sitios falsos (ej: `banco.com` → IP fraudulenta). A diferencia del _phishing_, el dominio en la barra de direcciones **es el mismo**, pero la IP es falsa.

---

## **🔍 Método de Detección**

El script compara las IPs resueltas por:

1. **DNS sospechoso** (ej: `45.55.197.218`).
2. **DNS confiables** (Google `8.8.8.8`, Cloudflare `1.1.1.1`).

Si hay diferencias, se marca como **posible pharming**.

---

## **💡 Ejemplo de Ataque**

| Dominio    | DNS Malicioso   | DNS Legítimo   | Conclusión          |
| ---------- | --------------- | -------------- | ------------------- |
| banco.com  | 182.189.112.153 | 104.18.25.63   | ❗ POSIBLE PHARMING |
| google.com | 142.250.190.46  | 142.250.190.46 | ✅ OK               |

---

## **📌 Notas**

- **Linux/macOS**: Usa `dig` para verificación manual (incluido en el reporte).
- **Windows**: Puedes usar `nslookup` (no tan preciso como `dig`).
- **DNSSEC**: Para mayor seguridad, usa servidores con DNSSEC habilitado (ej: `1.1.1.1`).

---

## **📜 Licencia**

MIT License - Libre para uso y modificación.
