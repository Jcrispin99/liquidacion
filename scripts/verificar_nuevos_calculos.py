import openpyxl
import sys

try:
    # Abrir el archivo Excel generado
    archivo = '../output/Liquidacion_ALARCON_TUCTO_JHOMAYRA.xlsx'
    workbook = openpyxl.load_workbook(archivo)
    hoja = workbook.active

    print("=== VERIFICACIÓN DE NUEVOS CÁLCULOS Y TEXTOS ===", flush=True)
    print(f"Archivo: {archivo}", flush=True)
    print("", flush=True)

    # Verificar el primer período
    fila_actual = 105
    
    print(f"--- PERÍODO 1 (Fila base {fila_actual}) ---", flush=True)
    
    # MESES
    print("MESES:", flush=True)
    print(f"  D{fila_actual}: {hoja[f'D{fila_actual}'].value}", flush=True)
    print(f"  D{fila_actual + 1}: {hoja[f'D{fila_actual + 1}'].value}", flush=True)
    print(f"  S{fila_actual + 1}: {hoja[f'S{fila_actual + 1}'].value}", flush=True)
    
    # DÍAS
    print("DÍAS:", flush=True)
    print(f"  D{fila_actual + 2}: {hoja[f'D{fila_actual + 2}'].value}", flush=True)
    print(f"  D{fila_actual + 3}: {hoja[f'D{fila_actual + 3}'].value}", flush=True)
    print(f"  S{fila_actual + 3}: {hoja[f'S{fila_actual + 3}'].value}", flush=True)
    
    # TOTALES Y TEXTOS
    print("TOTALES Y TEXTOS:", flush=True)
    print(f"  S{fila_actual + 4}: {hoja[f'S{fila_actual + 4}'].value}", flush=True)
    print(f"  M{fila_actual + 4}: {hoja[f'M{fila_actual + 4}'].value}", flush=True)
    print(f"  M{fila_actual + 5}: {hoja[f'M{fila_actual + 5}'].value}", flush=True)
    print(f"  M{fila_actual + 6}: {hoja[f'M{fila_actual + 6}'].value}", flush=True)
    
    print("Verificación completada.", flush=True)
    workbook.close()
    
except Exception as e:
    print(f"Error: {e}", flush=True)
    sys.exit(1)