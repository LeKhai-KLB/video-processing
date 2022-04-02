# import tkinter as tk
from tkinter import Tk, Frame, Label, LEFT, TOP, CENTER, Button, PhotoImage, ttk, NW, Canvas, RAISED
from tkinter import filedialog, Toplevel, X
import PIL.Image, PIL.ImageTk

import cv2, pandas
import numpy as np

class videoGUI:

    def __init__(self, window, window_title):

        self.window = window
        self.window.geometry('1000x800+300+0')
        self.window.resizable(width = 1, height = 1)
        self.window.config(bg = "#212121")
        self.window.title(window_title)
        self.Time = 0
        self.time = 0
        self.sec = 0
        self.min = 0
        self.string = str(self.min) + ':' + str(self.sec)
        self.backSub = cv2.createBackgroundSubtractorKNN()
        self.static_back = None
  
        self.df = pandas.DataFrame(columns = ["Start", "End"]) 
        top_frame = Frame(self.window, width = 1000, height = 30)
        bottom_frame = Frame(self.window, width = 1000, height = 770, bg = "#212121")
        left_frame = Frame(bottom_frame, bg = "#383838", width = 280, height = 770)
        right_frame = Frame(bottom_frame, bg = "#383838", width = 680, height = 770)
        
        # Left Frame:
        labelFunction = Label(left_frame, text = "Chế độ", bg = "#383838", fg = 'white')
        self.infoFrame = Frame(left_frame, width = 200, height = 300, bg = "#60686F")
        labelInfomation= Label(left_frame, text = "Thông tin video", bg = "#383838", fg = 'white')
        comboFrame = Frame(left_frame, width = 200, height = 200, bg = "#60686F")
        blankFrame = Frame(left_frame, width = 200, height = 30, bg = "#383838")
        
        # Combo Frame:
        self.camera = False
        self.chooseBox = ttk.Combobox(comboFrame, width = 15)
        self.chooseBox['values'] = ('Camera', 'Video') 
        buttonSelect = Button(comboFrame, bg = "#DEE1E6", text = "select", command = self.select_mode)
        
        # Right Frame:
        vidFrame = Frame(right_frame, bg = "#0D0D0D", height = 400, width = 640)
        controlFrame = Frame(right_frame, bg = '#60686F', height = 30, width = 640)
        rightFrame_bot = Frame(right_frame, bg = '#60686F', relief = RAISED, borderwidth = 1, height = 80, width = 400)
        self.messageFrame = Frame(rightFrame_bot, bg = '#19232D', borderwidth = 1, height = 55, width = 350)
        
        # Message frame:
        self.label0 = Label(self.messageFrame, text = "CHỌN 1 CHẾ ĐỘ XEM VIDEO !!!", bg = '#19232D', fg = 'white')
        self.label1 = Label(self.messageFrame, text = "ĐANG XỬ LÝ VIDEO", bg = '#19232D', fg = 'white')
        self.label2 = Label(self.messageFrame, text = "THỜI GIAN:", bg = '#19232D', fg = 'white')
        self.label3 = Label(self.messageFrame, text = self.string, bg = '#19232D', fg = 'white')
        self.label0.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            
        # Control Frame:
        playIcon = PhotoImage(file = "co2.png")
        self.btn_play = Button(controlFrame, image = playIcon, command=self.play_video)
        sIcon = PhotoImage(file = "s1.png")
        self.btn_control = Button(controlFrame, image = sIcon, command=self.controlbox)
        
        # Top Frame:
        self.btn_select = Button(top_frame, text = "Open file", bg = "#DEE1E6", command = self.open_file)
        self.btn_about = Button(top_frame, text = "About", bg = "#DEE1E6", command = self.aboutBox)

        self.pause = False   # Parameter that controls pause button
        self.canvas1 = Canvas(vidFrame, bg = "#0D0D0D")
        self.canvas2 = Canvas(vidFrame, bg = "#0D0D0D")
        self.canvas3 = Canvas(vidFrame, bg = "#0D0D0D")
        self.canvas4 = Canvas(vidFrame, bg = "#0D0D0D")
        self.canvas1.config(width = 320, height = 310)
        self.canvas2.config(width = 320, height = 310)
        self.canvas3.config(width = 320, height = 310)
        self.canvas4.config(width = 320, height = 310)
        self.canvas1.grid(row = 0, column = 0)
        self.canvas2.grid(row = 0, column = 1)
        self.canvas3.grid(row = 1, column = 0)
        self.canvas4.grid(row = 1, column = 1)
        
         # Display:
        top_frame.pack(side = TOP)
        self.btn_select.place(anchor = NW, relwidth = 0.2)
        self.btn_about.place(anchor = NW, relx = 0.2, relwidth = 0.2)
        bottom_frame.pack(side = TOP)
        left_frame.pack(side = LEFT, padx = 10)
        right_frame.pack(side = LEFT, padx = 10)
        labelInfomation.pack(side = TOP, pady = 10)
        self.infoFrame.pack(side = TOP, padx = 30)
        labelFunction.pack(side = TOP, pady = 10)
        comboFrame.pack(side = TOP, padx = 30)
        blankFrame.pack(side = TOP)
        vidFrame.place(relx = 0.5, rely = 0.4, anchor = CENTER)
        controlFrame.place(relx = 0.5, rely = 0.8, anchor = CENTER)
        self.btn_play.pack(side = LEFT, padx = 5, pady = 5)
        self.btn_control.pack(side = LEFT, padx = 5, pady = 5)
        # self.btn_pause.pack(side = LEFT, pady = 10, padx = 5)
        # self.btn_resume.pack(side = LEFT, pady = 10, padx = 5)
        self.chooseBox.place(relx = 0.5, rely = 0.2, anchor = CENTER)
        rightFrame_bot.place(relx = 0.5, rely = 0.9, anchor = CENTER)
        self.messageFrame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        buttonSelect.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        self.delay = 15   # ms

        self.window.mainloop()
    
    def fclear(self):
        list = self.infoFrame.place_slaves()
        for l in list:
            l.place_forget()
            
    def open_file(self):
        self.pause = False
        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),
                                                                                         ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        # Open the video file
        self.camera = False
        self.fclear()
        self.cap = cv2.VideoCapture(self.filename)
        frame_number = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        sec2 = frame_number / self.fps
        self.sec2 = int(sec2)
        self.info()

    def select_mode(self):
        if self.chooseBox.get() == 'Camera':
            self.fclear()
            self.pause = False
            self.camera = True
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.info()
        elif self.chooseBox.get() == 'Video':
            self.open_file()
        self.label0.place_forget()
        self.time = 0
        self.sec = 0
        self.min = 0
        self.static_back = None
        # List when any moving object appear 
        self.motion = 0 
        self.string = str(self.min) + ':' + str(self.sec)
        self.label3.place_forget()
        self.label3.configure(text = self.string)
        self.label1.place(relx = 0.5, rely = 0.2, anchor = CENTER)
        self.label2.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        self.label3.place(relx = 0.5, rely = 0.8, anchor = CENTER)
        
    def info(self):
        panel1 = Label(self.infoFrame, text = 'ĐƯỜNG DẪN FILE:', bg = '#60686F', fg = 'black')
        if self.camera == True:
            panel11 = Label(self.infoFrame, text = 'None', bg = '#60686F', fg = 'white')
        else:
            txt = str(self.filename)
            panel11 = Label(self.infoFrame, text = txt, bg = '#60686F', fg = 'white')
        
        panel2 = Label(self.infoFrame, text = 'THỜI LƯỢNG (số giây):', bg = '#60686F', fg = 'black')
        if self.camera == True:
            panel21 = Label(self.infoFrame, text = 'None', bg = '#60686F', fg = 'white')
        else:
            panel21 = Label(self.infoFrame, text = str(self.sec2), bg = '#60686F', fg = 'white')
        
        panel3 = Label(self.infoFrame, text = 'FPS:', bg = '#60686F', fg = 'black')
        if self.camera == False:
            panel31 = Label(self.infoFrame, text = str(self.fps), bg = '#60686F', fg = 'white')
        else:
            panel31 = Label(self.infoFrame, text = 'None', bg = '#60686F', fg = 'white')
        
        panel1.place(relx = 0.5, rely = 0.2, anchor = CENTER)
        panel11.place(relx = 0.5, rely = 0.3, anchor = CENTER)
        panel2.place(relx = 0.5, rely = 0.4, anchor = CENTER)
        panel21.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        panel3.place(relx = 0.5, rely = 0.6, anchor = CENTER)
        panel31.place(relx = 0.5, rely = 0.7, anchor = CENTER)
        panell = Label(self.infoFrame, text = '--------o0o--------', bg = '#60686F', fg = 'black')
        panell.place(relx = 0.5, rely = 0.82, anchor = CENTER)
    def get_frame(self):   # get only one frame
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            self.pause = False
            self.camera = False
            
    def show_time(self):
        if self.time == 15:
            self.time = 0
            self.sec += 1
            if self.sec == 59:
                self.sec = 0
                self.min += 1
            self.string = str(self.min) + ':' + str(self.sec)
            self.label3.place_forget()
            self.label3.configure(text = self.string)
            self.label3.place(relx = 0.5, rely = 0.8, anchor = CENTER)
            
        
    def play_video(self):

        # Get a frame from the video source, and go to the next frame automatically
        self.time += 1
        self.show_time()
        ret, frame = self.get_frame()
        dsize = (320, 310)
        frame = cv2.resize(frame, (dsize))
        color_frame = np.copy(frame)
        fgMask = self.backSub.apply(frame)
        self.motion = 0
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
  
        # Converting gray scale image to GaussianBlur  
        # so that change can be find easily 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 
  
        # In first iteration we assign the value  
        # of static_back to our first frame 
        if self.static_back is None: 
            self.static_back = gray 
  
        # Difference between static background  
        # and current frame(which is GaussianBlur) 
        diff_frame = cv2.absdiff(self.static_back, gray) 
  
        # If change in between static background and 
        # current frame is greater than 30 it will show white color(255) 
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
        cnts,_ = cv2.findContours(thresh_frame.copy(),  
                       cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
  
        for contour in cnts: 
            if cv2.contourArea(contour) < 10000: 
                continue
  
            (x, y, w, h) = cv2.boundingRect(contour) 
            # making green rectangle arround the moving object 
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (0, 255, 0), 3) 
  
        if self.camera == True:
            frame = cv2.flip(frame, 1)
            fgMask = cv2.flip(fgMask,1)
            diff_frame = cv2.flip(diff_frame, 1)
            color_frame = cv2.flip(color_frame, 1)
        if ret:
            self.test = PIL.Image.fromarray(frame)
            self.test1 = PIL.Image.fromarray(color_frame)
            self.test2 = PIL.Image.fromarray(fgMask)
            self.test3 = PIL.Image.fromarray(diff_frame)
            self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas1.create_image(0, 0, image = self.photo1, anchor = NW)
            self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(color_frame))
            self.canvas2.create_image(0, 0, image = self.photo2, anchor = NW)
            self.photo3 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(fgMask))
            self.canvas3.create_image(0, 0, image = self.photo3, anchor = NW)
            self.photo4 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(diff_frame))
            self.canvas4.create_image(0, 0, image = self.photo4, anchor = NW)
            self.zoomcycle = 0
            self.zimg_id = None
            self.zimg_id1 = None
            self.zimg_id2 = None
            self.zimg_id3 = None
            
            self.window.bind("<MouseWheel>",self.zoomer)
            self.canvas1.bind("<Motion>",self.crop)
            self.canvas2.bind("<Motion>",self.crop)
            self.canvas3.bind("<Motion>",self.crop)
            self.canvas4.bind("<Motion>",self.crop)
        if not self.pause:
            self.window.after(self.delay, self.play_video)


    def pause_video(self):
        self.pause = True

#Addition
    def resume_video(self):
        self.pause=False
        self.play_video()
        
    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.zimg_id: self.canvas1.delete(self.zimg_id)
        if self.zimg_id1: self.canvas2.delete(self.zimg_id1)
        if self.zimg_id2: self.canvas3.delete(self.zimg_id2)
        if self.zimg_id3: self.canvas4.delete(self.zimg_id3)
        if (self.zoomcycle) != 0:
            x,y = event.x, event.y
            if self.zoomcycle == 1:
                tmp = self.test.crop((x-45,y-30,x+45,y+30))
                tmp1 = self.test1.crop((x-45,y-30,x+45,y+30))
                tmp2 = self.test2.crop((x-45,y-30,x+45,y+30))
                tmp3 = self.test3.crop((x-45,y-30,x+45,y+30))
            elif self.zoomcycle == 2:
                tmp = self.test.crop((x-30,y-20,x+30,y+20))
                tmp1 = self.test1.crop((x-30,y-20,x+30,y+20))
                tmp2 = self.test2.crop((x-30,y-20,x+30,y+20))
                tmp3 = self.test3.crop((x-30,y-20,x+30,y+20))
            elif self.zoomcycle == 3:
                tmp = self.test.crop((x-15,y-10,x+15,y+10))
                tmp1 = self.test1.crop((x-15,y-10,x+15,y+10))
                tmp2 = self.test2.crop((x-15,y-10,x+15,y+10))
                tmp3 = self.test3.crop((x-15,y-10,x+15,y+10))
            elif self.zoomcycle == 4:
                tmp = self.test.crop((x-6,y-4,x+6,y+4))
                tmp1 = self.test1.crop((x-6,y-4,x+6,y+4))
                tmp2 = self.test2.crop((x-6,y-4,x+6,y+4))
                tmp3 = self.test3.crop((x-6,y-4,x+6,y+4))
            size = 150,150 #kích thước khung phóng to
            self.zimg = PIL.ImageTk.PhotoImage(tmp.resize(size))
            self.zimg_id = self.canvas1.create_image(event.x,event.y,image=self.zimg)
            self.zimg1 = PIL.ImageTk.PhotoImage(tmp1.resize(size))
            self.zimg_id1 = self.canvas2.create_image(event.x,event.y,image=self.zimg1)
            self.zimg2 = PIL.ImageTk.PhotoImage(tmp2.resize(size))
            self.zimg_id2 = self.canvas3.create_image(event.x,event.y,image=self.zimg2)
            self.zimg3 = PIL.ImageTk.PhotoImage(tmp3.resize(size))
            self.zimg_id3 = self.canvas4.create_image(event.x,event.y,image=self.zimg3)

        
    def controlbox(self):
        self.box = Toplevel(self.window)
        self.box.title("Control box")
        self.box.geometry('100x80')
        box_top = Frame(self.box, bg = '#60686F')
        pauseIcon = PhotoImage(file = "pause1.png")
        self.btn_pause = Button(box_top, image = pauseIcon, command=self.pause_video)
        self.btn_pause.image = pauseIcon
        resumeIcon = PhotoImage(file = "media-end.png")
        self.btn_resume = Button(box_top, image = resumeIcon, command=self.resume_video)
        self.btn_resume.image = resumeIcon
        
        box_top.place(relx = 0.5, rely = 0.5, anchor = CENTER)
        self.btn_pause.pack(side = LEFT, padx = 5, pady = 5)
        self.btn_resume.pack(side = LEFT, padx = 5, pady = 5)
    
    def aboutBox(self):
        self.box_left = Toplevel(self.window)
        self.box_left.title("About")
        Label(self.box_left,fg="red", text="HỌC PHẦN NHẬP MÔN XỬ LÝ ẢNH",height="1",font=("arial", 17),padx=200).pack()
        Label(self.box_left, text="    ĐỒ ÁN MÔN HỌC",height="1",fg="Blue",font=("arial", 18,"bold"),pady=20).pack()
        Label(self.box_left, text="ĐỀ TÀI: TÌM HIỂU THƯ VIỆN OPENCV, NGÔN NGỮ LẬP TRÌNH PYTHON, MỘT SỐ ĐỊNH DẠNG VIDEO",height="1",fg="Red",font=("arial", 14),pady=5).pack()
        Label(self.box_left, text="VIẾT ỨNG DỤNG PHÁT HIỆN CHUYỂN ĐỘNG",height="1",fg="Red",font=("arial", 14),pady=20).pack()
        Label(self.box_left, text="  Nhóm Thực Hiện:",height="1",fg="Blue",font=("arial", 14),pady=10).pack()
        Label(self.box_left, text="  Nhóm 4",height="1",fg="Blue",font=("arial", 14),pady=5).pack()
        Label(self.box_left,anchor="w", text=" Giáo viên hướng dẫn:",height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=' ThS    Ngô thị Hồng Thắm',padx=50,height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=" Thành viên thực hiện:",height="1",font=("arial", 14),pady=10).pack(fill=X)
        Label(self.box_left,anchor="w", text=' Lê Quang Khải       18DDS0803112',padx=50,height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=' Nguyễn Thành Khiêm       18DDS0803116',padx=50,height="1",font=("arial", 14)).pack(fill=X)
        Label(self.box_left,anchor="w", text=' Lại huy Tuấn Anh    18DDS0803103',padx=50,height="1",font=("arial", 14)).pack(fill=X)
    
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

##### End Class #####


# Create a window and pass it to videoGUI Class
videoGUI(Tk(), "Xử lý video")