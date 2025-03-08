from tkinter import * #Import toan bo thu vien tkinter
from StillClock import StillClock #Import class StillClock 

class DisplayClock:
    def __init__(self):
        window = Tk() #Tao cua so
        window.title("Change Clock Time") #Dat tieu de cho cua so

        self.clock = StillClock(window) #Tao dong ho
        self.clock.pack() #Hien thi dong ho

        frame = Frame(window) #Tao mot frame
        frame.pack() #Hien thi frame

        #Nhap gio
        Label(frame, text = "Enter hours: ").pack(side = LEFT)
        self.hour = IntVar()
        self.hour.set(self.clock.getHour())
        Entry(frame, textvariable = self.hour, width = 2).pack(side = LEFT)

        #Nhap phut
        Label(frame, text = "Enter minutes: ").pack(side = LEFT)
        self.minute = IntVar()
        self.minute.set(self.clock.getMinute())
        Entry(frame, textvariable = self.minute, width = 2).pack(side = LEFT)

        #Nhap giay
        Label(frame, text = "Enter seconds: ").pack(side = LEFT)
        self.second = IntVar()
        self.second.set(self.clock.getSecond())
        Entry(frame, textvariable = self.second, width = 2).pack(side = LEFT)

        #nut cap nhat thoi gian
        Button(frame, text = "Set New Time", command = self.setNewTime).pack(side = LEFT)

        window.mainloop() #Tao vong lap chay chuong trinh

    def setNewTime(self):
        self.clock.setHour(self.hour.get())
        self.clock.setMinute(self.minute.get())
        self.clock.setSecond(self.second.get())

DisplayClock() #Chay ung dung        
