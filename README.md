# Siminchik Server

SiminchikServer es un servidor que procesa diversas aplicaciones de la Fundación Siminchikkunarayku (https://www.siminchikkunarayku.pe). Las aplicaciones que procesa actualmente son las siguientes: un Automatic Speech Recognition (Qillqaq), Text-To-Speech (TTS), Recolector de Prompts (Tarpuriq) y el Recolector de Speech Corpus (Huqariq). El servidor puede enviar información a aplicaciones moviles, websites y otras aplicaciones mediante los endpoints que brinda.


**Table of Contents**

- [Prerequisitos](#prerequisitos)
- [Entorno de configuración](#entorno-de-configuración)
- [Instalación de requerimientos](#instalación-de-requerimientos)
- [Qillqaq](#qillqaq)
  - [Usando modelo de lengauje](#usando-modelo-de-lenguaje)
  - [Sin modelo de lenguaje](#sin-modelo-de-languaje)
- [Huqariq](#huqariq)
- [Tarpuriq](#tarpuriq)
- [Servidor en desarrollo](#servidor-en-desarrollo)
- [Servidor en producción](#servidor-en-producción)
  - [Instalación de gunicorn](#instalación-de-gunicorn)
  - [Modo en producción](#modo-en-producción)
- [Recomendaciones](#recomendaciones)
- [Documentación](#documentación)
- [Contacto](#contacto)

## Prerequisitos

* [Python 3.6](https://www.python.org/)
* [SOX](http://sox.sourceforge.net/)
* [MySQL](https://www.mysql.com)

## Entorno de configuración

Configure un entorno virtual y actívelo:

```bash
virtualenv siminchik -p python3
. venv/bin/activate
```

## Instalación de requerimientos

Primero, se debe actualizar el sistema:

```bash
sudo apt-get update
sudo apt-get upgrade
```

Segundo, debe clonar el repositorio

```bash
sudo git clone https://github.com/rjzevallos/SiminchikServer
```

Tercero, instalar los requerimientos usando el archivo requirements.txt

```bash
cd SiminchikServer
sudo pip install -r requirements.txt
```

Cuarto, instalar el parquete de procesamiento de audio ffmpeg

```bash
sudo apt-get install ffmpeg
```

Quinto, creamos una base de datos en mysql

```bash
sudo mysql -p
create database app_quechua;
use app_quechua;
source ../db/siminchik.sql;
```

## Qillqaq

Para poder usar el Automatic Speech Recognition, se debe descargar el modelo entrenado

```bash
sudo wget https://github.com/rjzevallos/QillqaqServer/releases/download/v0.01/5-gram.binary
sudo wget https://github.com/rjzevallos/QillqaqServer/releases/download/v0.01/output_graph.pb
sudo wget https://github.com/rjzevallos/QillqaqServer/releases/download/v0.01/quz_trie
```

## Prueba del modelo

Hay 2 formas de probar el modelo

### Usando el modelo de lenguaje

```bash
deepspeech --model output_graph.pbmm --alphabet quz_alphabet.txt --lm 5-gram.binary --trie quz_trie --audio hatispa.wav
```

### Sin modelo de lenguaje

```bash
deepspeech --model output_graph.pb --alphabet quz_alphabet.txt --audio hatispa.wav
```


## Huqariq

La aplicaciones para recolectar speech corpus cuenta actualmente con alrededor de 4,000 prompts del Quechua Chanca y Collao.
A continuación se muestra la distribución de prompts por cada variedad.


| Variedad             | Cantidad             |
| -------------------- | ---------------------|
| Chanca               | 1428                 |
| Collao               | 2966                 |
| -------------------- | ---------------------|
| Total                | 4394                 |


La cantidad de prompts se recolecta con la aplicación Tarpuriq que se muestra en el apartado siguiente.



## Tarpuriq

La aplicaciones para prompts que sirven como alimento para Huqariq cuenta actualmente con alrededor de 8,000 frases del Quechua Chanca y Collao.
A continuación se muestra la distribución de los textos por cada variedad.


| Variedad             | Cantidad             |
| -------------------- | ---------------------|
| Chanca               | 3887                 |
| Collao               | 3401                 |
| -------------------- | ---------------------|
| Total                | 8288                 |


Los textos que sirven como base para la grabaciones de los prompts fueron recolectados de los diccionarios realizados por el Ministerio de Educación de Perú, asi mismo, por otros diccionarios como el "Diccionario Funcional de Quechua-Ingles" de Clodoaldo Soto Ruiz y el libro "Autobiografía" de Gregorio Condori Mamani.

## Servidor en desarrollo

Con el fin testear el funcionamiento del servidor, el siguiente comando nos permite correr el servidor en modo de desarrollo:

```bash
python server.py
```

## Servidor en producción

### Instalación de gunicorn

Para poder instalar gunicorn necesitamos correr el siguiente comando:

```bash
pip install gunicorn
```

Para verificar si instalamos de forma correcta gunicorn debemos colocar el siguiente comando:

```bash
gunicorn --workers 3 --bind 0.0.0.0:5000 -m 007 wsgi:app
```

### Modo en producción

Con el fin de poner en modo de producción nuestro servidor debemos correr el siguiente comando:

```bash
nohup gunicorn --workers 3 --bind 0.0.0.0:5000 -m 007 wsgi:app
```

## Recommendations

El servidor debe tener las siguientes características: ubuntu 16.04 LTS, 16GB RAM, 125GB SSD.


## Documentación

La documentación se encuenta en el siguiente enlace: https://docs.google.com/document/d/1nOP5HCoASVtoykoC3LNMzKZEPyz-cU86YubEAo4COxw/edit

## Contacto

Estamos felices de poder ayudarlo:

rodolfojoel.zevallos01@estudiant.upf.edu y
camacho.l@pucp.pe
