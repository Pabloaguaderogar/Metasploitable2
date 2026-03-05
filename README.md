# 🛡️ Metasploitable 2: Vulnerability Analysis & Hardening Lab
---
**Legal Disclaimer:** *This laboratory was performed in a controlled environment for educational purposes only. All activities were authorized and follow ethical hacking guidelines.*
---
## 📋 Resumen del Proyecto
Este repositorio es una bitácora técnica de auditoría sobre un entorno **Metasploitable 2**. No se limita a la explotación, sino que documenta el ciclo completo: **Reconocimiento -> Explotación -> Exfiltración -> Hardening (Defensa) -> Limpieza**.
.
### 📂 Estructura del Proyecto
```text
.
├── ataques/                    # FASE OFENSIVA: Documentación de vectores de entrada y explotación
│   ├── 01_rpc/                 # Abuso de NFS/RPC para escalada de privilegios
│   │   ├── Ataque1_rpc.md
│   │   └── Ataque1_rpc.pdf
│   ├── 02_bindshell/           # Explotación de shells persistentes (Backdoors)
│   │   ├── Ataque_2_Bindshell.md
│   │   └── Ataque_2_Bindshell.pdf
│   ├── 03_unrealircd/          # Análisis de Supply Chain Attack (CVE-2010-2075)
│   │   ├── Ataque_3_UnreallRCD.md
│   │   └── Ataque_3_UnreallRCD.pdf
│   └── 04_samba/               # Cadena compleja: Samba + Tomcat + Dirty COW + Ransomware
│       ├── Samba.md
│       └── Samba.pdf
├── defensa/                    # FASE DEFENSIVA: Ingeniería, Hardening y Respuesta ante Incidentes
│   ├── 01_rpc/                 # Medidas de mitigación y cierre de puertos críticos
│   │   └── Defensa1_antes_educerecer_cerrar_NFS.pdf
│   ├── 04_samba/               # ANÁLISIS FORENSE POST-MORTEM (Wireshark Focus)
│   │   ├── md/                 # Artefactos visuales y OSINT (VirusTotal)
│   │   │   ├── cow_vt.csv      # Análisis de hashes del exploit Dirty COW
│   │   │   └── ... (.png)      # Capturas de flujos TCP y evidencias de intrusión
│   │   ├── Samba_Forensics.md  # Informe detallado del compromiso de Tomcat y Samba
│   │   └── Samba_Forensics.pdf
│   └── 04_samba_real_time/     # INGENIERÍA DE DETECCIÓN (Sonda Híbrida)
│       ├── 04_samba_analysis/  # DATA SCIENCE: Análisis avanzado con Python/Pandas
│       │   ├── Analisis_pcap.ipynb # Notebook con modelo estadístico 3-sigma 
│       │   ├── Analisis_pcap.md    
│       │   └── output_... (.png)   # Gráficas de baseline, anomalías y Kill Chain sincronizada
│       ├── alert.py            # Sonda en tiempo real (Scapy): Motor de DPI y Volumetría
│       ├── Sonda_IDS.md        # Especificaciones del motor de detección (Modelos Alice, Bob, Charly)
│       └── ... (.png)          # Capturas de la sonda en ejecución detectando 'firefart' y '.war'
├── evidence/                   # TRAZABILIDAD: Capturas de tráfico bruto (PCAP) para auditoría
│   ├── 04_samba/               # Tráfico de la intrusión completa (73MB)
│   │   ├── intrusion.tar.xz
│   │   └── intrusion.zip
│   └── 04_samba_realtime/      # Tráfico específico para validación de la Sonda IDS
│       ├── samba_real_time.tar.xz
│       └── samba_real_time.zip
└── README.md                   # ÍNDICE GENERAL: Metodología, hitos y resumen ejecutivo            # Índice General e hitos del proyecto
```
---

### ⚙️ Metodología de Trabajo

Basado en la formación del **Google Cybersecurity Professional Certificate**, este laboratorio documenta un ciclo de seguridad completo:

1. **PCAP Logging:** Captura proactiva de tráfico para garantizar la trazabilidad.
2. **Análisis Clásico:** Explotación controlada para identificar el impacto real.
3. **Hardening & Remediation:** Implementación de medidas de endurecimiento.
4. **Detección en Tiempo Real:** Scripts para identificación de patrones de intrusión.                 # Índice General

---

## 📑 Casos de Estudio Detallados

### 01. Abuso de RPC y NFS: Escalada de Privilegios Crítica
* **Identificación:** Escaneo con `nmap -sS` detectando el puerto **111 (rpcbind)** y **2049 (nfs)**.
* **Vulnerabilidad:** Exportación del sistema de archivos raíz (`/`) con permisos de lectura/escritura a cualquier IP (`showmount -e`).
* **Explotación:** 1. Montaje remoto del filesystem: `mount -t nfs 192.168.56.101:/ /mnt/nfsroot`.
    2. Inyección de persistencia: Edición directa de `/etc/passwd` y `/etc/shadow` desde la máquina atacante para crear el usuario `hack` con **UID 0** (Root) y sin contraseña.
* **Exfiltración:** Uso de `tar` para empaquetar `/home/msfadmin` y transferencia vía servidor HTTP temporal en Python.
* **📁 [Informe Técnico Detallado](./ataques/01_rpc/Ataque1_rpc.md)**

---

### 02. Bindshell en Puerto 1524: De la Explotación al Hardening
* **Identificación:** Detección de `ingreslock` en el puerto **1524**.
* **Vulnerabilidad:** Shell de root abierta por defecto (Backdoor).
* **Análisis Atacante:** Comparativa técnica entre `nc` y `telnet`. Uso de **Netcat** para obtener una shell interactiva instantánea.
* **Hardening (Defensa):**
    1. **Contención Inmediata:** Bloqueo del puerto mediante `iptables -A INPUT -p tcp --dport 1524 -j DROP`.
    2. **Investigación de Procesos:** Uso de `ss -lntp` y `ps -fp <PID>` para identificar que el proceso era lanzado por el super-servidor `xinetd`.
    3. **Remediación Definitiva:** Desactivación del servicio en `/etc/xinetd.d/` y reinicio del demonio para eliminar el vector de ataque permanentemente.
* **📁 [Informe Técnico Detallado](./ataques/02_bindshell/Ataque_2_Bindshell.md)**

---

## 🧹 Disciplina de Post-Explotación (Cleanup)
Siguiendo estándares profesionales de auditoría, cada ataque incluye una fase de limpieza para reducir la huella digital:
* Eliminación de artefactos y archivos temporales en `/tmp`.
* Cierre de servicios auxiliares y procesos huérfanos.
* Restauración de archivos de sistema (`/etc/passwd`).
* Limpieza selectiva del historial de comandos (`history -c`).

---

### 03. UnrealIRCd: Supply Chain Attack & Análisis de Persistencia
* **Identificación:** Banner Grabbing manual con `nc 192.168.56.101 6667`. Se identificó la versión **Unreal3.2.8.1**, conocida históricamente por contener un backdoor en su código fuente (CVE-2010-2075).
* **Explotación:** 1. Uso del framework **Metasploit** (`exploit/unix/irc/unreal_ircd_3281_backdoor`).
    2. Configuración de **Reverse Shell** mediante el payload `cmd/unix/reverse` para establecer la conexión hacia la máquina atacante (Kali).
* **Post-Explotación:** 1. **Exfiltración Crítica:** Recolección de los archivos `/etc/passwd` y `/etc/shadow`. 
    2. **Cracking de Credenciales:** Uso de la herramienta `unshadow` para combinar ambos ficheros y preparación para ataque de fuerza bruta offline con **John the Ripper**.
* **Hardening y Lección Aprendida:** 1. Se demostró que un Firewall (`iptables`) reduce la superficie de ataque externa pero no elimina la vulnerabilidad intrínseca del software. 
    2. **Recomendación:** Actualización inmediata a una versión no comprometida o deshabilitación total del servicio si no es esencial para el negocio.
* **📁 [Informe Técnico Detallado](./ataques/03_unrealircd/Ataque_3_UnreallRCD.md)**

---

### 04. Samba & Tomcat: De la Exposición de Archivos al Ransomware Real
* **Fase 1: Exposición SMB:** Se detectó un servicio Samba (3.0.20) con login anónimo permitido. Se verificó capacidad de **Escritura (R/W)** en el directorio `/tmp`, lo que permite el staging de malware y scripts de escalada.
* **Fase 2: Pivotaje a Tomcat:** Mediante fuerza bruta de credenciales por defecto, se obtuvo acceso al panel de gestión de **Apache Tomcat/5.5** (`tomcat:tomcat`).
* **Fase 3: Intrusión:** Despliegue de un archivo `.war` malicioso generado con `msfvenom` para obtener una shell reversa.
* **Fase 4: Escalada de Privilegios (Dirty COW):** * Uso del exploit `CVE-2016-5195` (Dirty COW) para sobrescribir el archivo `/etc/passwd`.
    * Creación de un usuario root temporal (`firefart`) y posterior persistencia mediante un **SUID Wrapper en C** compilado *in-situ*.
* **Fase 5: Simulación de Ransomware:** Ejecución de un script Bash que automatiza el cifrado de archivos mediante `OpenSSL` (AES-256-CBC), demostrando el impacto real de una intrusión no detectada.
* **Defensa y Mitigación:** * **Principio de Menor Privilegio:** Restringir el acceso anónimo en Samba (`map to guest = never`).
    * **Gestión de Credenciales:** Cambio inmediato de contraseñas por defecto en servicios administrativos.
    * **Patch Management:** Actualización del Kernel para mitigar vulnerabilidades de tipo Race Condition.
* **📁 [Código del Ransomware y Bitácora](./ataques/04_samba/Samba.md)**

---

### 0.5 Análisis Forense del Caso 04 (Blue Team Focus)
Para este análisis se utilizó el archivo `intrusion.pcap` (73 MB). El reto principal consistió en filtrar el ruido de red (tráfico HTTP de usuarios legítimos, ARP y broadcast) para aislar la actividad del atacante.



#### A. Mapeo de Vectores (Identificación del Atacante .102)
Tras aplicar filtros de exclusión, se identificó la secuencia de escaneo y la apertura del canal C2 (4444).

| No. | Time | Src | Dst | Puerto | Stream |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5160 | 201.2 | .101 | .102 | 8180 [S,A] | 2170 |
| 5185 | 201.2 | .101 | .102 | 80 [S,A] | 2173 |
| **7303** | **655.2** | **.102** | **.101** | **4444 [S,A]** | **2493** |

#### B. Evidencia de Compromiso en Tomcat
Identificación del acceso administrativo y la inyección del payload mediante tráfico HTTP.

| No. | Time | Len | Src→Dst | Status / Auth | Detalle Forense |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 6525 | 456.3 | 480 | .102→.101 | **tomcat:tomcat** | Creds. Default. |
| 6526 | 456.3 | 8868 | .101→.102 | **200 OK** | **ACCESO OK** |
| **7259** | **649.7** | **557** | **POST (V1)*** | **SUBIDA .WAR** |

#### C. Deep Packet Inspection (DPI)
El análisis del **Stream 2493** confirmó la descarga del código fuente del exploit y su compilación inmediata con `gcc` dentro de la shell. La detección de estos comandos en texto claro confirma la actividad maliciosa post-explotación y la escalada a root.

#### D. Conclusión y Recomendaciones Ejecutivas
El host fue comprometido debido a credenciales débiles y un kernel desactualizado. Se recomienda:
1. **Contención:** Aislamiento del host y purga de directorios en `/webapps/`.
2. **Hardening:** Cambio de contraseñas de Tomcat y restricción de acceso al panel por IP.
3. **Remediación:** Actualización urgente del Kernel para mitigar vulnerabilidades de Race Condition.

* **📁 [Informe Forense](./defensa/04_samba/md/Samba_Forensics.md)** * **📊 [Análisis OSINT VirusTotal (Dirty COW)](./defensa/04_samba/md/cow_vt.csv)**
* **📦 Evidencia PCAP (Real Noise):** **[Descargar .tar.xz (Linux)](./evidence/04_samba/intrusion.tar.xz)** | **[Descargar .zip (Windows)](./evidence/04_samba/intrusion.zip)**

---

### 06. Sonda IDS Híbrida
#### A. Evolución de Modelos (Alice, Bob & Charly)

*   Alice (DPI): Detección de firmas estáticas. Efectiva pero vulnerable a variaciones.

*    Bob (Volumetría): Detección de ráfagas simple. Alto ratio de falsos positivos con tráfico legítimo.

*    Charly (Ventana Temporal): Implementación de un intervalo de integración de 3.0s. Logra diferenciar el tráfico humano interactivo de los escaneos automatizados basándose en la densidad de eventos (Hz).

#### B. Capacidades Actuales

1.    Lógica Volumétrica: Filtra ráfagas de Nmap y detecta actividad de terminal interactiva.

2.    DPI de Ejecución: Alertas inmediatas ante el uso de gcc, ptrace, mmap, firefart y subidas de archivos .war.

#### C. Lecciones Aprendidas y Roadmap

1.    Enrutamiento Asimétrico: Se documentó el fallo en el escenario Kali-Charly-Bob, donde la falta de ruta de retorno impedía el sniffing bidireccional, optando por una monitorización en el host objetivo.

2.    Limitaciones de Scapy: Se identificó que exfiltraciones masivas (>6 MB/s) pueden saturar el procesamiento en Python.

3.    Mejora Propuesta: Migrar de métricas PPS (Paquetes por segundo) a BPS (Bytes por segundo) para detectar exfiltraciones pesadas fragmentadas.

* **📁 [Documentación de la Sonda](./defensa/04_samba_real_time/Sonda_IDS.md)** | **🐍 [Código Fuente](./defensa/04_samba_real_time/alert.py)**

* **📦 Evidencia IDS (Real Time):** **[Descargar .tar.xz (Linux)](./evidence/04_samba_real_time/samba_real_time.tar.xz)** | **[Descargar .zip (Windows)](./evidence/04_samba_real_time/samba_real_time.zip)**

---

### 07. Sonda IDS Híbrida: Análisis Estadístico y Correlación Temporal

Para elevar la capacidad de detección, se ha desarrollado un motor de análisis post-captura en **Python (Pandas/Matplotlib)** que correlaciona la telemetría de red con los logs de la sonda IDS.

#### A. Modelo de Detección Estadística (Baseline vs. Anomalía)
A diferencia de los umbrales estáticos, se ha implementado un modelo basado en **Física Estadística**:
* **Baseline dinámico:** Cálculo de la media y desviación estándar ($\sigma$) del tráfico en condiciones normales.
* **Criterio de Detección ($3\sigma$):** Aplicación de la regla empírica para identificar anomalías con un **99.7% de confianza estadística**. Esto permite ignorar el "ruido" de red y centrar la alerta en ráfagas reales de ataque.
* **Escalabilidad Logarítmica:** Visualización en escala logarítmica para detectar simultáneamente exfiltraciones masivas (3000 PPS) y persistencia silenciosa (10 PPS).

#### B. Correlación de la Kill Chain (Cadena de Ataque)
Mediante una **sincronización multicapa**, se han mapeado los eventos detectados por la sonda (DPI) sobre el flujo de paquetes del PCAP:

1. **Reconocimiento (Escaneo Nmap):** Identificado por ráfagas interactivas iniciales. Se filtran handshakes vacíos para optimizar la CPU de la sonda.
2. **Acceso Inicial (`.war`):** Correlación exacta entre el pico de tráfico HTTP y la firma de DPI de subida de artefactos.
3. **Escalada de Privilegios (`gcc` / `firefart`):** Detección de la fase de compilación in-situ y ejecución del exploit mediante inspección de strings en el payload.
4. **Control Total y Exfiltración:** Los picos finales de tráfico confirman la toma de control del atacante y la preparación de los datos para su salida.



#### C. Resultados del Análisis Forense Integrado

| Métrica | Valor Obtenido | Significado Forense |
| :--- | :--- | :--- |
| **Media Baseline** | 14.22 PPS | Tráfico normal de mantenimiento del servidor. |
| **Umbral Anomalía ($3\sigma$)** | 45.10 PPS | Límite superior de ruido; cualquier superación es incidente. |
| **Pico de Exfiltración** | **3102.0 PPS** | Momento exacto del compromiso de datos. |
| **Detección DPI** | 100% Match | Correlación total entre anomalía estadística y firma maliciosa. |

* **📁 [Notebook de Análisis (Pandas)](./defensa/04_samba_real_time/04_samba_analysis/Analisis_pcap.ipynb)** * **🐍 [Lógica de la Sonda](./defensa/04_samba_real_time/alert.py)**
