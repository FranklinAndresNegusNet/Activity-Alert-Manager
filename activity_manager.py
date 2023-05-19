from plyer import notification
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QListWidget, QInputDialog
from datetime import datetime, timedelta
import schedule
from schedule import Job
import time
import sys
import threading

class Activity:
    def __init__(self, name, start_time, break_time, end_time):
        self.name = name
        self.start_time = start_time
        self.break_time = break_time
        self.end_time = end_time
        self.job = None

    def alert_start(self):
        notification.notify(title="Alerta de actividad",
                            message=f"Se acerca el tiempo para la actividad: {self.name}",
                            timeout=10)

    def alert_break(self):
        notification.notify(title="Alerta de descanso",
                            message=f"Faltan 5 minutos para descansar de la actividad: {self.name}",
                            timeout=10)

    def alert_resume(self):
        notification.notify(title="Alerta de actividad",
                            message=f"Es hora de retomar la actividad: {self.name}",
                            timeout=10)

    def alert_end(self):
        notification.notify(title="Alerta de actividad",
                            message=f"La actividad {self.name} ha finalizado",
                            timeout=10)

    def schedule_alert(self, alert_time):
        if self.job:
            self.job.cancel()

        self.job = schedule.every().day.at(self.end_time).do(self.alert_end)


    

class ActivityManager:
    def __init__(self):
        self.activities = []

    def add_activity(self, name, start_time, break_time, end_time):
        activity = Activity(name, start_time, break_time, end_time)
        self.activities.append(activity)
        schedule.every().day.at(start_time).do(activity.alert_start)
        schedule.every().day.at((datetime.strptime(start_time, '%H:%M') + timedelta(minutes=break_time - 5)).strftime('%H:%M')).do(activity.alert_break)
        schedule.every().day.at((datetime.strptime(start_time, '%H:%M') + timedelta(minutes=break_time)).strftime('%H:%M')).do(activity.alert_resume)
        schedule.every().day.at(end_time).do(activity.alert_end)
        return activity

    def delete_activity(self, name):
        for activity in self.activities:
            if activity.name == name:
                self.activities.remove(activity)
                return True
        return False

    def view_activities(self):
        return self.activities


class MainWindow(QMainWindow):
    def __init__(self, activity_manager):
        super().__init__()
        self.activity_manager = activity_manager
        self.setWindowTitle("Gestor de Actividades")
        self.setGeometry(200, 200, 500, 300)
        self.initUI()

    def is_valid_time(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False

    def initUI(self):
        self.add_activity_button = QPushButton("Agregar actividad", self)
        self.add_activity_button.move(20, 20)
        self.add_activity_button.clicked.connect(self.add_activity)

        self.delete_activity_button = QPushButton("Eliminar actividad", self)
        self.delete_activity_button.move(200, 20)
        self.delete_activity_button.clicked.connect(self.delete_activity)

        self.add_multiple_activities_button = QPushButton("Agregar múltiples actividades", self)
        self.add_multiple_activities_button.move(20, 260)
        self.add_multiple_activities_button.clicked.connect(self.add_multiple_activities)

        self.resume_activity_button = QPushButton("Reanudar actividad", self)
        self.resume_activity_button.move(200, 260)
        self.resume_activity_button.clicked.connect(self.resume_activity)



        # Añadiendo un botón de salida
        self.exit_button = QPushButton("Salir", self)
        self.exit_button.move(380, 20)
        self.exit_button.clicked.connect(self.close_application)

        self.activity_list = QListWidget(self)
        self.activity_list.move(20, 60)
        self.activity_list.resize(460, 100) # Ajustar el tamaño aquí

        self.update_activity_list()

    # Método para cerrar la aplicación
    def close_application(self):
        self.close()


    def add_activity(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Agregar actividad', 'Nombre de la actividad:')
        if ok:
            start_time, ok = QtWidgets.QInputDialog.getText(self, 'Agregar actividad', 'Hora de inicio (formato 24h, ej: 15:30):')
            if ok and self.is_valid_time(start_time):
                break_time, ok = QtWidgets.QInputDialog.getInt(self, 'Agregar actividad', 'Tiempo de descanso en minutos:', min=1)
                if ok:
                    end_time, ok = QtWidgets.QInputDialog.getText(self, 'Agregar actividad', 'Hora de finalización (formato 24h, ej: 17:30):')
                    if ok and self.is_valid_time(end_time):
                        try:
                            self.activity_manager.add_activity(name, start_time, break_time, end_time)  # Aquí es donde debes incluir end_time
                            self.update_activity_list()
                            self.update_activity_list()
                        except Exception as e:
                            print(f"Ocurrió un error al agregar la actividad: {str(e)}")
                    else:
                        print("La hora de finalización no es válida.")
                else:
                    print("El tiempo de descanso no es válido.")
            else:
                print("La hora de inicio no es válida.")




    def delete_activity(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Eliminar actividad', 'Nombre de la actividad:')
        if ok:
            if self.activity_manager.delete_activity(name):
                self.update_activity_list()

    def add_multiple_activities(self):
        activities_text, ok = QInputDialog.getMultiLineText(self, 'Agregar múltiples actividades', 'Introduce las actividades en el formato: Nombre,Hora de inicio, Tiempo de descanso.\nUna actividad por línea.')
        if ok:
            activities = activities_text.split('\n')
            for activity in activities:
                if activity.strip():  # Aseguramos que la actividad no sea una cadena vacía
                    try:
                        name, start_time, break_time = activity.split(',')
                        if self.is_valid_time(start_time.strip()):
                            try:
                                self.activity_manager.add_activity(name.strip(), start_time.strip(), int(break_time.strip()))
                            except Exception as e:
                                print(f"Ocurrió un error al agregar la actividad: {str(e)}")
                        else:
                            print(f"La hora de inicio de la actividad {name} no es válida.")
                    except ValueError:
                        print(f"El formato de la actividad {activity} no es válido.")
            self.update_activity_list()


    def resume_activity(self):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Reanudar actividad', 'Nombre de la actividad:')
        if ok:
            resume_time, ok = QtWidgets.QInputDialog.getText(self, 'Reanudar actividad', 'Hora de reanudación (formato 24h, ej: 15:30):')
            if ok and self.is_valid_time(resume_time):
                for activity in self.activity_manager.view_activities():
                    if activity.name == name:
                        activity.schedule_alert(resume_time)
            else:
                print("La hora de reanudación no es válida.")


    def update_activity_list(self):
        self.activity_list.clear()
        for activity in self.activity_manager.view_activities():
            self.activity_list.addItem(f"Actividad: {activity.name}, Hora de inicio: {activity.start_time}, Tiempo de descanso: {activity.break_time} minutos")


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    activity_manager = ActivityManager()
    app = QApplication(sys.argv)
    win = MainWindow(activity_manager)
    win.show()
    
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
