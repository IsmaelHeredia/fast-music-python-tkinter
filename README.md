# Fast Music

En este proyecto se hizo un completo reproductor de música en Python usando ttkbootstrap para la interfaz gráfica, usa Sqlalchemy para trabajar con una base de datos Sqlite que gestiona la configuración y manejo de multimedia del programa.

Las funciones incorporadas son :

Reproducción de música, videos y streams.
Sincronización de toda la muisca usando Google Drive.
Se pueden descargar uno o varios videos de youtube para convertir en MP3 o MP4 según se necesite.
Permite descargar playlists completas de youtube y convertir en música o videos.
El reproductor registra en la base de datos las ultimas playlists seleccionadas para cargarlas siempre al inicio de la aplicación.  

A continuación se muestran unas imágenes del programa en funcionamiento.

![screenshot]()

Para instalar las dependencias se necesita ejecutar el siguiente comando : 

```
pip install -r requirements.txt
```

Ademas se tienen que crear las credenciales para el servicio "Google Drive API" en la URL https://console.cloud.google.com, una vez creado todo se descargan las credenciales y se guardan en el mismo directorio del programa con el nombre de client_secrets.json.

Una vez configurado todo, se puede ejecutar la aplicación app.py para iniciar el programa, cuando se inicie se debe cargar la ventana "Configuración" y configurar todos los directorios que se necesitan para escanear las canciones y videos, también es necesario especificar el directorio donde están guardadas las canciones en Google Drive y se deben configurar los directorios donde se van almacenar las canciones descargadas. Cuando todos esos datos estén configurados se podrá iniciar el escáner desde ese misma ventana y reproducir cualquier archivo multimedia que se necesite.