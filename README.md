Activity Alert Manager

Activity Alert Manager is a desktop application built in Python that allows users to schedule alerts for different activities and breaks. With this application, users can add activities with their respective start times and break durations. Alerts are triggered to notify users when an activity is about to start, when break time is approaching, and when it is time to resume an activity after the break.

Clone this repository on your local machine.

bash

git clone https://github.com/FranklinAndresNegusNet/Activity-Alert-Manager.git

Navigate into the project directory and run activity_manager.py:

bash

cd ActivityAlertManager
python3 activity_manager.py

In the application interface, you can add activities individually or in bulk. For each activity, you will need to provide a name, a start time, and a break time.

Once the activities are scheduled, you will receive notifications on your desktop at the scheduled times.

Technologies Used

    Python: The main programming language used for developing the application.
    PyQt5: A set of Python bindings for Qt library's GUI widgets. It was used to build the application's user interface.
    Schedule: A Python library for job scheduling. It was used to schedule the alerts at specified times.
    Plyer: A Python library for accessing features of hardware devices. It was used to generate the desktop notifications.

Contributing

Contributions are always welcome. Please read the contribution guidelines before contributing.
License

This project is licensed under the MIT License. See the LICENSE file for more details.
