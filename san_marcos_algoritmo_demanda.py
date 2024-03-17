## Librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

"""## Archivos necesarios"""

demanda = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Ventas_reducido")
inventarios = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Inventario_reducido")
df_limite_inf = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Limite_inf")
df_limite_sup = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Limite_sup")
combinaciones = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Calidad")
escenario_positivo = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Escenario_positivo")
escenario_negativo = pd.read_excel("/content/Ventas__Inventario_SanMarcos.xlsx", sheet_name= "Escenario_negativo")

# Algortimo para determinar producción en función de la demanda

# Suponiendo que los dataframes ya están definidos como demada, escenario_positivo y escenario_negativo

def seleccionar_escenario():
    print("Seleccione un escenario:")
    print("1. Escenario normal")
    print("2. Escenario Positivo")
    print("3. Escenario Negativo")

    opcion = input("Ingrese el número del escenario que desea seleccionar: ")

    if opcion == '1':
        escenario = demanda
    elif opcion == '2':
        escenario = escenario_positivo
    elif opcion == '3':
        escenario = escenario_negativo
    else:
        print("Opción no válida. Por favor, intente de nuevo.")
        return seleccionar_escenario()

    return escenario

# Llamar a la función y almacenar el resultado en la variable escenario
escenario = seleccionar_escenario()

escenario

"""## Seleccionar el mes"""

# Selección del mes
# Lista de meses válidos
meses_validos = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Solicitar al usuario que seleccione un mes
while True:
    mes = input("Selecciona el mes (ejemplo: Marzo, Abril): ")
    if mes.capitalize() in meses_validos:
        break
    else:
        print("Mes no válido. Inténtalo de nuevo.")

print(f"Has seleccionado el mes de {mes.capitalize()}.")

mes

"""## Seleccionar el producto"""

# Selecciona el producto
opciones = ["Bote jalapeños 215", "Bote jalapeños 380","Bote jalapeños 780", "Bote jalapeños 2800", "Bote rajas verdes 105", "Bote rajas verdes 215", "Bote rajas verdes 380", "Bote rajas verdes 800"
,"Bote rajas verdes 2800", "Bote rodajas 380", "Bote rodajas 800", "Bote rodajas 2800", "Bote jalapeños en trozos 215"]

# Mostrar las opciones al usuario
print("Selecciona una opción:")
for i, opcion in enumerate(opciones, start=1):
    print(f"{i}. {opcion}")

# Solicitar al usuario que elija una opción
while True:
    try:
        seleccion = int(input("Ingresa el número de la opción elegida: "))
        if 1 <= seleccion <= len(opciones):
            break
        else:
            print("Número fuera de rango. Inténtalo de nuevo.")
    except ValueError:
        print("Ingresa un número válido.")

# Almacenar el resultado en una variable
producto_elegido = opciones[seleccion - 1]
print(f"Has seleccionado: {producto_elegido}")

"""## Función que calcula la diferencia entre la demanda del producto y el inventario"""

def calcular_diferencia_dataframe(mes, producto_elegido, escenario, df_inventarios, df_limite_inf, df_limite_sup):
    # Convertir el nombre del mes a título para coincidir con las columnas del dataframe
    mes = mes.title()

    # Verificar si el producto está en ambos dataframes
    if producto_elegido in escenario['Producto'].values and producto_elegido in inventarios['Producto'].values:
        # Obtener la demanda y el inventario para el producto y mes seleccionados
        demanda_producto = escenario.loc[escenario['Producto'] == producto_elegido, mes].values[0]
        inventario_producto = inventarios.loc[df_inventarios['Producto'] == producto_elegido, mes].values[0]

        # Calcular la diferencia
        diferencia = demanda_producto - inventario_producto

        # Obtener el límite_inf de la tabla según el producto y el mes
        limite_producto_mes_inf = df_limite_inf.loc[df_limite_inf['Producto'] == producto_elegido, mes].values[0]
        limite_producto_mes_sup = df_limite_sup.loc[df_limite_sup['Producto'] == producto_elegido, mes].values[0]

         # Mensaje de alta producción para los meses de Junio, Julio y Agosto
        if mes in ['Junio', 'Julio', 'Agosto']:
            return "Sí producir, mes de alta producción.", "Demanda:", demanda_producto, ",Inventario:", inventario_producto, ",Diferencia:", diferencia, ",Limite inferior:",limite_producto_mes_inf, ",Límite superior:",limite_producto_mes_sup

        # Verificar si la diferencia es menor a 0
        if diferencia < 0:
            return "No producir", "Demanda:", demanda_producto, "Inventario:", inventario_producto, "Diferencia:", diferencia, "Limite inferior:",limite_producto_mes_inf, "Límite superior:",limite_producto_mes_sup
        # Verificar si la diferencia es mayor a 0 y menor al límite
        elif 0 < diferencia < limite_producto_mes_inf:
            return "Producir", "Demanda:", demanda_producto, "Inventario:", inventario_producto, "Diferencia:", diferencia, "Limite inferior:",limite_producto_mes_inf, "Límite superior:",limite_producto_mes_sup
        elif diferencia > limite_producto_mes_sup:
            return "La demanda supera al inventario disponible y al limite superior", "Demanda:", demanda_producto, "Inventario:", inventario_producto, "Diferencia:", diferencia, "Limite inferior:",limite_producto_mes_inf, "Límite superior:",limite_producto_mes_sup
        else:
            return "Diferencia positiva, pero excede el límite", "Demanda:", demanda_producto, "Inventario:", inventario_producto, "Diferencia:", diferencia, "Limite inferior:",limite_producto_mes_inf, "Límite superior:",limite_producto_mes_sup
    else:
        return "Producto no encontrado en los dataframes."

# Ejemplo de uso de la función con el dataframe 'limite' incluido:
resultado = calcular_diferencia_dataframe(mes, producto_elegido, escenario, inventarios, df_limite_inf, df_limite_sup)
if isinstance(resultado, tuple):
    print(f"La recomendación para {producto_elegido} en {mes} es: {' '.join(map(str, resultado))}")
else:
    print(resultado)

"""### Seleccionar el tamaño del chile (Por combinación)

### Seleccionar la calidad del chile
"""

# Selecciona el producto
opciones_tamano = {
    "Grande-Grande": 1,
    "Grande-Mediano": 2,
    "Grande-Chico": 3,
    "Chico-Grande": 4,
    "Chico-Mediano": 5,
    "Chico-Chico": 6
}

# Mostrar las opciones al usuario
print("Selecciona el tamaño de chile:")
for opcion, numero in opciones_tamano.items():
    print(f"{numero}. {opcion}")

# Solicitar al usuario que elija una opción
while True:
    try:
        seleccion_numero = int(input("Ingresa el número de la opción elegida: "))
        if seleccion_numero in opciones_tamano.values():
            break
        else:
            print("Número fuera de rango. Inténtalo de nuevo.")
    except ValueError:
        print("Ingresa un número válido.")

# Almacenar el resultado en una variable
tamano_chile = seleccion_numero
print(f"Has seleccionado el tamaño número: {tamano_chile}")

# Selecciona el producto
opciones_calidad = {
    "Excelente Calidad": 1,
    "No plagado": 2,
    "Plagado": 3,
    "Mala calidad": 4
}

# Mostrar las opciones al usuario
print("Selecciona el tamaño de chile:")
for opcion, numero in opciones_calidad.items():
    print(f"{numero}. {opcion}")

# Solicitar al usuario que elija una opción
while True:
    try:
        seleccion_numero = int(input("Ingresa el número de la opción elegida: "))
        if seleccion_numero in opciones_calidad.values():
            break
        else:
            print("Número fuera de rango. Inténtalo de nuevo.")
    except ValueError:
        print("Ingresa un número válido.")

# Almacenar el resultado en una variable
calidad_chile = seleccion_numero
print(f"Has seleccionado el tamaño número: {tamano_chile}")

"""### Seleccionar las toneladas"""

while True:
    try:
        toneladas = float(input("Introduce las toneladas disponibles: "))
        break  # Si se introduce un número, se rompe el bucle
    except ValueError:
        print("Por favor, introduce un número válido.")
# Convertir las toneladas a gramos

"""## Preguntar el tamaño y la calidad, Utilizar el valor del producto y el id de las combinaciones para saber si si se puede hacer. En caso de que no se pueda mostrar las combinaciones posibles con las características (ID) del producto

### Combinaciones de productos
"""

# Suponiendo que tienes una lista de diccionarios que representan tu tabla de datos
productos = [{'Producto': 'Bote jalapeños 215', 'Tamaño': 5, 'Calidad': 1, 'ID': '5,1'},
 {'Producto': 'Bote jalapeños 2800', 'Tamaño': 1, 'Calidad': 1, 'ID': '1,1'},
 {'Producto': 'Bote jalapeños 380', 'Tamaño': 4, 'Calidad': 1, 'ID': '4,1'},
 {'Producto': 'Bote jalapeños 380', 'Tamaño': 3, 'Calidad': 1, 'ID': '3,1'},
 {'Producto': 'Bote jalapeños 780', 'Tamaño': 1, 'Calidad': 1, 'ID': '1,1'},
 {'Producto': 'Bote jalapeños 780', 'Tamaño': 2, 'Calidad': 1, 'ID': '2,1'},
 {'Producto': 'Bote rajas verdes 105', 'Tamaño': 5, 'Calidad': 3, 'ID': '5,3'},
 {'Producto': 'Bote rajas verdes 105', 'Tamaño': 5, 'Calidad': 4, 'ID': '5,4'},
 {'Producto': 'Bote rajas verdes 215', 'Tamaño': 4, 'Calidad': 3, 'ID': '4,3'},
 {'Producto': 'Bote rajas verdes 215', 'Tamaño': 5, 'Calidad': 3, 'ID': '5,3'},
 {'Producto': 'Bote rajas verdes 215', 'Tamaño': 4, 'Calidad': 4, 'ID': '4,4'},
 {'Producto': 'Bote rajas verdes 215', 'Tamaño': 5, 'Calidad': 4, 'ID': '5,4'},
 {'Producto': 'Bote rajas verdes 380', 'Tamaño': 4, 'Calidad': 3, 'ID': '4,3'},
 {'Producto': 'Bote rajas verdes 380', 'Tamaño': 3, 'Calidad': 3, 'ID': '3,3'},
 {'Producto': 'Bote rajas verdes 380', 'Tamaño': 4, 'Calidad': 4, 'ID': '4,4'},
 {'Producto': 'Bote rajas verdes 380', 'Tamaño': 3, 'Calidad': 4, 'ID': '3,4'},
 {'Producto': 'Bote rajas verdes 800', 'Tamaño': 3, 'Calidad': 3, 'ID': '3,3'},
 {'Producto': 'Bote rajas verdes 800', 'Tamaño': 2, 'Calidad': 3, 'ID': '2,3'},
 {'Producto': 'Bote rajas verdes 800', 'Tamaño': 3, 'Calidad': 4, 'ID': '3,4'},
 {'Producto': 'Bote rajas verdes 800', 'Tamaño': 2, 'Calidad': 4, 'ID': '2,4'},
 {'Producto': 'Bote rajas verdes 2800','Tamaño': 1,'Calidad': 3,'ID': '1,3'},
 {'Producto': 'Bote rajas verdes 2800','Tamaño': 2,'Calidad': 3,'ID': '2,3'},
 {'Producto': 'Bote rajas verdes 2800','Tamaño': 1,'Calidad': 4,'ID': '1,4'},
 {'Producto': 'Bote rajas verdes 2800','Tamaño': 2,'Calidad': 4,'ID': '2,4'},
 {'Producto': 'Bote rodajas 2800', 'Tamaño': 1, 'Calidad': 2, 'ID': '1,2'},
 {'Producto': 'Bote rodajas 2800', 'Tamaño': 2, 'Calidad': 2, 'ID': '2,2'},
 {'Producto': 'Bote rodajas 800', 'Tamaño': 3, 'Calidad': 2, 'ID': '3,2'},
 {'Producto': 'Bote rodajas 800', 'Tamaño': 4, 'Calidad': 2, 'ID': '4,2'},
 {'Producto': 'Bote rodajas 380', 'Tamaño': 5, 'Calidad': 2, 'ID': '5,2'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 1,'Calidad': 3,'ID': '1,3'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 1,'Calidad': 4, 'ID': '1,4'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 2,'Calidad': 3,'ID': '2,3'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 2,'Calidad': 4,'ID': '2,4'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 3,'Calidad': 3,'ID': '3,3'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 3,'Calidad': 4,'ID': '3,4'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 4,'Calidad': 3,'ID': '4,3'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 4,'Calidad': 4,'ID': '4,4'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 5,'Calidad': 1,'ID': '5,1'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 5,'Calidad': 2,'ID': '5,2'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 5,'Calidad': 3,'ID': '5,3'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 5,'Calidad': 4,'ID': '5,4'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 6,'Calidad': 1,'ID': '6,1'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 6,'Calidad': 2,'ID': '6,2'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 6,'Calidad': 3,'ID': '6,3'},
 {'Producto': 'Bote jalapeños en trozos 215','Tamaño': 6,'Calidad': 4,'ID': '6,4'}
]


# Función para encontrar las combinaciones de productos posibles
def encontrar_combinaciones(tamano, calidad, lista_productos):
    combinaciones = []
    for producto in lista_productos:
        if producto["Tamaño"] == tamano and producto["Calidad"] == calidad:
            combinaciones.append(producto["Producto"])
    return combinaciones

# Llamada a la función con las variables de tamaño y calidad
combinaciones_posibles = encontrar_combinaciones(tamano_chile, calidad_chile, productos)

# Imprimir las combinaciones encontradas
print("Combinaciones de productos posibles:")
for combinacion in combinaciones_posibles:
    print(combinacion)

toneladas