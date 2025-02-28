# Fast Music

En este proyecto se hizo un completo reproductor de música en Python usando ttkbootstrap para la interfaz gráfica, usa Sqlalchemy para trabajar con una base de datos Sqlite que gestiona la configuración y manejo de multimedia del programa.

Las funciones incorporadas son :

Reproducción de música, videos y streams.

Sincronización de toda la muisca usando Google Drive.

Se pueden descargar uno o varios videos de youtube para convertir en MP3 o MP4 según se necesite.

Permite descargar playlists completas de youtube y convertir en música o videos.

El reproductor registra en la base de datos las ultimas playlists seleccionadas para cargarlas siempre al inicio de la aplicación.  

A continuación se muestran unas imágenes del programa en funcionamiento.

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgb9brE_yKhaW3KzZxMIBCwQMIdduBPR0WOmHA2nMPu6DqnoeiXmQwD-SfgxFrvMwRMqPYd1YZH0zefaa70dAGjT9hI21GemZoSb6MQ3mtb1kQN83UgLljVv82siJtkbd8pxfoQ0VLncr7jaEb5f8BvX4KvNUtXLwPKOrp4HTpOp95pc0QJJ8zXkVxOyfY/s1247/1.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhLPF1LgpdxcCzoyHEQRvaAF52bSD2eL_beyKUE8p3tA8PO3DSR_HwUjiBXt8PHFh_uT8RFLMGAoWQ8C-hZmHSq0PMxektBSehoYGE-Ct8ETJm6XkEcuKFBen1SvJI5I2qRg00n9pF5gdbGoi-7007AjvJAR5SqbBgIY1GwFv2AdhBOEOiENSSKvh7Ltew/s1250/2.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjfcnS9bP0N77dRPQGBeGgPnvuZs4fRYr48YPQ1kHUiPM30Y0-rom3EYw9zUTiJi4xT7ne3wWDqTnXSOsTOsHuV-xg_1KO-0D-_nJCoeXYEns4F1FG4yoiJz5tRkr3Jo07dj__wqW8AUjk24pQtEkhh95_e6xnEAmZnr-2sY5rDLdEkCbKAfFL_SFKqFfk/s1249/3.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiIQgYkts9kG-Fcaul777FrMLZFcBQxej010g-CM4qhyphenhyphenCXcFeSate3it8G6_MlduSZ-1XZADtfSRIT7H7IX8Umu7c_c7OetNDKfT_gc3r23XDCm9tFqg4D0opHce5Qybt5Crb1Ne38jOjqn_FkwFNR5GeBxL4vrq24ETl4gLDB49Dncjfrp3Wme9MgpkWI/s1252/4.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjXiucO-w3CWpMVOFJWbYW_ri1Stcbi9HOIAoAh0M4jLdVrY5_cKAniTicwtntn9pReFwgLgHn4CW-OQ4WW-UUwwKMLaxBvnVGyb7BW7UqCQMLWaoN91-uvqpLdmnJiIbVqQslKv_DXK6ZlJx3ZpDM0GW5oB3lC7wLsWp1vv92MSI6eyviFbUQcC_nbBiY/s1248/5.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhz1hfzcMk4CHkXoDk9BPWSVvm04yEkw8AajUTKMZzO3YAlGSpXrwbhsZskH8bISzxD4BMF94DtjCos4SozNU5xRJ5nneNUBc4ZYbyOjbFLL7IygYyuzg_T3_hx0lDHzdcqi2z4z3tALiO-yE3mU38VtORo7ukW07KzKeJVSRMP6f24DI71oSpIJk9hBj4/s1252/6.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEifZlXEj7d-ltC-LIxho90kboG_fPGAGugIJtCTlehodUyhHZKcC3A9XyIDql4nV1XN_nh5NH7Jvm9s96OZlRAvPJKbdEDAG5_UJXeagRGd_E9TGESdlQO-pkMEonV4Yt8s0MolV5xEzIjyQ38bzC-m2X1NQILJkjZGenkfYuML0SEQOv-_p3drB66PMTM/s1251/7.png)

![screenshot](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjLuudDGRjOvENKaWC9XC81W7sHHNl4BBtPLVLEpekCue7xFGbIDf5h6KkrczUG5lpxwOZ-iXy22IzvMYwfZPJ338T-WRJ6E1f3hZdNLo4Nm4c_FKDxZeYolIVzIY_XXpN4IclnKC5zDJBJyMifmas0MkUpYq2-pFNQD0LWKAWZO6L8vmzQytpibPPkNH8/s899/8.png)

Para instalar las dependencias se necesita ejecutar el siguiente comando : 

```
pip install -r requirements.txt
```

Ademas se tienen que crear las credenciales para el servicio "Google Drive API" en la URL https://console.cloud.google.com, una vez creado todo se descargan las credenciales y se guardan en el mismo directorio del programa con el nombre de client_secrets.json.

Una vez configurado todo, se puede ejecutar la aplicación app.py para iniciar el programa, cuando se inicie se debe cargar la ventana "Configuración" y configurar todos los directorios que se necesitan para escanear las canciones y videos, también es necesario especificar el directorio donde están guardadas las canciones en Google Drive y se deben configurar los directorios donde se van almacenar las canciones descargadas. Cuando todos esos datos estén configurados se podrá iniciar el escáner desde ese misma ventana y reproducir cualquier archivo multimedia que se necesite.