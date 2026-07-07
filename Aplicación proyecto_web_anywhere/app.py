from flask import Flask, render_template
import pandas as pd
import folium
import json
from folium.plugins import Fullscreen #Encargada de pantalla completa
import os

#Para obtener rutas absolutas relativas al proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Corriendo HTML
app = Flask(__name__)

#Funcion para colocar color a las capas segun el nivel de riesg
def color_riesgo(feature):

    #Obtierne el valor de riesgo de una parroquia y si no existe se le coloca la etiqueta de sin datos
    riesgo = feature["properties"].get("riesgo", "Sin datos")

    colores = {
        "Nulo": "#4CAF50",
        "Bajo": "#FFFF00",
        "Medio": "#FFA500",
        "Alto": "#FF0000",
        "Sin datos": "#BDBDBD"
    }

    return {
        "fillColor": colores[riesgo],
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7
    }

#Funcion para resaltar parroquias cuando se pase el cursor
def resaltar(feature):
    return {
        "weight": 2.5,
        "color": "#14212B",
        "fillOpacity": 0.9,
    }

#Datos
#Funcion para cargar tanto el GeoJson como las preidcciones.Las combina en un solo GeoJson
def cargar_datos(ruta_geojson, ruta_predicciones):
    # Cargando GeoJson de párroquias
    with open(ruta_geojson, encoding="utf-8") as f:
        geojson = json.load(f)

    # Leyendo CSV de predicciones
    predicciones = pd.read_csv(ruta_predicciones, usecols= ["DPA_DESPAR","DPA_DESCAN","DPA_DESPRO","num_inundaciones","riesgo_inundacion"])

    # Renombrando columnas para que coincidan con el GeoJson
    predicciones = predicciones.rename(columns={
        "DPA_PARROQ": "ADM3_PCODE",
        "DPA_DESPAR": "ADM3_ES",
        "DPA_DESCAN": "ADM2_ES",
        "DPA_DESPRO": "ADM1_ES"
    })

    # Uniendo CSV con GeoJson
    pred = predicciones.set_index(["ADM1_ES", "ADM2_ES", "ADM3_ES"])

    for feature in geojson["features"]:
        props = feature["properties"]

        key = (
            props["ADM1_ES"],
            props["ADM2_ES"],
            props["ADM3_ES"]
        )

        if key in pred.index:
            props["riesgo"] = pred.loc[key, "riesgo_inundacion"]
            props["numero inundaciones"] = pred.loc[key, "num_inundaciones"]

    return geojson

#Funcion para calcular la cantidad de parroquias por Nivel de riesgo
def calcular_estadisticas(geojson):

    orden_riesgo = ["Alto", "Medio", "Bajo", "Nulo", "Sin datos"]

    # Inicializar el contador
    conteo = {nivel: 0 for nivel in orden_riesgo}

    # Contar parroquias por nivel de riesgo
    for feature in geojson["features"]:
        riesgo = feature["properties"].get("riesgo", "Sin datos")
        conteo[riesgo] += 1

    return conteo

#Funcion para crear mapa, recibe el GeoJson ya preparado
def crear_mapa(geojson):
    # Cargando Mapa
    mapa = folium.Map(
        location=[-1.8312, -78.1834],  # Latitud y longitud de Ecuador
        zoom_start=7,
        tiles=None,
        control_scale=True #Indica la cantidad de mtros desde donde se visualiza
    )


    # Crear la capa GeoJSON que representa el riesgo de inundación
    capa_riesgo = folium.GeoJson(
        geojson,
        name="Capa de riesgo",
        style_function=color_riesgo,
        highlight_function=resaltar, #No es necesario especificar parametros Folium llama la funcion por cada feature
        tooltip=folium.GeoJsonTooltip(
            fields=[
                "ADM3_ES",
                "ADM2_ES",
                "ADM1_ES"
            ],
            aliases=[
                "Parroquia:",
                "Cantón:",
                "Provincia:"
            ],
            sticky=False
        ),

        popup=folium.GeoJsonPopup(
            fields=[
                "riesgo",
                "numero inundaciones"
            ],
            aliases=[
                "Riesgo de inundación:",
                "Número de inundaciones"
            ]
        )
    )

    #Luego agregamos la capa de riesgo en el mapa
    capa_riesgo.add_to(mapa)

    #Estilos de mapa Seleccionables
    folium.TileLayer("OpenStreetMap",name="Calles").add_to(mapa)
    folium.TileLayer("CartoDB Positron",name="Claro").add_to(mapa)
    folium.TileLayer("CartoDB Dark_Matter",name="Oscuro").add_to(mapa)
    folium.TileLayer("Esri.WorldImagery", name="Satélite").add_to(mapa)

    #Con esta linea se agrega un opcion que permite escoger el tipos de estilos o visualizaciones
    folium.LayerControl(collapsed=False).add_to(mapa)

    Fullscreen(
        position="topleft",
        title="Pantalla completa",
        title_cancel="Salir"
    ).add_to(mapa) #Se agrega la opcion de pantalla completa a el mapa

    return mapa._repr_html_()


#USANDO FUNCIONES:

#Cargando datos
geojson_ruta = os.path.join(BASE_DIR, "parroquias_ecuador.geojson")
predicciones_ruta = os.path.join(BASE_DIR, "dataset.csv")
geojson_preparado= cargar_datos(ruta_geojson= geojson_ruta, ruta_predicciones= predicciones_ruta)

#Calculando estadisticas
estadisticas = calcular_estadisticas(geojson_preparado)

#Creando mapa
mapa = crear_mapa(geojson_preparado)

"""El decorador @app.route("/") indica que la función que aparece debajo ("inicio()")
se ejecutará cuando un usuario visite la ruta raíz de la aplicación."""
@app.route("/")

#Es la funcion que genera la pagina principal que vera el usuario
def inicio():
    #"render_template()" carga el archivo y reemplaza las expresiones de Jinja con los datos enviados desde Python.
    return render_template(
        "index.html",
        mapa= mapa,
        stats= estadisticas
    )


if __name__ == "__main__":
    #Aquí se obtiene el puerto donde se ejecutará la aplicación.
    puerto = int(os.environ.get("PORT", 5000))
    # App.run inica el servidor Flask
    # host="0.0.0.0" -> abierto para todas las interfaces de red
    # port=puerto -> Indica el puerto donde escuchará la aplicación.
    # debug=False -> Desactiva el modo de depuración.
    app.run(host="0.0.0.0", port=puerto, debug=False)

