from datetime import date
from dateutil.relativedelta import relativedelta

def calcular_meses_cts(fecha_ingreso, fecha_cese, periodo_cts_inicio, periodo_cts_fin):
    """
    Calcula meses y días computables para CTS en un período semestral específico.
    
    Args:
        fecha_ingreso (date): Fecha de ingreso del trabajador
        fecha_cese (date): Fecha de cese o fin del período
        periodo_cts_inicio (date): Inicio del semestre CTS (1 mayo o 1 noviembre)
        periodo_cts_fin (date): Fin del semestre CTS (31 octubre o 30 abril)
    
    Returns:
        tuple: (meses, días) computables para el cálculo CTS
    """
    inicio_calculo = max(fecha_ingreso, periodo_cts_inicio)
    fin_calculo = min(fecha_cese, periodo_cts_fin)

    if fin_calculo < inicio_calculo:
        return 0, 0

    diferencia = relativedelta(fin_calculo + relativedelta(days=1), inicio_calculo)
    meses = diferencia.years * 12 + diferencia.months
    dias = diferencia.days

    return meses, dias

def generar_y_calcular_periodos_cts(fecha_ingreso, fecha_cese_o_calculo):
    """
    Genera todos los períodos CTS semestrales para un trabajador.
    
    Args:
        fecha_ingreso (date): Fecha de ingreso del trabajador
        fecha_cese_o_calculo (date): Fecha límite para el cálculo
    
    Returns:
        list: Lista de diccionarios con período, meses_computables y dias_computables
    """
    resultados_cts = []

    if 1 <= fecha_ingreso.month <= 4:
        periodo_actual_inicio = date(fecha_ingreso.year - 1, 11, 1)
        periodo_actual_fin = date(fecha_ingreso.year, 4, 30)
    elif 5 <= fecha_ingreso.month <= 10:
        periodo_actual_inicio = date(fecha_ingreso.year, 5, 1)
        periodo_actual_fin = date(fecha_ingreso.year, 10, 31)
    else:
        periodo_actual_inicio = date(fecha_ingreso.year, 11, 1)
        periodo_actual_fin = date(fecha_ingreso.year + 1, 4, 30)

    while periodo_actual_inicio <= fecha_cese_o_calculo:
        if periodo_actual_fin > fecha_cese_o_calculo:
            fecha_fin_calculo = fecha_cese_o_calculo
        else:
            fecha_fin_calculo = periodo_actual_fin

        meses, dias = calcular_meses_cts(fecha_ingreso, fecha_fin_calculo, periodo_actual_inicio, periodo_actual_fin)
        
        if meses > 0 or dias > 0:
            resultados_cts.append({
                "periodo": f"{periodo_actual_inicio.strftime('%Y-%m-%d')} al {periodo_actual_fin.strftime('%Y-%m-%d')}",
                "meses_computables": meses,
                "dias_computables": dias
            })

        if periodo_actual_inicio.month == 5:
            periodo_actual_inicio = date(periodo_actual_inicio.year, 11, 1)
            periodo_actual_fin = date(periodo_actual_inicio.year + 1, 4, 30)
        else:
            periodo_actual_inicio = date(periodo_actual_inicio.year + 1, 5, 1)
            periodo_actual_fin = date(periodo_actual_inicio.year, 10, 31)

    return resultados_cts