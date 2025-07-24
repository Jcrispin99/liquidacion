from datetime import date
from dateutil.relativedelta import relativedelta

def calcular_meses_dias_gratificacion(fecha_ingreso, fecha_cese, periodo_grat_inicio, periodo_grat_fin):
    """
    Calcula meses y días computables para gratificación en un período semestral específico.
    
    Args:
        fecha_ingreso (date): Fecha de ingreso del trabajador
        fecha_cese (date): Fecha de cese o fin del período
        periodo_grat_inicio (date): Inicio del semestre gratificación (1 enero o 1 julio)
        periodo_grat_fin (date): Fin del semestre gratificación (30 junio o 31 diciembre)
    
    Returns:
        tuple: (meses, días) computables para el cálculo de gratificación
    """
    inicio_calculo = max(fecha_ingreso, periodo_grat_inicio)
    fin_calculo = min(fecha_cese, periodo_grat_fin)

    if fin_calculo < inicio_calculo:
        return 0, 0

    diferencia = relativedelta(fin_calculo + relativedelta(days=1), inicio_calculo)
    meses = diferencia.years * 12 + diferencia.months
    dias = diferencia.days

    return meses, dias

def generar_y_calcular_periodos_gratificacion(fecha_ingreso, fecha_cese_o_calculo):
    """
    Genera todos los períodos de gratificación semestrales para un trabajador.
    
    Las gratificaciones se calculan por períodos:
    - Enero a Junio (se paga en Julio)
    - Julio a Diciembre (se paga en Diciembre)
    
    Args:
        fecha_ingreso (date): Fecha de ingreso del trabajador
        fecha_cese_o_calculo (date): Fecha límite para el cálculo
    
    Returns:
        list: Lista de diccionarios con período, meses_computables y dias_computables
    """
    resultados_gratificacion = []

    # Determinar el primer período de gratificación
    if fecha_ingreso.month <= 6:
        # Si ingresó en el primer semestre, empezar con ese período
        periodo_actual_inicio = date(fecha_ingreso.year, 1, 1)
        periodo_actual_fin = date(fecha_ingreso.year, 6, 30)
    else:
        # Si ingresó en el segundo semestre, empezar con ese período
        periodo_actual_inicio = date(fecha_ingreso.year, 7, 1)
        periodo_actual_fin = date(fecha_ingreso.year, 12, 31)

    while periodo_actual_inicio <= fecha_cese_o_calculo:
        # Ajustar fecha fin si el período se extiende más allá de la fecha límite
        if periodo_actual_fin > fecha_cese_o_calculo:
            fecha_fin_calculo = fecha_cese_o_calculo
        else:
            fecha_fin_calculo = periodo_actual_fin

        meses, dias = calcular_meses_dias_gratificacion(
            fecha_ingreso, fecha_fin_calculo, periodo_actual_inicio, periodo_actual_fin
        )
        
        if meses > 0 or dias > 0:
            resultados_gratificacion.append({
                "periodo": f"{periodo_actual_inicio.strftime('%Y-%m-%d')} al {periodo_actual_fin.strftime('%Y-%m-%d')}",
                "meses_computables": meses,
                "dias_computables": dias
            })

        # Avanzar al siguiente período
        if periodo_actual_inicio.month == 1:  # Estaba en enero-junio
            periodo_actual_inicio = date(periodo_actual_inicio.year, 7, 1)
            periodo_actual_fin = date(periodo_actual_inicio.year, 12, 31)
        else:  # Estaba en julio-diciembre
            periodo_actual_inicio = date(periodo_actual_inicio.year + 1, 1, 1)
            periodo_actual_fin = date(periodo_actual_inicio.year, 6, 30)

    return resultados_gratificacion

def test_gratificacion_iterable():
    """
    Función de prueba para mostrar cómo funciona el iterable de períodos de gratificación
    """
    print("=== CALCULADORA DE PERÍODOS DE GRATIFICACIÓN (ITERABLE) ===")
    print()
    
    # Casos de prueba con diferentes fechas de ingreso
    casos_prueba = [
        {
            'nombre': 'Trabajador ingreso marzo 2021',
            'fecha_ingreso': date(2021, 3, 15),
            'fecha_calculo': date(2025, 7, 23),
            'descripcion': 'Ingresó en marzo 2021, cálculo hasta julio 2025'
        },
        {
            'nombre': 'Trabajador ingreso agosto 2022',
            'fecha_ingreso': date(2022, 8, 10),
            'fecha_calculo': date(2025, 7, 23),
            'descripcion': 'Ingresó en agosto 2022, cálculo hasta julio 2025'
        },
        {
            'nombre': 'Trabajador reciente 2024',
            'fecha_ingreso': date(2024, 11, 1),
            'fecha_calculo': date(2025, 7, 23),
            'descripcion': 'Ingresó en noviembre 2024, cálculo hasta julio 2025'
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"CASO {i}: {caso['nombre']}")
        print(f"Descripción: {caso['descripcion']}")
        print(f"Fecha ingreso: {caso['fecha_ingreso'].strftime('%d/%m/%Y')}")
        print(f"Fecha cálculo: {caso['fecha_calculo'].strftime('%d/%m/%Y')}")
        print()
        
        periodos = generar_y_calcular_periodos_gratificacion(
            caso['fecha_ingreso'], 
            caso['fecha_calculo']
        )
        
        print("PERÍODOS DE GRATIFICACIÓN:")
        print("-" * 60)
        
        total_periodos = len(periodos)
        for j, periodo in enumerate(periodos, 1):
            print(f"  Período {j}/{total_periodos}: {periodo['periodo']}")
            print(f"    Tiempo computable: {periodo['meses_computables']} meses, {periodo['dias_computables']} días")
            print()
        
        print(f"RESUMEN: {total_periodos} períodos de gratificación encontrados")
        print("=" * 70)
        print()

if __name__ == "__main__":
    test_gratificacion_iterable()