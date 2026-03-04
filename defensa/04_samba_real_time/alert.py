from scapy.all import sniff, TCP, IP
import datetime
import time

# 1. Configuración de objetivos
TARGET_IP = "192.168.56.101"

# Variables para análisis de ráfaga (Burst)
packet_count = 0
start_time = time.time()
packet_count1 = 0
start_time1 = time.time()
signatures = ["gcc", "ptrace", "mmap", "firefart", "pthread", ".war"]

def analyze_packet(pkt):
    global packet_count, start_time, signatures, packet_count1, start_time1
    
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        # Usamos decode con ignore para mayor limpieza técnica
        payload_raw = pkt[TCP].payload
        payload_str = bytes(payload_raw).decode('utf-8', errors='ignore')
        payload_size = len(payload_raw)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        # --- LÓGICA 1: FIRMAS (DPI) ---
        for sig in signatures:
            if sig in payload_str:
                print(f"[{timestamp}]  [ALERTA DPI] Firma detectada: '{sig}'")
                if sig == ".war" and pkt[IP].src != TARGET_IP:
                    print(f"   [!] CRÍTICO: Intento de subida de artefacto JAVA (.war)")
                print("-" * 50)

        # --- LÓGICA 2: COMPORTAMIENTO (Volumetría) ---
        # Detección de pulsación de tecla (Shell interactiva)
        if 0 < payload_size < 10:
            packet_count1 += 1
            current_time1 = time.time()
            
            # Comprobamos si ha pasado el "intervalo de integración"
            if current_time1 - start_time1 > 1.0:
                # HA PASADO EL SEGUNDO: Evaluamos qué hemos acumulado
                if packet_count1 > 3:
                    print(f"[{timestamp}]  Actividad interactiva: Posible Escaneo - Ráfaga: {packet_count1}pkts/s")
                else:
                    print(f"[{timestamp}]   Actividad interactiva (Shell/Teclado) - Size: {payload_size}B")
                
                # Reseteo de las variables de control para el siguiente intervalo
                packet_count1 = 0
                start_time1 = current_time1

        # Detección de ráfagas (Transferencia de archivos)
        if payload_size > 1400:
            packet_count += 1

        # Evaluación de ventana de tiempo (cada 1 segundo para no saturar la consola)
        current_time = time.time()
        if current_time - start_time > 1.0:
            if packet_count > 25: # Si en 1 seg hay más de 25 paquetes grandes
                print(f"[{timestamp}] 🚀 ALERTA DE FLUJO: Ráfaga de datos detectada ({packet_count} pks)")
            packet_count = 0
            start_time = current_time

# 3. Lanzamiento
print(f" Sonda híbrida (DPI + Volumetría) iniciada...")
print(f"Monitorizando {TARGET_IP}. Pulsa Ctrl+C para detener.\n")

sniff(filter=f"tcp and dst {TARGET_IP}", prn=analyze_packet, store=0, iface="eth0")
