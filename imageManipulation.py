# SECV3213-02 FUNDAMENTAL OF IMAGE PROCESSING #
#                 ASSIGNMENT 1                #
# ------------------GROUP 9------------------ #
# 1. Gan Qi You    A21EC0178                  #
# 2. Lai Kai Chian A21EC0041                  #
# 3. Wai Jia Wen   A21EC0139                  #

import cv2 as cv
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import (Tk, ttk, Label, Frame, Button, Radiobutton, IntVar, HORIZONTAL)

class ImageManipulation(Tk):

    def __init__(self):
        super().__init__()
        self.manipulationMenu()

    #----- GUI -----
    def manipulationMenu(self):
        # set title of window
        self.title('Image Manipulation Application')
        # read png image file
        icon = PhotoImage(file = './icon/edit_image_icon.png')
        # set the title bar icon
        self.iconphoto(False, icon)
        # set the size of window
        self.geometry("600x500+50+50")
        self.setupMenu()
    
    def setupMenu(self):
        # set up the widgets
        # title
        title = Label(self, text="Image Manipulation Application", font=('Helvetica', 20), bd=10)
        title.pack()

        line = ttk.Separator(self, orient=HORIZONTAL)
        line.pack(fill='x')

        ## open image
        manipulation_label = Label(self, text="Choose an image", font=('Helvetica', 14), bd=10)
        manipulation_label.pack(anchor='w')
        img_button = Button(self, text="Open Image", font=('Helvetica', 11), width=10, command=self.openImageFile, fg='white', background='blue', activebackground='skyblue')
        img_button.pack(anchor='w', padx=10)
        empty_line = Label(self, text=""); empty_line.pack() # an empty line

        ## choose manipulation type
        manipulation_label = Label(self, text="How do you want to manipulate the image?", font=('Helvetica', 14), bd=10)
        manipulation_label.pack(anchor='w')

        manip = Frame(self) # frame to store the radio buttons in a line
        manip.pack(anchor='w', padx=10)

        self.var = IntVar()
        self.var.set(0)
        self.manipulation_methods = ["Blacken", "Brighten", "Darken"]

        for  i, method in  enumerate(self.manipulation_methods):
            self.manip_method = Radiobutton(manip, text=method, variable=self.var, value=i, font=('Helvetica', 11), bd=4, bg='white', fg='black', activebackground='skyblue')
            self.manip_method.pack(side='left')
        
        darken_brighten_level_label = Label(manip, text="Darken/Brighten(%):", font=('Helvetica', 11), bd=10)
        darken_brighten_level_label.pack(side='left')
        self.darken_brighten_percentage = Scale(manip, from_=0, to=100, orient=HORIZONTAL, length=150, activebackground='blue')
        self.darken_brighten_percentage.set(50)
        self.darken_brighten_percentage.pack()

        next_button = Button(self, text="Next", font=('Helvetica', 11), width=10, command=self.getManipulation, fg='white', background='blue', activebackground='skyblue') # button to pass the selected manipulation and percentage
        next_button.pack(anchor='w', padx=10)
        empty_line = Label(self, text=""); empty_line.pack() # an empty line

        ## instruction of ROI
        roi_label = Label(self, text="Select a Region Of Interest (ROI)", font=('Helvetica', 14), bd=10)
        roi_label.pack(anchor='w')
        roi_label = Label(self, text="- use mouse to select ROI", font=('Helvetica', 11), padx=10)
        roi_label.pack(anchor='w')
        roi_label = Label(self, text="- click ENTER/space to confirm, C to cancel selected ROI", font=('Helvetica', 11), padx=10)
        roi_label.pack(anchor='w')
        roi_label = Label(self, text="- after selecting multiple ROIs, click Esc to perform manipulation", font=('Helvetica', 11), padx=10)
        roi_label.pack(anchor='w')
        empty_line = Label(self, text=""); empty_line.pack() # an empty line

        ## footer buttons to save the manipulated image or reset manipulation on image
        footer = Frame(self) # frame to store the radio buttons in a line
        footer.pack(anchor='center', padx=10)
        next_button = Button(footer, text="Save", font=('Helvetica', 11), width=10, command=self.save, fg='white', background='red', activebackground='skyblue') # button to pass the selected manipulation and percentage
        next_button.pack(side='left')
        next_button = Button(footer, text="Reset", font=('Helvetica', 11), width=10, command=self.reset, fg='white', background='green', activebackground='skyblue') # button to pass the selected manipulation and percentage
        next_button.pack(side='left', padx=10)

    #----- FUNCTIONS -----
    # variables definitions
    # raw_img      : uploaded original image
    # img          : a copy of original image to be used in manipulations
    # temp_img     : the temporary image after manipulations

    # get the manipulation type
    def getManipulation(self):
        if(self.var.get()==0):
            self.blacken()
        elif(self.var.get()==1):
            self.brighten()
        else:
            self.darken()

    # open image file
    def openImageFile(self):
        self.filename = filedialog.askopenfilename(initialdir='./images', title='Select an image for manipulation')
        self.raw_img = cv.imread(self.filename)
        self.img = self.raw_img.copy()
        cv.destroyAllWindows()
        cv.imshow('Image', self.img)

    # blacken image
    def blacken(self):
        cv.destroyAllWindows()
        (x,y,z) = self.img.shape # get the dimension of image
        self.rectangle = 255*np.ones((x,y,z), dtype="uint8") # create white blank image of the same size
        self.rois = cv.selectROIs("Select ROIs", self.img) # select multiple ROIs
        for roi in self.rois:
            # make the roi region becomes black
            self.rectangle[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] = 0
            # perform bitwise AND on the image
            self.temp_img = cv.bitwise_and(self.rectangle, self.img)
        self.img = self.temp_img
        cv.destroyAllWindows()
        cv.imshow('Image', self.img)

    # darken image (division)
    def darken(self):
        cv.destroyAllWindows()
        (x,y,z) = self.img.shape # get the dimension of image
        self.rois = cv.selectROIs("Select ROIs", self.img) # select multiple ROIs
        # calculate the darkness scale
        # to make image darker the scale should be <1, use 100 to subtract the percentage because greater percentage of darkness is resulted from smaller decimal value of scale
        darkness = (100-self.darken_brighten_percentage.get())/100
        # perform division on the selected ROIs based on chosen scale
        for roi in self.rois:
            self.img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] = cv.divide(self.img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])], (1,1,1,1), scale=darkness)
        cv.destroyAllWindows()
        cv.imshow('Image', self.img)

    # lighten image (multiplication)
    def brighten(self):
        cv.destroyAllWindows()
        (x,y,z) = self.img.shape # get the dimension of image
        self.rois = cv.selectROIs("Select ROIs", self.img) # select multiple ROIs
        # calculate the brightness scale
        # add 1 because cannot scale cannot smaller than 1, <1 will make image darker (like division)
        brightness = (self.darken_brighten_percentage.get()/100)+1.0
        # perform multiplication on the selected ROIs based on chosen scale
        for roi in self.rois:
            self.img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] = cv.multiply(self.img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])], (1,1,1,1), scale=brightness)
        cv.destroyAllWindows()
        cv.imshow('Image', self.img)

    # save image
    def save(self):
        file_type = self.filename.split('.')[-1]
        filename = filedialog.asksaveasfilename()
        filename = filename + "." + file_type

        cv.imwrite(filename, self.img)
        cv.destroyAllWindows()
    
    # reset image
    def reset(self):
        self.img = self.raw_img.copy()
        cv.destroyAllWindows()
        cv.imshow('Image', self.img)

if  __name__  ==  "__main__":
    app = ImageManipulation()
    app.mainloop()