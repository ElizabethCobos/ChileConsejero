## Librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Chile Consejero",
    page_icon="🌶",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Sidebar
with st.sidebar:
    st.sidebar.image("SanMarcos.png")
    st.title('🌶 Chile Consejero')
    st.subheader('Elige los supuestos con ayuda de los filtros')
    st.write('Decide fácil y rápido la producción')


#######################
# Cargar información

demanda = pd.read_csv("Ventas_reducido.csv")
inventarios = pd.read_csv("Inventario_reducido.csv")
df_limite_inf = pd.read_csv("Limite_inf.csv")
df_limite_sup = pd.read_csv("Limite_sup.csv")
combinaciones = pd.read_csv("Calidad.csv")
escenario_positivo = pd.read_csv("Escenario_positivo.csv")
escenario_negativo = pd.read_csv("Escenario_negativo.csv")

# Algortimo para determinar producción en función de la demanda

# Suponiendo que los dataframes ya están definidos como demada, escenario_positivo y escenario_negativo

def seleccionar_escenario():

    opcion_e = st.selectbox('Seleccione un escenario: ', options= ['Escenario Normal','Escenario Positivo','Escenario Negativo'])

    if opcion_e == 'Escenario Normal':
        escenario = demanda
    elif opcion_e == 'Escenario Positivo':
        escenario = escenario_positivo
    elif opcion_e == 'Escenario Negativo':
        escenario = escenario_negativo
    else:
        print("Opción no válida. Por favor, intente de nuevo.")
        return seleccionar_escenario()

    return escenario

# Llamar a la función y almacenar el resultado en la variable escenario
escenario = seleccionar_escenario()

# Selección del mes
# Lista de meses válidos
opcion_m = st.selectbox('Seleccione un mes: ', options= ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"])
mes = opcion_m

opcion_p = st.selectbox('Seleccione un producto: ', options= ["Bote jalapeños 215", "Bote jalapeños 380","Bote jalapeños 780", "Bote jalapeños 2800", "Bote rajas verdes 105", "Bote rajas verdes 215", "Bote rajas verdes 380", "Bote rajas verdes 800"
,"Bote rajas verdes 2800", "Bote rodajas 380", "Bote rodajas 800", "Bote rodajas 2800", "Bote jalapeños en trozos 215"])

producto_elegido = opcion_p

#DIFERENCIA ENTRE DEMANDA DEL PRODUCTO E INVENTARIO

def calcular_diferencia_dataframe(mes, producto_elegido, escenario, inventarios, df_limite_inf, df_limite_sup):
# Convertir el nombre del mes a título para coincidir con las columnas del dataframe
    mes = mes.title()

    # Verificar si el producto está en ambos dataframes
    if producto_elegido in escenario['Producto'].values and producto_elegido in inventarios['Producto'].values:
        # Obtener la demanda y el inventario para el producto y mes seleccionados
        demanda_producto = escenario.loc[escenario['Producto'] == producto_elegido, mes].values[0]
        inventario_producto = inventarios.loc[inventarios['Producto'] == producto_elegido, mes].values[0]

        # Calcular la diferencia
        diferencia = demanda_producto - inventario_producto

        # Obtener el límite_inf de la tabla según el producto y el mes
        limite_producto_mes_inf = df_limite_inf.loc[df_limite_inf['Producto'] == producto_elegido, mes].values[0]
        limite_producto_mes_sup = df_limite_sup.loc[df_limite_sup['Producto'] == producto_elegido, mes].values[0]

         # Mensaje de alta producción para los meses de Junio, Julio y Agosto
        if mes in ['Junio', 'Julio', 'Agosto']:
            st.header('Produce: Mes de alta producción')
            st.write(f'La demanda es de:  {demanda_producto}.  El Inventario es de: {inventario_producto}.   Si produces, el inventario restante será:  {diferencia}')
            st.write(f'Recuerda que tus limites de inventario son:  Limite Inferior: {limite_producto_mes_inf}  Límite superior: {limite_producto_mes_sup}')

        # Verificar si la diferencia es menor a 0
        if diferencia < 0 and mes not in ['Junio', 'Julio', 'Agosto']:
            st.header("No Producir")
            st.write(f'La demanda es de:  {demanda_producto}.  El Inventario es de: {inventario_producto}.  Si produces, el inventario restante será:  {diferencia}')
            st.write(f'Recuerda que tus limites de inventario son:   Limite Inferior: {limite_producto_mes_inf}  Límite superior: {limite_producto_mes_sup}')

        # Verificar si la diferencia es mayor a 0 y menor al límite
        elif 0 < diferencia < limite_producto_mes_inf:
            st.header("Produce")
            st.write(f'La demanda es de:  {demanda_producto}.  El Inventario es de: {inventario_producto}.   Si produces, el inventario restante será:  {diferencia}')
            st.write(f'Recuerda que tus limites de inventario son:   Limite Inferior: {limite_producto_mes_inf}   Límite superior: {limite_producto_mes_sup}')
            
        elif diferencia > limite_producto_mes_sup:
            st.header("La demanda supera al inventario disponible y al limite superior")
            st.write(f'La demanda es de:  {demanda_producto}.   El Inventario es de: {inventario_producto}.   Si produces, el inventario restante será:  {diferencia}')
            st.write(f'Recuerda que tus limites de inventario son:   Limite Inferior: {limite_producto_mes_inf}   Límite superior: {limite_producto_mes_sup}')
        else:
            st.write(f'Diferencia positiva, pero excede el limite, Demanda: {demanda_producto}, Inventario: {inventario_producto}, Diferencia: , {diferencia}, Limite inferior: {limite_producto_mes_inf}, Límite superior: {limite_producto_mes_sup}')
    else:
        st.header("Producto no encontrado en los dataframes.")

# Ejemplo de uso de la función con el dataframe 'limite' incluido:
resultado = calcular_diferencia_dataframe(mes, producto_elegido, escenario, inventarios, df_limite_inf, df_limite_sup)
#st.header(resultado)

#Seleccionar la tamaño del chile
def select_t():

    opcion_tam = st.selectbox('Seleccione un tamaño: ', options= ["Grande-Grande","Grande-Mediano","Grande-Chico","Chico-Grande","Chico-Mediano","Chico-Chico"])

    if opcion_tam == 'Grande-Grande':
        tamano_chile = 1
    elif opcion_tam == 'Grande-Mediano':
        tamano_chile = 2
    elif opcion_tam == 'Grande-Chico':
        tamano_chile = 3
    elif opcion_tam == 'Chico-Grande':
        tamano_chile = 4
    elif opcion_tam == 'Chico-Mediano':
        tamano_chile = 5
    elif opcion_tam == 'Chico-Chico':
        tamano_chile = 6

    return tamano_chile

# Llamar a la función y almacenar el resultado en la variable escenario
tamano_chile = select_t()

#Seleccionar la tamaño del chile
def select_cal():

    opcion_cal = st.selectbox('Seleccione la Calidad: ', options= ['Excelente Calidad', 'No Plagado','Plagado', 'Mala Calidad'])

    if opcion_cal == 'Excelente Calidad':
        calidad_chile = 1
    elif opcion_cal == 'No plagado':
        calidad_chile = 2
    elif opcion_cal == 'Plagado':
        calidad_chile = 3
    elif opcion_cal == 'Mala Calidad':
        calidad_chile = 4

    return calidad_chile

# Llamar a la función y almacenar el resultado en la variable escenario
calidad_chile = select_cal()

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
def encontrar_combinaciones(tamano_chile, calidad_chile, lista_productos):
    combinaciones = []
    for producto in lista_productos:
        if producto["Tamaño"] == tamano_chile and producto["Calidad"] == calidad_chile:
            combinaciones.append(producto["Producto"])
    return combinaciones

# Llamada a la función con las variables de tamaño y calidad
combinaciones_posibles = encontrar_combinaciones(tamano_chile, calidad_chile, productos)
lista_combinaciones = []
# Imprimir las combinaciones encontradas
st.header("Combinaciones de productos posibles:")
for combinacion in combinaciones_posibles:
    print(combinacion)
    lista_combinaciones.append(combinacion)
st.write(combinaciones_posibles) 
