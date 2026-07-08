# Clasificación del Riesgo de Inundación en Ecuador

Aplicación web desarrollada con Flask y Python para visualizar el riesgo de inundación por parroquias del Ecuador mediante un mapa interactivo.

## Estructura del proyecto
```text
Aplicación_proyecto_web_anywhere/
│
├── app.py                      # Aplicación principal Escrita en Python
├── dataset.csv                 # Datos utilizados
├── parroquias_ecuador.geojson  # GeoJson de parroquias del Ecuador
├── requirements.txt            # Dependencias del proyecto
│
├── static/
│   └── UG_logo.png             # Logo utilizado en la interfaz HTML
│
└── templates/
    └── index.html              # Página escrita en HTML
```
## Requisitos

- python 3.10 o superior (se recomienda Python 3.10)
- pip (administrador de paquetes de Python)

## Instalación

Desde una terminal en un directorio de windows, siga los siguientes pasos:
(para ello es necesario tener instalado git)

1. Clonar el repositorio

```bash
git clone https://github.com/Manuel-Orellana/Proyecto-riesgo-Inundaciones-Grupo-B.git
```

2. Entrar al proyecto

```bash
cd Proyecto-riesgo-Inundaciones-Grupo-B

cd "Aplicación proyecto_web_anywhere"
```

3. Crear y activar un venv:
```bash
python -m venv venv ó py -3.10 -m venv venv

.\venv\Scripts\Activate.ps1
```

4. Instalar las dependencias en el venv:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

Luego abre el navegador en:

```
http://127.0.0.1:5000/
```

## Tecnologías utilizadas

- Python
- Flask
- HTML
- GeoJSON
- CSV
- CSS (De manera interna en el HTML)

## Autores

- Manuel Elías Orellana Lavayen
- Diego Antony Murillo Alvarado
- Hernán Andrés Pilozo Rodríguez
- Kelly Naomi Medina Guallo
- Ian Erick López Llorentty
- Miguel Alejandro Yglesias Alvea
- Dario Ramon Robles Ponce
