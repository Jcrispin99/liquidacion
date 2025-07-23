import pandas as pd
import openpyxl
import os
from datetime import date
from calculadoras import generar_y_calcular_periodos_cts

proyecto_dir = os.path.join(os.path.dirname(__file__), '..')

ruta_base_xls = os.path.join(proyecto_dir, 'base', 'base.xlsx')
ruta_plantilla = os.path.join(proyecto_dir, 'base', 'Plantilla.xlsx')

ruta_salida = os.path.join(proyecto_dir, 'output')

if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)
    print(f"Carpeta creada en: {ruta_salida}")


try:
    df = pd.read_excel(ruta_base_xls, skiprows=3)
    print("\nDatos de base.xls cargados correctamente.")

    for indice, fila in df.iterrows():
        plantilla_wb = openpyxl.load_workbook(ruta_plantilla)
        hoja = plantilla_wb.active

        # Verificar si el código del trabajador es válido
        if pd.isna(fila['Cod. Trab.']):
            codigo = "SIN_CODIGO"
        else:
            codigo = str(int(fila['Cod. Trab.']))
            
        # Verificar si el nombre de la persona es válido
        if pd.isna(fila['Apellidos y Nombres']):
            nombre_persona = "SIN_NOMBRE"
        else:
            nombre_persona = str(fila['Apellidos y Nombres'])
            
        cargo = fila['Cargo']
        f_ingreso = fila['Fec. Ing.']
        f_cese = fila['Fecha Cese']
        salario = fila['Basico']
        #sacar el promedio gratificacion año pasado hoja['K24'] = 520
        #dividir esa gratificacion en 6   hoja['P24'] = 520/6
        #computable = basico +  hoja['P24'] = 520/6 


        hoja['J16'] = nombre_persona          
        hoja['J17'] = "DNI N°: " + codigo
        hoja['J18'] = cargo
        hoja['J19'] = f_ingreso
        hoja['J20'] = f_cese
        hoja['J21'] = "EXTINCIÓN O LIQUIDACIÓN DEL EMPLEADOR"
        hoja['J22'] = f"del {f_ingreso} al {f_cese}"
        hoja['K23'] = salario
        hoja['K24'] = 520
        hoja['P24'] = 520/6
        hoja['K25'] = salario + 520/6

        # --- CÁLCULO DE CTS ---
        # Verificar si la fecha de ingreso es válida
        if pd.isna(f_ingreso):
            print(f"  Saltando CTS para {nombre_persona}: fecha de ingreso vacía")
        else:
            # Convertir fecha de ingreso a objeto date
            fecha_ingreso_trabajador = pd.to_datetime(f_ingreso, dayfirst=True).date()
            
            # Definir hasta qué fecha se calculará la CTS (ajustado para incluir trabajadores de 2025)
            fecha_calculo_cts = date(2025, 10, 31)

            # Obtener el historial de períodos CTS
            historial_cts = generar_y_calcular_periodos_cts(fecha_ingreso_trabajador, fecha_calculo_cts)

            # Escribir los datos de CTS a partir de la celda AE105
            fila_inicial = 105
            columna_excel = 'AE'
            
            fila_actual = fila_inicial
            for reporte in historial_cts:
                # Celda para los meses
                hoja[f'{columna_excel}{fila_actual}'] = reporte['meses_computables']
                
                # Celda para los días (una fila debajo)
                hoja[f'{columna_excel}{fila_actual + 1}'] = reporte['dias_computables']
                
                # Avanzamos 3 filas para el siguiente período (1 para días + 2 de espacio)
                fila_actual += 3

        nombre_archivo_salida = f"Liquidacion_{nombre_persona.replace(' ', '_')}.xlsx"
        ruta_completa_salida = os.path.join(ruta_salida, nombre_archivo_salida)

        try:
            plantilla_wb.save(ruta_completa_salida)
            print(f"Archivo generado: {nombre_archivo_salida}")
        except PermissionError:
            print(f"Error: No se pudo guardar {nombre_archivo_salida}. El archivo puede estar abierto en Excel. Ciérralo e intenta de nuevo.")

    print("\n¡Proceso completado! Revisa la carpeta 'output'.")

except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar un archivo: {e}")
except KeyError as e:
    print(f"Error: El nombre de una columna no se encontró en base.xls: {e}")
    print("Por favor, revisa los nombres de las columnas en la sección '¡AQUÍ LA MAGIA!'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
