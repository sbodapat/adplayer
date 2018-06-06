
#! Author S Mahesh Gupta
#! Version 1.0

import time
time.sleep(60) # wait upto boot process complete
from flask import *
import RPi.GPIO as GPIO
import subprocess
import sys
import os
import glob
import keyboard
import webbrowser

a=subprocess.Popen(["chromium-browser","--incognito", "http://0.0.0.0:5000/","--start-fullscreen"])  # Open browser and run videos at program execution starts
app= Flask(__name__, static_folder="/media/pi/SOWMYA/static",static_url_path="/media/pi/SOWMYA/static") # Videos and Imagesg Input Path (Here From Pendrive)
globalvidnumber=len(glob.glob("/media/pi/SOWMYA/static/*.mp4"))  #two variables to take care of looping part.
globalvideocount=-1 # video count
mobile_num = 0 # mobile number
a = 0 # Interrupt flag

GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # Interrupt Pin

def test(channel):  # Interrupt function
	global a
	print('Enteringtheloop')
	os.system("sudo killall chromium-browser") # closing all previous crome browsers
	a=subprocess.Popen(["chromium-browser","http://0.0.0.0:5000/interruptslides","--start-fullscreen"]) # Open Interrupt Slides in Full screen
	print('End of the slides')
	a = 1 # setting flag for interrupt occured indication


GPIO.add_event_detect(17,GPIO.RISING,callback=test,bouncetime=50000)	
#use raspberrypi gpio setup and detection here. callback->interruptslides()

@app.route("/")
def home():    #main homepage where looping takes place
    global globalvideocount
    global globalvidnumber
    global a
    global mobile_num
	
    print("start home: ")
	
    if a: # checking flag of interrupt so that we can do our operations
        pr1 = open("/home/pi/print_doc.txt","r") // # open user message
        data = pr1.readlines() # reaing the use message
        pr1.close()
        pr2 = open("/home/pi/final_pri.txt","w") # open printer message doc and write what to print
        for i in data:
            pr2.write(str(i)) # writiing user message
        pr2.write("MOBILE: ") 
        pr2.write(str(mobile_num)) # writing mobile number
        pr2.write("\r\n")
        pr2.write(".................")
        pr2.close()
        os.system("lp /home/pi/final_pri.txt") # printing the final message 
        globalvideocount = -1
        a = 0 # clear the interrupt flag
        pr3 = open("/home/pi/print_mob.txt","a") # open mobile number saving log
        pr3.write("Mobile: ")
        pr3.write(str(mobile_num)) # writing mobile number in to the log
        pr3.write("\r\n")
        pr3.close()
    
    if globalvideocount==globalvidnumber-1: # checking video count if maximum-1 then again set to -1
        globalvideocount=-1

    globalvideocount+=1 # for next video
    print("End home")
    return render_template("home.html",filenameargument=glob.glob("/media/pi/SOWMYA/static/*.mp4")[globalvideocount].split("/media/pi/SOWMYA/static/")[1]) # input to html file here give the path to videos (here i given from pendrive)

@app.route("/bottleinterrupt")
def bottleinterrupt():    #this gets called whenever bottle is put in
    print("start bottleinterrupt")
    return render_template("bottle.html") # for mobile number validtion
    

@app.route("/interruptslides")
def interruptslides(): # Interrupt slides 
    print("start interruptslides")
    return render_template("interruptslides.html",numofslides=len(glob.glob("/media/pi/SOWMYA/static/*.jpg")),filelist=sorted(glob.glob("/media/pi/SOWMYA/static/*.jpg"))) # input to html file here give the path to Images (here i given from pendrive)

@app.route("/submit",methods=["GET","POST"])
def submit():
    global mobile_num
    mobile_num=request.args.get('mobile')
    print(mobile_num)
    return render_template("submit.html",mobile=request.args.get('mobile'))

if __name__ == '__main__':
   app.run(host='0.0.0.0')