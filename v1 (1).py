import cv2
import numpy as np
import os
import pandas as pd
import DetectChars
import DetectPlates
import PossiblePlate
import PIL.Image
from PIL import ImageTk
import tkinter
from tkinter import filedialog
import subprocess as sub
#import sys

filename = 'uninitialized'

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)
showSteps = False
#******************************************************************************

root = tkinter.Tk()
root.title("License Plate Recognition")
root.geometry('1000x700')
c=tkinter.Canvas(root,bg="blue",height=250,width=300)
filename1=tkinter.PhotoImage(file = "E:/Webp.net-resizeimage.gif")
background_label=tkinter.Label(root,image=filename1)
background_label.place(x=0,y=0,relwidth=1,relheight=1)

def open_file_dialog():
    global filename
    filename = filedialog.askopenfilename(filetypes=[("allfiles","*")])
    #create_window0(filename)
def open_file_dialog1():
    global filename3
    filename3 = filedialog.askopenfilename(filetypes=[("text files","*.txt")])

def showimg(filename):
    load = PIL.Image.open(filename)
    render = ImageTk.PhotoImage(load)
    img = tkinter.Label(window0,image=render)
    img.image = render
    img.place(x=1,y=1)

def create_window0(filename):
    window0 = tkinter.Toplevel(root)
    window0.geometry('1000x700')
    window0.title("License Plate Struck!")

    load = PIL.Image.open(filename)
    render = ImageTk.PhotoImage(load)
    img = tkinter.Label(window0, image=render)
    img.image = render
    img.place(x=1, y=1)

def create_window():
    window = tkinter.Toplevel(root)
    window.geometry('1000x700')
    window.configure(background= 'indianred4')
    w = tkinter.Label(window, text="Details are also displayed in the file (E:\output.txt)",font=("Courier New Bold",11))
    w.config(justify="center", foreground='black', background='pink1')
    w.place(relx=.5,rely=.05,anchor='c')
    btn2 = tkinter.Button(window, text='Get the owner details!',font=("Courier New Bold",10), command=lambda: mainfnc(filename), bg = "tomato1", fg = "black")
    btn2.place(relx=.5,rely=.1,anchor='c')
    w1 = tkinter.Label(window, text="Detected License Plate:",font=("Courier New Bold",11))
    w1.config(justify="center", foreground='black', background='pink1')
    w1.place(relx=.2, rely=.3, anchor='c')
    w2 = tkinter.Label(window, text="Details:",font=("Courier New Bold",11))
    w2.config(justify="center", foreground='black', background='pink1')
    w2.place(relx=.2, rely=.5, anchor='c')
    def mainfnc(variable):

        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training
        # global text1
        if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
            print("\nerror: KNN traning was not successful\n")  # show error message
            return  # and exit program
        # end if

        imgOriginalScene = cv2.imread(variable)
        imS = cv2.resize(imgOriginalScene, (960, 540))  # open image

        if imgOriginalScene is None:  # if image was not read successfully
            print("\nerror: image not read from file \n\n")  # print error message to std out
            os.system("pause")  # pause so user can see error message
            return  # and exit program
        # end if

        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

        #winname = "Test"
        #cv2.namedWindow(winname)  # Create a named window
        #cv2.moveWindow(winname, 20, 20)
        # cv2.imshow(winname, imgOriginalScene)            # show scene image

        if len(listOfPossiblePlates) == 0:  # if no plates were found
            print("\nno license plates were detected\n")  # inform user no plates were found
        else:  # else
            # if we get in here list of possible plates has at leat one plate

            # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            cv2.imshow("imgPlate", licPlate.imgPlate)     # show crop of plate and threshold of plate
            x = licPlate.imgThresh
            cv2.imshow("imgThresh", x)

            if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                print("\nno characters were detected\n\n")  # show message
                return  # and exit program
            # end if

            drawRedRectangleAroundPlate(imgOriginalScene, licPlate)  # draw red rectangle around plate
            text1 = licPlate.strChars
            print("\nlicense plate read from image = " + text1 + "\n")  # write license plate text to std out
            Results = tkinter.Text(window, height=2, width=10)
            Results.config( foreground='black', background='plum1',font=("Courier New Bold",16), bd=5)
            Results.place(relx=.6, rely=.3, anchor='c')
            Results.insert(1.0, text1)
            df = pd.read_csv("data4.csv")
            a = df[df['Plate No.'] == text1]
            print(a)
            Results1 = tkinter.Text(window, height=3, width=50)
            Results1.config(foreground='black', background='plum1',font=("Courier New Bold",12),bd=5)
            Results1.place(relx=.6, rely=.5, anchor='c')
            Results1.insert(1.0, a)
            # writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           # write license plate text on the image

            cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image

            # cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file

        # end if else

        cv2.waitKey(0)  # hold windows open until user presses a key

        return

    # end main
    ###################################################################################################
    def print_output(licPlate):
        global a
        df = pd.read_csv("data.csv")
        a = df[df['Plate No.'] == text1]
        print(a)
        return

    ###################################################################################################
    ###################################################################################################
    def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

        p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)  # get 4 vertices of rotated rect

        cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)  # draw 4 red lines
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)

        return

    # end function

    ###################################################################################################


    '''def show_output():
        file = open("output.txt")
        data = file.read()
        file.close()
        Results = tkinter.Text(window, height=2, width=30)
        Results.place(relx=.6, rely=.6, anchor='c')
        Results.insert(END, "data")'''

    #btn6 = tkinter.Button(window, text='Open the output file', font=("Courier New Bold", 10),command=lambda: show_output(), bg="salmon1", fg="black")
    #btn6.place(relx=.3, rely=.2, anchor='c') '''

lbl=tkinter.Label(root, text="RECOGNITION OF NUMBER PLATES",font=("Courier New Bold",24),relief='solid')
lbl.config(justify="center", foreground='black', background='gold2')
lbl.place(relx=.5,rely=.05,anchor='c')
#lbl.grid(column=2, row=0)

btn1=tkinter.Button(root, text='Select Image file',font=("Courier New Bold",10),command=open_file_dialog, bg = "salmon1", fg="black")
btn1.place(relx=.3,rely=.2,anchor='c')

btn4 = tkinter.Button(root, text="Display Image",font=("Courier New Bold",10), command=lambda: create_window0(filename), bg = "salmon1", fg = "black")
btn4.place(relx=.5,rely=.2,anchor='c')
#top = tkinter.Toplevel(root)

btn2 = tkinter.Button(root, text="Process & Detect",font=("Courier New Bold",10), command=create_window, bg = "salmon1", fg = "black")
btn2.place(relx=.7,rely=.2,anchor='c')
#******************************************************************************




#btn1.pack()
root.mainloop()
#####################
