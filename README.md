# Proyecto 1 - Procesamiento Digital de Imágenes

## Instrucciones para la instalación de las librerías y la ejecución del juego

### Instalación de virtualenv

El virtualenv nos sirve para aislar las librerías necesarias para la ejecución del juego de otras librerías instaladas en el computador. Para instalar la librería de virtualenv es necesario tener el manejador de paquetes de Python(pip), teniendo pip instalaremos virtualenv con el siguiente comando.

```bash
pip install virtualenv
```

Una vez hayamos instalado el virtualenv, el siguiente paso es crear un ambiente virtual en nuestro proyecto, para esto ejecutaremos el siguiente comando.

```bash
virtualenv pdi_pygame
```

Nota: Es importante ejecutar este comando desde la carpeta root de nuestro proyecto.

Habiendo creado el ambiente virtual, debemos activar dicho ambiente para instalar las librerías, esto lo haremos con el siguiente comando

#### En Windows

```bash
pdi_pygame\Scripts\activate
```

#### En Linux

```bash
source pdi_pygame/bin/activate
```

### Instalación de las librerías

Posteriormente a la activación del ambiente virtual, podremos instalar las librerías de forma aislada de la siguiente forma:

```bash
pip install -r requirements.txt
```

### Ejecución del juego

Finalmente para la ejecución del juego ejecutaremos el siguiente comando:

```bash
python src/index.py
```

Nota: Es importante ejecutar este comando desde la carpeta root de nuestro proyecto.
