# 🛡️ Rogue DNS & Pharming Detector

Un script interactivo que permite detectar posibles ataques de **pharming** mediante la comparación entre resoluciones DNS de un servidor sospechoso y servidores confiables.

---

## 🔎 ¿Qué hace este script?

Este analizador realiza los siguientes pasos:

1. **Consulta un dominio usando un DNS sospechoso.**
2. **Compara los resultados con los de DNS confiables** como Google, Cloudflare y Quad9.
3. **Verifica si hay diferencias en el contenido HTML**, como formularios de inicio de sesión.
4. **Genera un reporte detallado** con evidencias técnicas, comandos útiles (`dig`, `curl`) y conclusiones.

---

## ✅ Características

- 🔹 Entrada por terminal (dominios y DNS sospechoso).
- 🔹 Detección automatizada de posibles ataques de pharming.
- 🔹 Análisis de diferencias clave en formularios HTML (`<form>`, `login`, `password`, etc.).
- 🔹 Comandos útiles para análisis manual (`dig`, `curl`).
- 🔹 Reportes generados automáticamente en la carpeta `reports/`.

---

## ⚙️ Requisitos

- Python 3.8+
- Módulos:
  - `dnspython`
  - `requests`

Instala las dependencias necesarias con:

```bash
pip install dnspython requests
```

---

## 🚀 Cómo usar

Ejecuta el script desde terminal:

```bash
python rogue_dns_detector.py
```

Ejemplo de entrada:

```plaintext
Ingrese IP del DNS sospechoso: 45.55.197.218
Ingrese dominios (separados por coma): banco.com,paypal.com
```

---

## 📤 Salida esperada

Ejemplo de análisis:

```
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
  - dig banco.com @45.55.197.218 +short
  - dig banco.com @8.8.8.8 +short

[!] DETECTANDO DIFERENCIAS CLAVE EN HTML...

[diferencias en formularios/login]:
--- LEGITIMO
+++ FRAUDULENTO
- <form action="/login" method="post">
+ <form action="http://phishingsite.com/fake" method="post">

[+] COMANDOS PARA VERIFICACIÓN MANUAL:
  - curl --header 'Host: banco.com' http://182.189.112.153
```

---

## 🗂 Reportes

Los reportes se guardan automáticamente en la carpeta `./reports/` con nombre:

```
report_YYYYMMDD_HHMMSS.txt
```

Incluyen:

- Análisis por dominio.
- Comparación de IPs.
- Detección de diferencias en HTML.
- Comandos sugeridos (`dig`, `curl`).
- Resumen de IPs maliciosas detectadas.

---

## 📚 ¿Qué es un ataque de pharming?

Es una técnica donde un atacante redirige el tráfico hacia un sitio fraudulento **sin cambiar el dominio visible**. Lo hace manipulando la resolución DNS, por eso es tan difícil de detectar solo visualmente.

---

## 🧪 Método de detección utilizado

| Paso | Descripción                                  |
| ---- | -------------------------------------------- |
| 1    | Resolver dominio con el DNS sospechoso       |
| 2    | Resolver el mismo dominio con DNS confiables |
| 3    | Detectar diferencias en IPs                  |
| 4    | Verificar diferencias en HTML (formularios)  |

---

## 📝 Notas adicionales

- Este script **no requiere privilegios de administrador**.
- Ideal para análisis en equipos SOC, laboratorios de ciberseguridad o cursos de hacking ético.
- Funciona en Windows, Linux y macOS.
- Las solicitudes HTTP ignoran certificados SSL para facilitar análisis contra IPs sin HTTPS (no recomendado en entornos de producción).

---

## 🧑‍💻 Autor y Licencia

- 📄 Licencia: MIT
- 🔧 Puedes modificar libremente este código.
