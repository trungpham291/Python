from tkinter import Canvas
import time
import math

class StillClock(Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=200, bg="white")
        self.hour = time.localtime().tm_hour
        self.minute = time.localtime().tm_min
        self.second = time.localtime().tm_sec
        self.drawclock()

    def drawclock(self):
        self.delete("all") # Xóa noi dung cu
        self.create_oval(10, 10, 190, 190, width=2) # ve mat dong ho 

        #ve kim gio
        hour_angle = math.radians(30 * (self.hour % 12) - 90)
        self.create_line(100, 100, 100 + 50 * math.cos(hour_angle), 100 + 50 * math.sin(hour_angle), width=3, fill="black")

        #ve kim phut
        minute_angle = math.radians(6 * self.minute - 90)
        self.create_line(100, 100, 100 + 70 * math.cos(minute_angle), 100 + 70 * math.sin(minute_angle), width=2, fill="blue")

        #ve kim giay
        second_angle = math.radians(6 * self.second - 90)
        self.create_line(100, 100, 100 + 80 * math.cos(second_angle), 100 + 80 * math.sin(second_angle), width=1, fill="red")

    def getHour(self):
        return self.hour 
    def getMinute(self):
        return self.minute
    def getSecond(self):
        return self.second
    def setHour(self, hour):
        self.hour = hour
        self.drawclock()
    def setMinute(self, minute):
        self.minute = minute
        self.drawclock()
    def setSecond(self, second):
        self.second = second
        self.drawclock()       

  
        
