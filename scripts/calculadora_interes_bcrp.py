from datetime import datetime, timedelta
import math

def interes_bcrp(monto, fecha_inicio, fecha_fin):
    """
    Calcula el interés laboral según metodología BCRP
    
    Args:
        monto (float): Monto base para calcular interés
        fecha_inicio (str): Fecha de inicio en formato 'YYYY-MM-DD'
        fecha_fin (str): Fecha de fin en formato 'YYYY-MM-DD'
    
    Returns:
        float: Interés calculado redondeado a 2 decimales
    """
    try:
        # Convertir strings a objetos datetime
        fi = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        ff = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
        # Validar que fecha inicio sea menor que fecha fin
        if fi > ff:
            return 0.0
        
        # Calcular días transcurridos
        dias = (ff - fi).days
        
        # Tasa diaria efectiva aproximada usada por el BCRP
        # 7.35E-05 = 0.0000735 (aproximadamente 2.68% anual)
        tasa_diaria = 7.35e-5
        
        # Fórmula de interés compuesto: monto * ((1 + tasa)^dias - 1)
        acumulado = monto * ((1 + tasa_diaria) ** dias - 1)
        
        # Redondear a 2 decimales
        return round(acumulado, 2)
        
    except ValueError as e:
        print(f"Error en formato de fecha: {e}")
        return 0.0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 0.0

# Función de prueba
def test_interes_bcrp():
    """
    Función para testear la calculadora de intereses
    """
    print("=== PRUEBAS DE CALCULADORA DE INTERÉS BCRP ===")
    print()
    
    # Casos de prueba
    casos_prueba = [
        {
            'monto': 1000.0,
            'fecha_inicio': '2023-01-01',
            'fecha_fin': '2023-12-31',
            'descripcion': 'Año completo con S/1000'
        },
        {
            'monto': 500.0,
            'fecha_inicio': '2023-06-01',
            'fecha_fin': '2023-12-31',
            'descripcion': '6 meses con S/500'
        },
        {
            'monto': 248.26,  # Ejemplo basado en nuestros cálculos CTS
            'fecha_inicio': '2023-05-01',
            'fecha_fin': '2024-04-30',
            'descripcion': 'Período CTS típico con S/248.26'
        },
        {
            'monto': 1000.0,
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-01-31',
            'descripcion': 'Un mes con S/1000'
        },
        {
            'monto': 0.0,
            'fecha_inicio': '2023-01-01',
            'fecha_fin': '2023-12-31',
            'descripcion': 'Monto cero'
        },
        {
            'monto': 1000.0,
            'fecha_inicio': '2023-12-31',
            'fecha_fin': '2023-01-01',
            'descripcion': 'Fechas invertidas (debe retornar 0)'
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        interes = interes_bcrp(
            caso['monto'], 
            caso['fecha_inicio'], 
            caso['fecha_fin']
        )
        
        # Calcular días para referencia
        try:
            fi = datetime.strptime(caso['fecha_inicio'], '%Y-%m-%d')
            ff = datetime.strptime(caso['fecha_fin'], '%Y-%m-%d')
            dias = (ff - fi).days if ff > fi else 0
        except:
            dias = 0
            
        print(f"Caso {i}: {caso['descripcion']}")
        print(f"  Monto: S/{caso['monto']:.2f}")
        print(f"  Período: {caso['fecha_inicio']} a {caso['fecha_fin']} ({dias} días)")
        print(f"  Interés calculado: S/{interes:.2f}")
        
        if caso['monto'] > 0 and dias > 0:
            tasa_efectiva = (interes / caso['monto']) * 100
            print(f"  Tasa efectiva: {tasa_efectiva:.4f}%")
        
        print()

def calcular_interes_cts(monto_cts, fecha_inicio_periodo, fecha_calculo=None):
    """
    Calcula el interés laboral para un monto CTS específico
    
    Args:
        monto_cts (float): Monto CTS base
        fecha_inicio_periodo (str): Fecha inicio del período CTS
        fecha_calculo (str, optional): Fecha hasta la cual calcular. Si es None, usa fecha actual
    
    Returns:
        dict: Información del cálculo de interés
    """
    if fecha_calculo is None:
        fecha_calculo = datetime.now().strftime('%Y-%m-%d')
    
    interes = interes_bcrp(monto_cts, fecha_inicio_periodo, fecha_calculo)
    
    # Calcular días para información adicional
    try:
        fi = datetime.strptime(fecha_inicio_periodo, '%Y-%m-%d')
        ff = datetime.strptime(fecha_calculo, '%Y-%m-%d')
        dias = (ff - fi).days if ff > fi else 0
    except:
        dias = 0
    
    return {
        'monto_base': monto_cts,
        'fecha_inicio': fecha_inicio_periodo,
        'fecha_calculo': fecha_calculo,
        'dias_transcurridos': dias,
        'interes_calculado': interes,
        'total_con_interes': monto_cts + interes,
        'tasa_efectiva_porcentaje': (interes / monto_cts * 100) if monto_cts > 0 else 0
    }

def test_interes_con_datos_cts():
    """
    Prueba la calculadora con datos similares a los que tendríamos en CTS
    """
    print("\n=== PRUEBAS CON DATOS TIPO CTS ===")
    print()
    
    # Simular algunos casos CTS
    casos_cts = [
        {
            'monto': 248.26,  # Ejemplo de nuestro cálculo anterior
            'fecha_inicio': '2023-05-01',
            'fecha_calculo': '2024-04-30',
            'descripcion': 'Período CTS completo (1 año)'
        },
        {
            'monto': 297.92,  # Otro ejemplo
            'fecha_inicio': '2023-11-01', 
            'fecha_calculo': '2024-04-30',
            'descripcion': 'Período CTS parcial (6 meses)'
        },
        {
            'monto': 150.00,
            'fecha_inicio': '2024-01-01',
            'descripcion': 'CTS desde enero hasta hoy'
        }
    ]
    
    for i, caso in enumerate(casos_cts, 1):
        resultado = calcular_interes_cts(
            caso['monto'],
            caso['fecha_inicio'],
            caso.get('fecha_calculo')
        )
        
        print(f"Caso CTS {i}: {caso['descripcion']}")
        print(f"  Monto CTS base: S/{resultado['monto_base']:.2f}")
        print(f"  Período: {resultado['fecha_inicio']} a {resultado['fecha_calculo']}")
        print(f"  Días transcurridos: {resultado['dias_transcurridos']}")
        print(f"  Interés laboral: S/{resultado['interes_calculado']:.2f}")
        print(f"  Total con interés: S/{resultado['total_con_interes']:.2f}")
        print(f"  Tasa efectiva: {resultado['tasa_efectiva_porcentaje']:.4f}%")
        print()

if __name__ == "__main__":
    test_interes_bcrp()
    test_interes_con_datos_cts()