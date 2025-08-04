import pandas as pd

# Cargar el archivo Excel con los datos sucios
# Cambiar el nombre del archivo si está en otra ruta
archivo = 'restaurantes_sucio.xlsx'

df = pd.read_excel(archivo)

# Eliminar columnas que no sirven para análisis
columnas_a_eliminar = [
    'Código interno',
    'ID Pedido',
    'Comentario extra',
    '¿Reserva previa?',
    'Ticket impreso'
]
df = df.drop(columns=columnas_a_eliminar, errors='ignore')

# Seleccionar sólo las columnas relevantes
columnas_relevantes = [
    'Fecha', 'Plato', 'Precio', 'Propina', 'Empleado', 'Método de pago', 'País', 'Cliente'
]
df = df[columnas_relevantes]

# Extraer el nombre del cliente desde la columna "Cliente"
# (elimina números u otros caracteres adicionales)
df['Cliente'] = df['Cliente'].astype(str).str.extract(r'([A-Za-zÁÉÍÓÚáéíóúñÑ ]+)', expand=False).str.strip()

# Estandarizar el formato de fecha a YYYY-MM-DD
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce', dayfirst=True).dt.strftime('%Y-%m-%d')

# Convertir "Precio" y "Propina" a números enteros
for columna in ['Precio', 'Propina']:
    df[columna] = df[columna].astype(str).str.replace(r'[^0-9]', '', regex=True)
    df[columna] = pd.to_numeric(df[columna], errors='coerce').fillna(0).astype(int)

# El DataFrame "df" ahora está limpio y listo para análisis
print(df.head())

# Si se desea guardar el resultado:
# df.to_csv('restaurantes_limpio.csv', index=False)
