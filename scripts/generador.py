import pandas as pd
import openpyxl
from openpyxl.styles import Font
import os
from datetime import date
from calculadora_cts import generar_y_calcular_periodos_cts
from calculadora_gratificaciones import generar_y_calcular_periodos_gratificacion

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
        gratificacion = salario/2 # Preguntar por el salario para ver si es el correcto
        computable = salario + (520 / 6)#referencial

        salario_antiguo = 1100
        gratificacion_antiguo = 550
        promedio_gratificacion = gratificacion_antiguo/6
        computable_antiguo = salario_antiguo + promedio_gratificacion

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
        hoja['K25'] = computable

        hoja['J93'] = nombre_persona          
        hoja['J94'] = "DNI N°: " + codigo
        hoja['J95'] = cargo
        hoja['J96'] = f_ingreso
        hoja['J97'] = f_cese
        hoja['J98'] = "EXTINCIÓN O LIQUIDACIÓN DEL EMPLEADOR"
        hoja['J99'] = f"del {f_ingreso} al {f_cese}"
        hoja['K100'] = salario_antiguo
        hoja['K101'] = gratificacion_antiguo
        hoja['K102'] = computable_antiguo
        hoja['P101'] = promedio_gratificacion
        hoja['K95'] = computable_antiguo


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
            tramo_numero = 1
            
            for reporte in historial_cts:
                # --- CÁLCULOS Y TEXTOS ---
                # Función auxiliar para escribir en celda si no está combinada
                def escribir_celda_segura(celda_ref, valor):
                    try:
                        if not isinstance(hoja[celda_ref], openpyxl.cell.MergedCell):
                            hoja[celda_ref] = valor
                            # Aplicar formato Arial Narrow tamaño 8
                            hoja[celda_ref].font = Font(name="Arial Narrow", size=8)
                    except:
                        pass  # Ignorar si hay error al escribir
                
                # D105: Texto descriptivo del tramo
                escribir_celda_segura(f'D{fila_actual}', f"Por Meses Completos: {tramo_numero} mer Tramo")
                
                # D106: Representación textual de la operación (mitad del computable / 12)
                mitad_computable = computable_antiguo / 2
                escribir_celda_segura(f'D{fila_actual + 1}', f"{int(mitad_computable)} / 12")
                
                # H106: Resultado numérico de mitad del computable / 12
                escribir_celda_segura(f'H{fila_actual + 1}', mitad_computable / 12)
                
                # J106: Cantidad de meses + "meses"
                escribir_celda_segura(f'J{fila_actual + 1}', f"{reporte['meses_computables']} meses")
                
                # S106: (mitad del computable / 12) * cantidad de meses
                resultado_meses = (mitad_computable / 12) * reporte['meses_computables']
                escribir_celda_segura(f'S{fila_actual + 1}', resultado_meses)
                
                # --- CÁLCULOS PARA DÍAS ---
                # D107: Texto descriptivo para días
                escribir_celda_segura(f'D{fila_actual + 2}', "Por Días")
                
                # D108: Representación textual de la operación para días (mitad del computable / 12 / 30)
                escribir_celda_segura(f'D{fila_actual + 3}', f"{round(mitad_computable/12, 1)} / 30")
                
                # H108: Resultado numérico de (mitad del computable / 12) / 30
                escribir_celda_segura(f'H{fila_actual + 3}', (mitad_computable / 12) / 30)
                
                # J108: Cantidad de días
                escribir_celda_segura(f'J{fila_actual + 3}', f"{reporte['dias_computables']} días")
                
                # S108: Resultado de la operación por la cantidad de días
                resultado_dias = ((mitad_computable / 12) / 30) * reporte['dias_computables']
                escribir_celda_segura(f'S{fila_actual + 3}', resultado_dias)
                
                # S109: Sumatoria de S106 (meses) + S108 (días)
                total_periodo = resultado_meses + resultado_dias
                escribir_celda_segura(f'S{fila_actual + 4}', total_periodo)
                
                # Textos descriptivos en columna M
                escribir_celda_segura(f'M{fila_actual + 4}', "TOTAL CTS")
                escribir_celda_segura(f'M{fila_actual + 5}', "INTERES LABORAL")
                escribir_celda_segura(f'M{fila_actual + 6}', "Total CTS, Interes Laboral")
                
                # Avanzamos 9 filas para el siguiente período (4 filas usadas + 3 de textos + 2 de espacio)
                fila_actual += 7
                tramo_numero += 1

        # --- CÁLCULO DE GRATIFICACIONES ---
        # Verificar si la fecha de ingreso es válida
        if pd.isna(f_ingreso):
            print(f"  Saltando Gratificaciones para {nombre_persona}: fecha de ingreso vacía")
        else:
            # Convertir fecha de ingreso a objeto date
            fecha_ingreso_trabajador = pd.to_datetime(f_ingreso, dayfirst=True).date()
            
            # Definir hasta qué fecha se calculará las gratificaciones
            # Usar fecha de cese si existe, sino usar 2025.06.30 como predeterminada
            if pd.isna(f_cese):
                fecha_calculo_grat = date(2025, 6, 30)
            else:
                fecha_calculo_grat = pd.to_datetime(f_cese, dayfirst=True).date()

            # Obtener el historial de períodos de gratificación
            historial_grat = generar_y_calcular_periodos_gratificacion(fecha_ingreso_trabajador, fecha_calculo_grat)

            # Escribir los datos de gratificación a partir de la fila 173
            fila_inicial_grat = 183
            
            fila_actual_grat = fila_inicial_grat
            tramo_numero_grat = 1
            
            # Función auxiliar para escribir en celda si no está combinada
            def escribir_celda_segura_grat(celda_ref, valor):
                try:
                    if not isinstance(hoja[celda_ref], openpyxl.cell.MergedCell):
                        hoja[celda_ref] = valor
                        # Aplicar formato Arial Narrow tamaño 8
                        hoja[celda_ref].font = Font(name="Arial Narrow", size=8)
                except:
                    pass  # Ignorar si hay error al escribir
            
            for periodo_grat in historial_grat:
                # Calcular gratificación (salario/2)
                gratificacion = salario_antiguo / 2
                
                # M: Período de gratificación (del XX.XX.XXXX al XX.XX.XXXX)
                periodo_texto = periodo_grat['periodo'].replace('-', '.')
                escribir_celda_segura_grat(f'M{fila_actual_grat}', f"del {periodo_texto}")
                
                # D173+: "Por Meses Completos: X mer Tramo"
                escribir_celda_segura_grat(f'D{fila_actual_grat}', f"Por Meses Completos: {tramo_numero_grat} mer Tramo")
                
                # D174+: Variable gratificación / 6
                escribir_celda_segura_grat(f'D{fila_actual_grat + 1}', f"{gratificacion} / 6")
                
                # H174+: resultado de gratificacion/6
                escribir_celda_segura_grat(f'H{fila_actual_grat + 1}', gratificacion / 6)
                
                # J174+: meses del período actual
                escribir_celda_segura_grat(f'J{fila_actual_grat + 1}', f"{periodo_grat['meses_computables']} meses")
                
                # S174+: (gratificacion/6) * meses del período actual
                resultado_meses_grat = (gratificacion / 6) * periodo_grat['meses_computables']
                escribir_celda_segura_grat(f'S{fila_actual_grat + 1}', resultado_meses_grat)
                
                # D175+: "Por Días"
                escribir_celda_segura_grat(f'D{fila_actual_grat + 2}', "Por Días")
                
                # D176+: (gratificacion/6) / 30
                escribir_celda_segura_grat(f'D{fila_actual_grat + 3}', f"{round(gratificacion/6, 1)} / 30")
                
                # H176+: (gratificacion/6)/30
                escribir_celda_segura_grat(f'H{fila_actual_grat + 3}', (gratificacion / 6) / 30)
                
                # J176+: días del período actual
                escribir_celda_segura_grat(f'J{fila_actual_grat + 3}', f"{periodo_grat['dias_computables']} días")
                
                # S176+: ((gratificacion/6)/30) * días del período actual
                resultado_dias_grat = ((gratificacion / 6) / 30) * periodo_grat['dias_computables']
                escribir_celda_segura_grat(f'S{fila_actual_grat + 3}', resultado_dias_grat)
                
                # S177+: Total del período (meses + días)
                total_periodo_grat = resultado_meses_grat + resultado_dias_grat
                escribir_celda_segura_grat(f'S{fila_actual_grat + 4}', total_periodo_grat)
                
                # Textos descriptivos en columna M para cada período
                escribir_celda_segura_grat(f'M{fila_actual_grat + 4}', 'TOTAL GRATIFICACION')
                
                # D: "BONIFICACION EXTRAORDINARIA:"
                escribir_celda_segura_grat(f'D{fila_actual_grat + 5}', 'BONIFICACION EXTRAORDINARIA:')
                
                # F: "Ley Nº 29351"
                escribir_celda_segura_grat(f'F{fila_actual_grat + 6}', 'Ley Nº 29351')
                
                # J: "*"
                escribir_celda_segura_grat(f'J{fila_actual_grat + 6}', '*')
                
                # K: "9"
                escribir_celda_segura_grat(f'K{fila_actual_grat + 6}', '9')
                
                # L: "%"
                escribir_celda_segura_grat(f'L{fila_actual_grat + 6}', '%')
                
                # M: "TOTAL BONIF. EXTRAORD."
                escribir_celda_segura_grat(f'M{fila_actual_grat + 6}', 'TOTAL BONIF. EXTRAORD.')
                
                # M: "TOT GRATIF, MAS BONIF"
                escribir_celda_segura_grat(f'M{fila_actual_grat + 7}', 'TOT GRATIF, MAS BONIF')
                
                escribir_celda_segura_grat(f'M{fila_actual_grat + 8}', 'INTERES LABORAL')
                
                # M: "SUMATORIA TOTAL DE GRATIF. INTERES LABORAL" (último antes de la siguiente iteración)
                escribir_celda_segura_grat(f'M{fila_actual_grat + 9}', 'SUMATORIA TOTAL DE GRATIF. INTERES LABORAL')
                
                # Avanzar 12 filas para el siguiente período (4 filas usadas + 8 de textos adicionales)
                fila_actual_grat += 11
                tramo_numero_grat += 1

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
