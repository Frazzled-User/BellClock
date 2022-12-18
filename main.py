import sys
import os
import requests
import json
from PyQt5.QtCore import QTime, QTimer, QDate, QCoreApplication, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QLabel, QTextEdit
from PyQt5.uic import loadUi

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi(resource_path("homescreen-bellclock.ui"), self)
        self.examStartClockButton.clicked.connect(self.examclockscreen)
        self.StartClockButton.clicked.connect(self.gotoclockscreen)
        self.EarlyStartClockButton.clicked.connect(self.earlyclockscreen)
        self.EODMessageScreenButton.clicked.connect(self.eodmessagescreen)
        self.quitappbutton.clicked.connect(QCoreApplication.instance().quit)
        self.moreinfo.clicked.connect(self.moreinfoscreen)
        self.plainStartClockButton.clicked.connect(self.plainclockscreen)

    def gotoclockscreen(self):
        widget.setCurrentIndex(1)
    def examclockscreen(self):
        widget.setCurrentIndex(2)
    def earlyclockscreen(self):
        widget.setCurrentIndex(3)
    def eodmessagescreen(self):
        widget.setCurrentIndex(4)
    def plainclockscreen(self):
        widget.setCurrentIndex(6)
    def moreinfoscreen(self):
        widget.setCurrentIndex(7)


class ClockScreen(QDialog): # this class is for the standard bell schedule
    def __init__(self):
        super(ClockScreen, self).__init__()
        loadUi(resource_path("clockmain.ui"), self)
        self.API_KEY = "964dc5e3ee5213039c28f742919525e8"
        self.CITY = "Hillsborough County"
        self.initial_ttimer = QTimer()
        self.initial_ttimer.setSingleShot(True)
        self.initial_ttimer.timeout.connect(self.update_time)
        self.initial_ttimer.start(0)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.initial_timer = QTimer()
        self.initial_timer.setSingleShot(True)
        self.initial_timer.timeout.connect(self.update_weather)
        self.initial_timer.start(0)
        self.weather_timer = QTimer()
        self.weather_timer.setInterval(60000)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start()
        self.periodchange.setVisible(False)
        self.gobackhome.clicked.connect(self.back_to_home)
        self.belltimes = {
            "08:30": "Go to Block 11/21",
            "09:55": "Go to Homeroom",
            "10:09": "Go to Block 12/22",
            "11:39": "Go to A Lunch",
            "12:13": "Go to Block 13/23",
            "12:43": "Go to B Lunch Electives",
            "13:02": "C Lunch Electives End",
            "13:37": "B Lunch Electives End",
            "13:45": "Go to Block 14/24",
            "15:25": "Go HOME",
            "15:28": " "
        }

    def update_time(self):
        # shows the time
        time = QTime.currentTime()
        time_str = time.toString("hh:mm:ss AP")
        time_hm = time.toString('hh:mm')
        self.timedisplay.setText(time_str)
        current_date = QDate.currentDate()
        date_str = current_date.toString("ddd MM/dd/yyyy")
        self.datedisplay.setText(date_str)
        for time, message in self.belltimes.items():
            if time == time_hm:
                self.periodchange.setText(message)
                self.periodchange.setVisible(True)
                break
            else:
                self.periodchange.setVisible(False)
        for time, message in self.belltimes.items():
            if self.periodchange.text() == "Go HOME" and widget.currentIndex() == 1:
                widget.setCurrentIndex(5)
            elif self.periodchange.text() == " " and widget.currentIndex() == 5:
                widget.setCurrentIndex(1)
        for time, message in self.belltimes.items():
            if self.periodchange.text() == " ":
                self.periodchange.setVisible(False)

    def update_weather(self):
        # updates the "tempdisplay" label to show the current temperature
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)
        temperature = response_dict["main"]["temp"]
        rounded_temperature = round(temperature)
        self.tempdisplay.setText(f"{rounded_temperature} F")
        # updates the "precipdisplay" label to show the current weather
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)
        weather_conditions = response_dict["weather"][0]
        current_condition = weather_conditions["main"]
        self.precipdisplay.setText(current_condition)

    def back_to_home(self):
            widget.setCurrentIndex(0)

class EarlyClockScreen(QDialog): # This class is for the Early Bell Schedule
    def __init__(self):
        super(EarlyClockScreen, self).__init__()
        self.datedisplay = None
        self.timedisplay = None
        loadUi(resource_path("earlyclockmain.ui"), self)
        self.API_KEY = "964dc5e3ee5213039c28f742919525e8"
        self.CITY = "Hillsborough County"
        self.initial_ttimer = QTimer()
        self.initial_ttimer.setSingleShot(True)
        self.initial_ttimer.timeout.connect(self.update_time)
        self.initial_ttimer.start(0)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.initial_timer = QTimer()
        self.initial_timer.setSingleShot(True)
        self.initial_timer.timeout.connect(self.update_weather)
        self.initial_timer.start(0)
        self.weather_timer = QTimer()
        self.weather_timer.setInterval(60000)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start()
        self.periodchange.setVisible(False)
        self.gobackhome.clicked.connect(self.back_to_home)
        self.belltimes = {
            "08:30": "Go to Block 11/21",
            "09:45": "Go to Homeroom",
            "09:54": "Go to Block 12/22",
            "11:06": "Go to A Lunch",
            "11:40": "Go to Block 13/23",
            "12:10": "Go to B Lunch Electives",
            "12:20": "C Lunch Electives End",
            "12:55": "B Lunch Electives End",
            "13:00": "Go to Block 14/24",
            "14:25": "Go HOME",
            "14:28": " "
        }

    def update_time(self):
        # shows the time
        time = QTime.currentTime()
        time_str = time.toString("hh:mm:ss AP")
        time_hm = time.toString('hh:mm')
        self.timedisplay.setText(time_str)
        current_date = QDate.currentDate()
        date_str = current_date.toString("ddd MM/dd/yyyy")
        self.datedisplay.setText(date_str)
        for time, message in self.belltimes.items():
            if time == time_hm:
                self.periodchange.setText(message)
                self.periodchange.setVisible(True)
                break
            else:
                self.periodchange.setVisible(False)
        for time, message in self.belltimes.items():
            if self.periodchange.text() == "Go HOME" and widget.currentIndex() == 3:
                widget.setCurrentIndex(5)
            elif self.periodchange.text() == " " and widget.currentIndex() == 5:
                widget.setCurrentIndex(3)
        for time, message in self.belltimes.items():
            if self.periodchange.text() == " ":
                self.periodchange.setVisible(False)




    def update_weather(self):
            # updates the "tempdisplay" label to show the current temperature
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
            response = requests.get(api_url)
            response_dict = json.loads(response.text)
            temperature = response_dict["main"]["temp"]
            rounded_temperature = round(temperature)
            self.tempdisplay.setText(f"{rounded_temperature} F")
            # updates the "precipdisplay" label to show the current weather
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
            response = requests.get(api_url)
            response_dict = json.loads(response.text)
            weather_conditions = response_dict["weather"][0]
            current_condition = weather_conditions["main"]
            self.precipdisplay.setText(current_condition)# This class is for the Early Bell Schedule

    def back_to_home(self):
            widget.setCurrentIndex(0)

class ExamClockScreen(QDialog): # This class is for the Exam Bell Schedule
    def __init__(self):
        super(ExamClockScreen, self).__init__()
        self.datedisplay = None
        self.timedisplay = None
        loadUi(resource_path("examclockmain.ui"), self)
        self.API_KEY = "964dc5e3ee5213039c28f742919525e8"
        self.CITY = "Hillsborough County"
        self.initial_ttimer = QTimer()
        self.initial_ttimer.setSingleShot(True)
        self.initial_ttimer.timeout.connect(self.update_time)
        self.initial_ttimer.start(0)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.initial_timer = QTimer()
        self.initial_timer.setSingleShot(True)
        self.initial_timer.timeout.connect(self.update_weather)
        self.initial_timer.start(0)
        self.weather_timer = QTimer()
        self.weather_timer.setInterval(60000)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start()
        self.periodchange.setVisible(False)
        self.gobackhome.clicked.connect(self.back_to_home)
        self.belltimes = {
            "08:30": "Exam 1 Start",
            "10:30": "Exam 1 End",
            "10:40": "Exam 2 Start",
            "12:40": "Go HOME",
            "12:43": " "
        }
        
    def update_time(self):
        # shows the time
        time = QTime.currentTime()
        time_str = time.toString("hh:mm:ss AP")
        time_hm = time.toString('hh:mm')
        self.timedisplay.setText(time_str)
        current_date = QDate.currentDate()
        date_str = current_date.toString("ddd MM/dd/yyyy")
        self.datedisplay.setText(date_str)
        for time, message in self.belltimes.items():
            if time == time_hm:
                self.periodchange.setText(message)
                self.periodchange.setVisible(True)
                break
            else:
                self.periodchange.setVisible(False)
        for time, message in self.belltimes.items():
            if self.periodchange.text() == "Go HOME" and widget.currentIndex() == 2:
                widget.setCurrentIndex(5)
            elif self.periodchange.text() == " " and widget.currentIndex() == 5:
                widget.setCurrentIndex(2)
        for time, message in self.belltimes.items():
            if self.periodchange.text() == " ":
                self.periodchange.setVisible(False)

    def update_weather(self):
        # updates the "tempdisplay" label to show the current temperature
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)
        temperature = response_dict["main"]["temp"]
        rounded_temperature = round(temperature)
        self.tempdisplay.setText(f"{rounded_temperature} F")
        # updates the "precipdisplay" label to show the current weather
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)
        weather_conditions = response_dict["weather"][0]
        current_condition = weather_conditions["main"]
        self.precipdisplay.setText(current_condition)

    def back_to_home(self):
            widget.setCurrentIndex(0)

class PlainClock(QDialog):
    def __init__(self):
        super(PlainClock, self).__init__()
        loadUi(resource_path("plainclockmain.ui"), self)
        self.API_KEY = "964dc5e3ee5213039c28f742919525e8"
        self.CITY = "Hillsborough County"
        self.initial_ttimer = QTimer()
        self.initial_ttimer.setSingleShot(True)
        self.initial_ttimer.timeout.connect(self.update_time)
        self.initial_ttimer.start(0)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)
        self.timer.start()
        self.initial_timer = QTimer()
        self.initial_timer.setSingleShot(True)
        self.initial_timer.timeout.connect(self.update_weather)
        self.initial_timer.start(0)
        self.weather_timer = QTimer()
        self.weather_timer.setInterval(60000)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start()
        self.gobackhome.clicked.connect(self.back_to_home)

    def update_time(self):
        # shows the time
        time = QTime.currentTime()
        time_str = time.toString("hh:mm:ss AP")
        time_hm = time.toString('hh:mm')
        self.timedisplay.setText(time_str)
        current_date = QDate.currentDate()
        date_str = current_date.toString("ddd MM/dd/yyyy")
        self.datedisplay.setText(date_str)

    def update_weather(self):
        # updates the "tempdisplay" label to show the current temperature
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)
        temperature = response_dict["main"]["temp"]
        rounded_temperature = round(temperature)
        self.tempdisplay.setText(f"{rounded_temperature} F")
        # updates the "precipdisplay" label to show the current weather
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={self.CITY}&appid={self.API_KEY}&units=imperial"
        response = requests.get(api_url)
        response_dict = json.loads(response.text)
        weather_conditions = response_dict["weather"][0]
        current_condition = weather_conditions["main"]
        self.precipdisplay.setText(current_condition)

    def back_to_home(self):
        widget.setCurrentIndex(0)

class InfoScreen(QDialog):
    def __init__(self):
        super(InfoScreen, self).__init__()
        loadUi(resource_path("infoscreen.ui"), self)
        self.gobackhome.clicked.connect(self.back_to_home)

    def back_to_home(self):
            widget.setCurrentIndex(0)

message1 = " "

class EODMessageScreen(QDialog):
    def __init__(self):
        super(EODMessageScreen, self).__init__()
        loadUi(resource_path("EODMessage.ui"), self)
        self.gobackhome.clicked.connect(self.back_to_home)
        self.saveButton.clicked.connect(self.save_message)

    def save_message(self):
        global message1
        message1 = self.eodmessageinput.toPlainText()
        self.eod_screen = EODScreen()
        self.eod_screen.show()
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.eod_screen.close)
        self.timer.start(3000)  # 3 seconds

    def back_to_home(self):
        widget.setCurrentIndex(0)


class EODScreen(QDialog):
    def __init__(self):
        super(EODScreen, self).__init__()
        loadUi(resource_path("EODscreen.ui"), self)
        eod_message_screen = EODMessageScreen()
        global message1
        self.eodMessageLabel.setText(message1)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_message)
        self.timer.start()
        self.Utimer = QTimer()
        self.Utimer.setInterval(1000)
        self.Utimer.timeout.connect(self.remindervisibility)
        self.Utimer.start()

    def update_message(self):
        if eod_message_screen.isVisible() == True:
            global message1
            eodmessage = message1
            self.eodMessageLabel.setText(eodmessage)
        else:
            return None

    def remindervisibility(self):
        if self.eodMessageLabel.text() == " " and self.eodMessageLabel.isVisible() == True:
            self.eodMessageLabel.setVisible(False)
            self.label.setVisible(False)
            self.label_2.setGeometry(440, 356, 1041, 291)
        elif self.eodMessageLabel.text() != " " and self.eodMessageLabel.isVisible() == False:
            self.eodMessageLabel.setVisible(True)
            self.label.setVisible(True)
            self.label_2.setGeometry(440, 50, 1041, 291)

# main
app = QApplication(sys.argv)
widget = QStackedWidget()
# Home Screen
Home = HomeScreen()
widget.addWidget(Home)
# Clock Screen
clock_screen = ClockScreen()
widget.addWidget(clock_screen)
# Exam Clock Screen
exam_clock_screen = ExamClockScreen()
widget.addWidget(exam_clock_screen)
# Early Clock Screen
early_clock_screen = EarlyClockScreen()
widget.addWidget(early_clock_screen)
# EOD Message input Screen
eod_message_screen = EODMessageScreen()
widget.addWidget(eod_message_screen)
# EOD Message display screen
eod_screen = EODScreen()
widget.addWidget(eod_screen)
# Just a normal clock
plainclock = PlainClock()
widget.addWidget(plainclock)
# shows some info about the schedules
infoscreen = InfoScreen()
widget.addWidget(infoscreen)
# Window Settings
widget.setFixedHeight(1000)
widget.setFixedWidth(1920)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")