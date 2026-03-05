import requests
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURACIÓN (Set Points) ---
LIMITE_BITCOIN = 60000 
SEGUNDOS_ESPERA = 60

def bot_profesional_mario():
    # 1. Inicio de Ciclo
    ahora = datetime.now().strftime('%H:%M:%S')
    print(f"\n>>> INICIANDO CICLO DE MONITOREO: {ahora}")
    
    monedas = ["bitcoin", "ethereum", "cardano"]
    resultados = []
    fecha_reporte = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        for crypto in monedas:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
            
            # 2. Validación de Conexión (Sensor de señal)
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if crypto in data:
                    precio = data[crypto]['usd']
                    print(f"[{crypto.upper()}] Capturado: ${precio} USD")
                    
                    # 3. Lógica de Alerta (Set Point)
                    if crypto == "bitcoin" and precio < LIMITE_BITCOIN:
                        print(f"!!! ALERTA DE SEGURIDAD: Bitcoin bajo el límite de ${LIMITE_BITCOIN} !!!")
                    
                    resultados.append({
                        "Moneda": crypto.upper(),
                        "Precio USD": precio,
                        "Fecha": fecha_reporte
                    })
            else:
                print(f"Error de señal en {crypto}: Status {response.status_code}")
                continue # Salta a la siguiente moneda si esta falla

        # 4. Generación del Entregable (Excel)
        if resultados:
            df = pd.DataFrame(resultados)
            # Guardamos con el nombre final para tu portafolio
            df.to_excel("Reporte_Final_Mario.xlsx", index=False)
            print(">>> Reporte Excel generado con éxito.")

    except Exception as e:
        print(f"FALLA CRÍTICA EN EL SISTEMA: {e}")

# --- EJECUCIÓN CONTINUA (Lógica de Planta) ---
if __name__ == "__main__":
    print("SISTEMA DE MONITOREO REMOTO ACTIVADO")
    print("Presiona Ctrl+C para detener el bot")
    
    while True:
        bot_profesional_mario()
        print(f"Ciclo completado. Esperando {SEGUNDOS_ESPERA} segundos...")
        time.sleep(SEGUNDOS_ESPERA)
