# SECV3213-02 FUNDAMENTAL OF IMAGE PROCESSING #
#                 ASSIGNMENT 3                #
# ------------------GROUP 9------------------ #
# 1. Gan Qi You    A21EC0178                  #
# 2. Lai Kai Chian A21EC0041                  #
# 3. Wai Jia Wen   A21EC0139                  #

import cv2 as cv
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog as sd
from tkinter import (Tk, ttk, Label, Frame, Button, Radiobutton, IntVar, HORIZONTAL)
import matplotlib.pyplot as plt

# Default values
BORDER_SIZE = 15
CAPTION_SIZE = 60

class ImageThresholding(Tk):

    def __init__(self):
        super().__init__()
        self.manipulationMenu()

    #----- GUI -----
    def manipulationMenu(self):
        # set title of window
        self.title('Image Segmentation Application')
        # set the size of window
        self.geometry("500x400+50+50")
        self.setupMenu()
    
    def setupMenu(self):
        # set up the widgets
        # title
        title = Label(self, text="Image Segmentation Application", font=('Helvetica', 20), bd=10)
        title.pack()

        line = ttk.Separator(self, orient=HORIZONTAL)
        line.pack(fill='x')

        ## choose manipulation type
        manipulation_label = Label(self, text="How do you want to segment the image?", font=('Helvetica', 14), bd=10)
        manipulation_label.pack(anchor='w')

        manip = Frame(self) # frame to store the radio buttons in a line
        manip.pack(anchor='w', padx=10)

        self.var = IntVar()
        self.var.set(0)
        self.manipulation_methods = ["Global Threshold", "Otsu Threshold", "Adaptive Threshold"]

        for  i, method in  enumerate(self.manipulation_methods):
            self.manip_method = Radiobutton(manip, text=method, variable=self.var, value=i, font=('Helvetica', 11), bd=4, bg='white', fg='black', activebackground='skyblue')
            self.manip_method.pack(side='left')
        empty_line = Label(self, text=""); empty_line.pack() # an empty line

        next_button = Button(self, text="Next", font=('Helvetica', 11), width=10, command=self.getManipulation, fg='white', background='blue', activebackground='skyblue') # button to pass the selected manipulation and percentage
        next_button.pack(anchor='w', padx=10)
        empty_line = Label(self, text=""); empty_line.pack() # an empty line
        empty_line = Label(self, text=""); empty_line.pack() # an empty line

        ## footer buttons to save the manipulated image or reset operations
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

    # get the manipulation type
    def getManipulation(self):
        plt.close()
        self.openImageFile()
        if(self.var.get()==0):
            self.askGlobalThreshold()
        elif(self.var.get()==1):
            self.otsuThreshold()
        else:
            self.askBlockSize()

    # open image file
    def openImageFile(self):
        self.filename = filedialog.askopenfilename(initialdir='./images', title='Select an image for manipulation')
        self.raw_img = cv.imread(self.filename)
        self.img = self.raw_img.copy()
        cv.destroyAllWindows()
        plt.close()
        cv.imshow('Image', self.img)

    def askGlobalThreshold(self):
        global globalthresholdvalue
        globalthresholdvalue = sd.askinteger("Change threshold", "Enter the global threshold value (0-255) [default: 127]", minvalue=0, maxvalue=255)
        if globalthresholdvalue == None:
            globalthresholdvalue = 127
        self.globalThreshold()
    
    def askBlockSize(self):
        global blockSize, parameter1
        blockSize = sd.askinteger("Change Block Size", "Enter the block size (odd number) [default: 45]", minvalue=3)
        if blockSize == None:
            blockSize = 45; parameter1 = 10
        while(blockSize%2==0):
            blockSize = sd.askinteger("Change Block Size", "Enter the block size (odd number) [default: 45]", minvalue=3)
        parameter1 = sd.askinteger("Change Parameter", "Enter the parameter (min 0) [default: 10]", minvalue=0)
        self.adaptive()

    # global threshold
    def globalThreshold(self):
        cv.destroyAllWindows()
        plt.close()
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        ret, thres = cv.threshold(gray, globalthresholdvalue, 255, cv.THRESH_BINARY) 
        color_thresh = cv.cvtColor(thres, cv.COLOR_GRAY2BGR) # Convert the thresholded image to colored
        self.img = cv.bitwise_or(color_thresh, self.img) # Perform OR operation to get back the color of original image
        self.display(self.raw_img, self.img) # display the input & output

    # otsu threshold
    def otsuThreshold(self):
        cv.destroyAllWindows() 
        plt.close()
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        ret, thres = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU) 
        color_thresh = cv.cvtColor(thres, cv.COLOR_GRAY2BGR) # Convert the thresholded image to colored
        self.img = cv.bitwise_or(color_thresh, self.img) # Perform OR operation to get back the color of original image
        self.display(self.raw_img, self.img)

    # adaptive threshold
    def adaptive(self):
        cv.destroyAllWindows()
        plt.close()
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        thres = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize, parameter1)
        color_thresh = cv.cvtColor(thres, cv.COLOR_GRAY2BGR) # Convert the thresholded image to colored
        self.img = cv.bitwise_or(color_thresh, self.img) # Perform OR operation to get back the color of original image
        self.display(self.raw_img, self.img)

    # display image
    def display(self, image1, image2):
        global w, h
        w = sd.askinteger("Change Display Output Window Width", "Enter the width (2-15) [default: 8]", minvalue=2, maxvalue=15)
        h = sd.askinteger("Change Display Output Window Height", "Enter the height (1-8) [default: 4]", minvalue=1, maxvalue=8)
        if w == None:
            w = 8
        if h == None:
            h = 4
        fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(w, h), tight_layout=True)
        axs[0].imshow(image1[:,:,::-1])
        axs[0].set_title("Input")
        axs[0].axis("off")

        axs[1].imshow(image2[:,:,::-1])
        axs[1].set_title("Output")
        axs[1].axis("off")

        plt.show()
    
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
        plt.close()

if  __name__  ==  "__main__":
    app = ImageThresholding()
    app.mainloop()