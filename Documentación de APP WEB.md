#### crear_mapa

Es la función mas importante por que es la que crea el mapa que luego se lo convierte a HTML.

Va recibir únicamente de parámetro un GeoJson ya concatenado.

**1. Carga del mapa**

Se carga el mapa, para esto usamos la función Map de la librería folium, colocamos la localización de ecuador.

**2. Creación de la capa general de riesgo**

Creamos la capa que va representar el riesgo de inundación. Usamos GeoJson de la librería folium, el cual va recibir:

- GeoJson concatenado.
- función de estilo (color_riesgo).
- función de resaltado (resaltar).
- función de Hover: (la cual es “GeoJsonTooltip” de la librería folium), donde especificamos que las propiedades que va a usar son los tres niveles, luego se le coloca su apodo a los niveles.
- función de pop: (La cual es “GeoJsonPopup” de la librería folium), donde va a recibir el riesgo y el número de inundaciones.
- Luego agregamos la capa de riesgo creada a el mapa usando add_to().

**3. Creación de capas independientes por provincias**

Creamos capas independientes que van a representar el riesgo de inundación por provincias. Para ello aplicamos una logica similar a la capa general del mapa, solo que en este caso se lo hace mediante un bucle for, de la siguiente manera:

- Creamos una variable llamada provincias, la cual obtiene el nombre de todas las provincias presentes en el GeoJSON. Para ello se recorren todas las parroquias, se extrae la propiedad ADM1_ES (provincia) y, mediante un conjunto (set), se eliminan los nombres repetidos. Finalmente, con sorted() se ordenan alfabéticamente.

- Recorremos la lista de provincias con un bucle for. En cada iteración se trabaja únicamente con una provincia.

- Dentro del bucle se crea un nuevo GeoJSON temporal llamado “geojson_provincia”, el cual contiene únicamente las parroquias pertenecientes a la provincia que se está recorriendo. Esto se hace filtrando las características cuyo valor de ADM1_ES coincida con la provincia actual que recorre el bucle.

- Para cada GeoJSON filtrado se crea una nueva capa mediante folium.GeoJson, asignándole como nombre "Provincia: nombre_provincia", de modo que aparezca identificada en el control de capas del mapa.

- A esta nueva capa se le aplican las mismas funciones utilizadas en la capa general:
  - Función de estilo (color_riesgo).
  - Función de resaltado (resaltar).
  - Función Hover (GeoJsonTooltip).
  - Función Popup (GeoJsonPopup).

- Finalmente, cada capa creada se agrega al mapa utilizando el método add_to().

**4. Agregar capas base del mapa**

Agregamos a el mapa con “add_to()” distintas capas de estilos (“calles”, “claro”, “Oscuro”, “Satelite”).

**5. Agregar control de capas**

Se agrega una leyenda flotante dentor del mapa qiue va permitir manipular todas las funciones que hemos agregado a el mapa, esto con “LayerControl” de la librería folium.

**6. Agregar pantalla completa**

Se agrega a el mapa una opción de hacerla pantalla completa, esto con la función “Fullscreen” de folium y “add_to()”.

**7. Retornar mapa en HTML**

Por último se devuelve el mapa con “._repr_html_()” para que este en html listo para usar en la pagina html.
