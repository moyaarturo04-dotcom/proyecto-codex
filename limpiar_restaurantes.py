import pandas as pd

# Cargar datos
entrada = 'restaurantes_sucio.xlsx'
salida = 'restaurantes_limpios.xlsx'

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza la limpieza básica del DataFrame original."""
    # Crear columna con nombre de restaurante y quitar prefijo
    df['Restaurante'] = df['Cliente'].str.replace(r'^Cliente:\s*\d+\s*', '', regex=True).str.strip()

    # Normalizar país y restaurante
    df['País'] = df['País'].str.title()
    df['Restaurante'] = df['Restaurante'].str.title()

    # Convertir precios y propinas a números (remover símbolos y separadores)
    for col in ['Precio', 'Propina']:
        df[col] = (df[col]
                   .astype(str)
                   .str.replace('[^0-9,.-]', '', regex=True)
                   .str.replace('.', '', regex=True)
                   .str.replace(',', '.', regex=True)
                   .replace('', pd.NA)
                   .astype(float))

    # Estandarizar fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True, errors='coerce')

    # Calificación numérica contando estrellas
    df['Calificación'] = df['Calificación'].astype(str).str.count('⭐')

    # Tiempo de espera como número
    df['Tiempo espera (min)'] = pd.to_numeric(df['Tiempo espera (min)'], errors='coerce')

    # Columnas a conservar
    columnas = ['Restaurante', 'País', 'Fecha', 'Plato', 'Precio',
                'Método de pago', 'Propina', 'Calificación', 'Tiempo espera (min)']
    df_limpio = df[columnas].copy()
    return df_limpio

def generar_analisis(df: pd.DataFrame) -> pd.DataFrame:
    """Genera hoja de análisis con KPIs solicitados."""
    plato_mas_vendido = df['Plato'].mode().iloc[0]
    promedio_propina = df['Propina'].mean()
    tiempo_espera_prom = df['Tiempo espera (min)'].mean()

    total_por_pago = df.groupby('Método de pago')['Precio'].sum().reset_index()
    top_restaurantes = (df.groupby('Restaurante')['Calificación']
                          .mean()
                          .sort_values(ascending=False)
                          .head(5)
                          .reset_index())

    # Hoja de análisis organizada
    filas = []
    filas.append({'KPI': 'Plato más vendido', 'Valor': plato_mas_vendido})
    filas.append({'KPI': 'Promedio de propina', 'Valor': promedio_propina})
    filas.append({'KPI': 'Tiempo de espera promedio', 'Valor': tiempo_espera_prom})
    resumen = pd.DataFrame(filas)

    # Para exportación ordenada, devolvemos diccionarios
    return resumen, total_por_pago, top_restaurantes

def main():
    df = pd.read_excel(entrada)
    df_limpio = limpiar_datos(df)
    resumen, total_pago, top_rest = generar_analisis(df_limpio)

    with pd.ExcelWriter(salida, engine='openpyxl') as writer:
        df_limpio.to_excel(writer, sheet_name='datos_limpios', index=False)

        # Hoja de análisis
        start_row = 0
        resumen.to_excel(writer, sheet_name='analisis', index=False, startrow=start_row)
        start_row += len(resumen) + 2
        total_pago.to_excel(writer, sheet_name='analisis', index=False, startrow=start_row)
        start_row += len(total_pago) + 2
        top_rest.to_excel(writer, sheet_name='analisis', index=False, startrow=start_row)

if __name__ == '__main__':
    main()
