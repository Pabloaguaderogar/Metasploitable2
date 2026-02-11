# 🛡️ Metasploitable 2: Vulnerability Analysis & Hardening Lab
> [!IMPORTANT]
> **Legal Disclaimer:** This laboratory was performed in a controlled environment for educational purposes only. All activities were authorized and follow ethical hacking guidelines.
## 📋 Resumen del Proyecto
Este repositorio es una bitácora técnica de auditoría sobre un entorno **Metasploitable 2**. No se limita a la explotación, sino que documenta el ciclo completo: **Reconocimiento -> Explotación -> Exfiltración -> Hardening (Defensa) -> Limpieza**.

---

## 📑 Casos de Estudio Detallados

### 01. Abuso de RPC y NFS: Escalada de Privilegios Crítica
* **Identificación:** Escaneo con `nmap -sS` detectando el puerto **111 (rpcbind)** y **2049 (nfs)**.
* **Vulnerabilidad:** Exportación del sistema de archivos raíz (`/`) con permisos de lectura/escritura a cualquier IP (`showmount -e`).
* **Explotación:** 1. Montaje remoto del filesystem: `mount -t nfs 192.168.56.101:/ /mnt/nfsroot`.
    2. Inyección de persistencia: Edición directa de `/etc/passwd` y `/etc/shadow` desde la máquina atacante para crear el usuario `hack` con **UID 0** (Root) y sin contraseña.
* **Exfiltración:** Uso de `tar` para empaquetar `/home/msfadmin` y transferencia vía servidor HTTP temporal en Python.
* **📁 [Informe Técnico Detallado](./ataques/01_rpc/Ataque1_rpc.pdf)**

### 02. Bindshell en Puerto 1524: De la Explotación al Hardening
* **Identificación:** Detección de `ingreslock` en el puerto **1524**.
* **Vulnerabilidad:** Shell de root abierta por defecto (Backdoor).
* **Análisis Atacante:** Comparativa técnica entre `nc` y `telnet`. Uso de **Netcat** para obtener una shell interactiva instantánea.
* **Hardening (Defensa):**
    1. **Contención Inmediata:** Bloqueo del puerto mediante `iptables -A INPUT -p tcp --dport 1524 -j DROP`.
    2. **Investigación de Procesos:** Uso de `ss -lntp` y `ps -fp <PID>` para identificar que el proceso era lanzado por el super-servidor `xinetd`.
    3. **Remediación Definitiva:** Desactivación del servicio en `/etc/xinetd.d/` y reinicio del demonio para eliminar el vector de ataque permanentemente.
* **📁 [Informe Técnico Detallado](./ataques/02_bindshell/Ataque_2_Bindshell.pdf)**

---

## 🧹 Disciplina de Post-Explotación (Cleanup)
Siguiendo estándares profesionales de auditoría, cada ataque incluye una fase de limpieza para reducir la huella digital:
* Eliminación de artefactos y archivos temporales en `/tmp`.
* Cierre de servicios auxiliares y procesos huérfanos.
* Restauración de archivos de sistema (`/etc/passwd`).
* Limpieza selectiva del historial de comandos (`history -c`).

### 03. UnrealIRCd: Supply Chain Attack & Análisis de Persistencia
* **Identificación:** Banner Grabbing manual con `nc 192.168.56.101 6667`. Se identificó la versión **Unreal3.2.8.1**, conocida históricamente por contener un backdoor en su código fuente (CVE-2010-2075).
* **Explotación:** 1. Uso del framework **Metasploit** (`exploit/unix/irc/unreal_ircd_3281_backdoor`).
    2. Configuración de **Reverse Shell** mediante el payload `cmd/unix/reverse` para establecer la conexión hacia la máquina atacante (Kali).
* **Post-Explotación:** 1. **Exfiltración Crítica:** Recolección de los archivos `/etc/passwd` y `/etc/shadow`. 
    2. **Cracking de Credenciales:** Uso de la herramienta `unshadow` para combinar ambos ficheros y preparación para ataque de fuerza bruta offline con **John the Ripper**.
* **Hardening y Lección Aprendida:** 1. Se demostró que un Firewall (`iptables`) reduce la superficie de ataque externa pero no elimina la vulnerabilidad intrínseca del software. 
    2. **Recomendación:** Actualización inmediata a una versión no comprometida o deshabilitación total del servicio si no es esencial para el negocio.
* **📁 [Informe Técnico Detallado](./ataques/03_unrealircd/Ataque_3_UnreallRCD.pdf)**

### 04. Samba & Tomcat: De la Exposición de Archivos al Ransomware Real
* **Fase 1: Exposición SMB:** Se detectó un servicio Samba (3.0.20) con login anónimo permitido. Se verificó capacidad de **Escritura (R/W)** en el directorio `/tmp`, lo que permite el staging de malware y scripts de escalada.
* **Fase 2: Pivotaje a Tomcat:** Mediante fuerza bruta de credenciales por defecto, se obtuvo acceso al panel de gestión de **Apache Tomcat/5.5** (`tomcat:tomcat`).
* **Fase 3: Intrusión:** Despliegue de un archivo `.war` malicioso generado con `msfvenom` para obtener una shell reversa.
* **Fase 4: Escalada de Privilegios (Dirty COW):** * Uso del exploit `CVE-2016-5195` (Dirty COW) para sobrescribir el archivo `/etc/passwd`.
    * Creación de un usuario root temporal (`firefart`) y posterior persistencia mediante un **SUID Wrapper** en C compilado *in-situ*.
* **Fase 5: Simulación de Ransomware:** Ejecución de un script Bash que automatiza el cifrado de archivos mediante `OpenSSL` (AES-256-CBC), demostrando el impacto real de una intrusión no detectada.
* **Defensa y Mitigación:** * **Principio de Menor Privilegio:** Restringir el acceso anónimo en Samba (`map to guest = never`).
    * **Gestión de Credenciales:** Cambio inmediato de contraseñas por defecto en servicios administrativos.
    * **Patch Management:** Actualización del Kernel para mitigar vulnerabilidades de tipo Race Condition.
* **📁 [Código del Ransomware y Bitácora](./ataques/04_samba/Samba.pdf)**
