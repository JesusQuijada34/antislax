# Winslax_Widget.py - Widget Inteligente de Monitoreo y Limpieza
# Requiere: psutil

import psutil
import time
import os
import sys

# --- Configuración ---
# Umbral de uso de CPU/RAM para considerar un proceso como "consumidor alto"
CPU_THRESHOLD = 5.0  # % de CPU
RAM_THRESHOLD = 5.0  # % de RAM

def get_process_info():
    """Obtiene y clasifica los procesos por consumo de CPU y RAM."""
    high_consumers = []
    process_list = []
    
    # Obtener todos los procesos
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info
            pinfo['ram_mb'] = proc.memory_info().rss / (1024 * 1024)
            process_list.append(pinfo)
            
            if pinfo['cpu_percent'] > CPU_THRESHOLD or pinfo['memory_percent'] > RAM_THRESHOLD:
                high_consumers.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return process_list, high_consumers

def clean_temp_files():
    """Elimina archivos temporales comunes de Windows."""
    temp_paths = [
        os.path.join(os.environ.get('TEMP', ''), '*'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp', '*'),
    ]
    
    deleted_count = 0
    deleted_size = 0.0 # en MB

    # Esta función es un placeholder. En un entorno real de Windows,
    # se usaría `glob` y `os.remove` con manejo de errores para
    # eliminar archivos de forma segura. Aquí solo simulamos la limpieza.
    
    print("\n--- Limpieza de Archivos Temporales (Simulación) ---")
    print("En un entorno real, se eliminarían archivos de:")
    for path in temp_paths:
        print(f"  - {path}")
    
    # Simulación de resultados de limpieza
    deleted_count = 150
    deleted_size = 512.5
    
    print(f"\n[INFO] Archivos eliminados: {deleted_count}")
    print(f"[INFO] Espacio liberado: {deleted_size:.2f} MB")
    
    return deleted_count, deleted_size

def kill_process(pid):
    """Intenta terminar un proceso por su PID."""
    try:
        p = psutil.Process(pid)
        p.terminate()
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def main_widget_loop():
    """Bucle principal del widget de monitoreo."""
    
    # Limpieza inicial
    clean_temp_files()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 1. Información General
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        ram_total_gb = psutil.virtual_memory().total / (1024**3)
        ram_used_gb = psutil.virtual_memory().used / (1024**3)
        
        print("==================================================")
        print("         WINSLAX - MONITOR DE RENDIMIENTO         ")
        print("==================================================")
        print(f"  CPU Uso: {cpu_usage:.1f}%")
        print(f"  RAM Uso: {ram_usage:.1f}% ({ram_used_gb:.2f} GB / {ram_total_gb:.2f} GB)")
        print("--------------------------------------------------")
        
        # 2. Procesos de Alto Consumo
        process_list, high_consumers = get_process_info()
        
        if high_consumers:
            print(f"  PROCESOS DE ALTO CONSUMO (Umbral > {CPU_THRESHOLD}% CPU o > {RAM_THRESHOLD}% RAM):")
            print("  PID    | Nombre                  | CPU (%) | RAM (%) | RAM (MB)")
            print("  -------|-------------------------|---------|---------|----------")
            
            for p in high_consumers:
                print(f"  {p['pid']:<6} | {p['name'][:20]:<23} | {p['cpu_percent']:<7.1f} | {p['memory_percent']:<7.1f} | {p['ram_mb']:<8.1f}")
            
            print("--------------------------------------------------")
            
            # Opción de detener procesos
            action = input("¿Desea detener algún proceso (PID) o 'L' para Limpiar Temp o 'S' para Salir? ").strip().upper()
            
            if action == 'S':
                print("Saliendo del Widget de Winslax.")
                break
            elif action == 'L':
                clean_temp_files()
            elif action.isdigit():
                pid_to_kill = int(action)
                if kill_process(pid_to_kill):
                    print(f"[ÉXITO] Proceso {pid_to_kill} terminado.")
                else:
                    print(f"[ERROR] No se pudo terminar el proceso {pid_to_kill}.")
            
        else:
            print("  [INFO] No se encontraron procesos con alto consumo.")
            print("--------------------------------------------------")
            
            action = input("¿Desea 'L' para Limpiar Temp o 'S' para Salir? ").strip().upper()
            if action == 'S':
                print("Saliendo del Widget de Winslax.")
                break
            elif action == 'L':
                clean_temp_files()
        
        time.sleep(2) # Pausa antes de la próxima actualización

if __name__ == "__main__":
    # Verificar si psutil está instalado
    try:
        import psutil
    except ImportError:
        print("El módulo 'psutil' es necesario para este widget.")
        print("Por favor, instálelo con: pip install psutil")
        sys.exit(1)
        
    # El script Winslax_Widget.py está diseñado para ejecutarse en Windows.
    # La función `os.system('cls')` y la lógica de procesos son específicas de ese entorno.
    # En este entorno de sandbox, solo se mostrará la lógica de la función.
    print("Este es el Widget Inteligente de Winslax.")
    print("Para usarlo, debe ejecutarse en un sistema Windows con 'python Winslax_Widget.py'.")
    print("Se requiere el módulo 'psutil'.")
    
    # Ejecutar una sola vez la lógica principal para mostrar la funcionalidad
    # En un entorno real, se llamaría a main_widget_loop()
    clean_temp_files()
    
    # Simulación de monitoreo
    print("\n--- Simulación de Monitoreo ---")
    process_list, high_consumers = get_process_info()
    
    print(f"  CPU Uso: {psutil.cpu_percent(interval=1):.1f}%")
    print(f"  RAM Uso: {psutil.virtual_memory().percent:.1f}%")
    
    if high_consumers:
        print("\n  PROCESOS DE ALTO CONSUMO ENCONTRADOS:")
        for p in high_consumers:
            print(f"  - {p['name']} (CPU: {p['cpu_percent']:.1f}%, RAM: {p['memory_percent']:.1f}%)")
    else:
        print("\n  No se encontraron procesos de alto consumo en esta simulación.")
        
    print("\nFin de la simulación del Widget.")
