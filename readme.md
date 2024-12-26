# Blog App

Este proyecto es una aplicación web desarrollada en Django que permite gestionar un blog, crear autores, categorías y posts, además de realizar búsquedas avanzadas por título, categoría o autor.

**En la página principal o home encontrarás las entradas de este blog.**


## Cómo usar la aplicación

### Si no estás logeado:
Podrás ver los post creados, los autores registrados en la página y la cantidad de posteos que ha realizado cada usuario

### Si creaste una cuenta y estás logeado:

Crear una categoría:
Ve a la sección correspondiente desde la barra de navegación y añade una nueva categoría.

Crear posts:
Desde la sección "Crear Post", completa el formulario con el título, el cuerpo del post y selecciona la categoría deseada.

Mi cuenta:
En esta pestaña podrás editar tus datos personales y cambiar la contraseña.

Buscar posts:
Usa la barra de búsqueda avanzada para filtrar posts por título, categoría o autor.

### Recuerde instalar requirements.txt para utilizar la aplicación e iniciar el servidor con: 

```bash
python runserver.py
```


*Proyecto realizado para la Entrega Final de Python - Coderhouse*


TL;DR: Decidí hacer un estilo minimalista de la página centrándome en la funciones de Python y probando que funcione todo. No quise sobrecargarla con imagenes y estilos. Por otro lado, como ya tenía el proyecto creado y bastante avanzado desde la Preentrega 3, seguí agregando los html y me olvidé de generar una app de Accounts para poder separar los html que son referidos al usuario y los demás html por lo que decidí dejarlo así para no tener que modificar medio proyecto. Espero que esté bien de todas formas.

Por otro lado, decidí agregar el sistema de likes que era un extra.
