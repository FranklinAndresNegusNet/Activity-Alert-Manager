Activity Alert Manager

El Activity Alert Manager es una aplicación de escritorio construida con Python y PyQt5 que permite a los usuarios programar alertas para sus actividades diarias. Las actividades pueden tener un tiempo de inicio y un tiempo de descanso, y el programa enviará notificaciones para indicar cuándo comenzar una actividad, cuándo tomar un descanso y cuándo reanudar una actividad.
Uso inicial

    Clona este repositorio en tu máquina local.

bash

git clone https://github.com/yourusername/ActivityAlertManager.git

    Navega al directorio del proyecto y ejecuta activity_manager.py:

bash

cd ActivityAlertManager
python3 activity_manager.py

    En la interfaz de la aplicación, puedes agregar actividades individualmente o en masa. Para cada actividad, necesitarás proporcionar un nombre, una hora de inicio y un tiempo de descanso.

    Una vez que las actividades están programadas, recibirás notificaciones en tu escritorio en los momentos programados.

Tecnologías utilizadas

    Python: El lenguaje de programación principal utilizado para el desarrollo de la aplicación.
    PyQt5: Un conjunto de enlaces de Python para la biblioteca de widgets de la interfaz gráfica de usuario Qt. Se utilizó para construir la interfaz de usuario de la aplicación.
    Schedule: Una biblioteca de Python para la programación de trabajos. Se utilizó para programar las alertas en los momentos especificados.
    Plyer: Una biblioteca de Python para acceder a las características de los dispositivos de hardware. Se utilizó para generar las notificaciones de escritorio.

Contribución

Las contribuciones son siempre bienvenidas. Por favor, lee las pautas de contribución antes de contribuir.
Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.