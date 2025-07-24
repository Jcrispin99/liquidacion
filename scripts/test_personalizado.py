from calculadora_interes_bcrp import calcular_interes_cts
from datetime import datetime

def test_personalizado():
    """
    Test personalizado con parámetros específicos:
    - Monto: S/76
    - Fecha inicio: 15/Enero/2021
    - Fecha fin: 23/Julio/2025 (fecha actual)
    """
    print("=== TEST PERSONALIZADO ===")
    print("Parámetros del test:")
    print("- Monto CTS: S/76.00")
    print("- Fecha de inicio del período: 15/01/2021")
    print("- Fecha de cálculo (hoy): 23/07/2025")
    print()
    
    # Calcular interés desde el 15 de enero 2021 hasta hoy
    resultado = calcular_interes_cts(
        76.00,  # monto_cts
        "2021-01-15"  # fecha_fin_periodo - desde cuando se debe el pago
    )
    
    print("RESULTADOS DEL CÁLCULO:")
    print("=" * 50)
    print(f"Monto CTS original: S/{resultado['monto_base']:.2f}")
    print(f"Fecha desde: 15/01/2021")
    print(f"Fecha hasta: {datetime.now().strftime('%d/%m/%Y')}")
    print(f"Días transcurridos: {resultado['dias_transcurridos']} días")
    print(f"Años transcurridos: {resultado['dias_transcurridos']/365:.2f} años")
    print()
    print(f"Interés laboral calculado: S/{resultado['interes_calculado']:.2f}")
    print(f"Total con interés: S/{resultado['total_con_interes']:.2f}")
    print(f"Tasa efectiva aplicada: {resultado['tasa_efectiva_porcentaje']:.4f}%")
    print()
    
    # Mostrar desglose del cálculo
    print("DESGLOSE DEL CÁLCULO:")
    print("-" * 30)
    tasa_diaria = 0.000274  # Tasa diaria BCRP
    factor_interes = (1 + tasa_diaria) ** resultado['dias_transcurridos']
    interes_teorico = 76.00 * (factor_interes - 1)
    
    print(f"Tasa diaria BCRP: {tasa_diaria:.6f} (0.0274%)")
    print(f"Factor de interés: (1 + {tasa_diaria:.6f})^{resultado['dias_transcurridos']} = {factor_interes:.6f}")
    print(f"Interés teórico: S/76.00 × ({factor_interes:.6f} - 1) = S/{interes_teorico:.2f}")
    print(f"Interés final (redondeado): S/{resultado['interes_calculado']:.2f}")
    print()
    
    # Comparación con diferentes escenarios
    print("COMPARACIÓN CON OTROS ESCENARIOS:")
    print("-" * 40)
    
    # Escenario 1: Si se hubiera pagado después de 1 año
    resultado_1_año = calcular_interes_cts(76.00, "2022-01-15")
    print(f"Si se pagara después de 1 año (15/01/2022):")
    print(f"  Interés: S/{resultado_1_año['interes_calculado']:.2f}")
    print(f"  Total: S/{resultado_1_año['total_con_interes']:.2f}")
    
    # Escenario 2: Si se hubiera pagado después de 2 años
    resultado_2_años = calcular_interes_cts(76.00, "2023-01-15")
    print(f"Si se pagara después de 2 años (15/01/2023):")
    print(f"  Interés: S/{resultado_2_años['interes_calculado']:.2f}")
    print(f"  Total: S/{resultado_2_años['total_con_interes']:.2f}")
    
    # Escenario 3: Si se hubiera pagado después de 3 años
    resultado_3_años = calcular_interes_cts(76.00, "2024-01-15")
    print(f"Si se pagara después de 3 años (15/01/2024):")
    print(f"  Interés: S/{resultado_3_años['interes_calculado']:.2f}")
    print(f"  Total: S/{resultado_3_años['total_con_interes']:.2f}")
    
    print()
    print(f"RESULTADO FINAL PARA TU CONSULTA:")
    print(f"Monto CTS: S/76.00")
    print(f"Período: 15/01/2021 al 23/07/2025")
    print(f"Días de mora: {resultado['dias_transcurridos']} días")
    print(f"INTERÉS LABORAL: S/{resultado['interes_calculado']:.2f}")
    print(f"TOTAL A PAGAR: S/{resultado['total_con_interes']:.2f}")

if __name__ == "__main__":
    test_personalizado()