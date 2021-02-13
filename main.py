from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep
import os
<<<<<<< HEAD
import datetime
=======
from picamera import PiCamera
>>>>>>> 432798788455b96504889d500e280c963a5744bb
import ephem
import math
import cv2

sense = SenseHat()
camera = PiCamera()
<<<<<<< HEAD
mag = sense.get_compass_raw()

imagenumber = 0
=======
# sense.show_message("Hello")
>>>>>>> 432798788455b96504889d500e280c963a5744bb

#Two-line element set for ISS
#https://www.celestrak.com/NORAD/elements/stations.txt
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21043.27289556  .00003336  00000-0  68749-4 0  9997"
line2 = "2 25544  51.6440 240.5646 0002850   6.0842 149.2030 15.48970429269234"
iss = ephem.readtle(name, line1, line2)

<<<<<<< HEAD
#Create and write to csv file
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path + '/data/data.csv'
with open (filename, "w") as file:
        file.write("time , Image Name , cloud %, mag_x, mag_y, mag_z, ISS location dec, ISS location ra \n")
file.close()
=======
imagenumber = 0

>>>>>>> 432798788455b96504889d500e280c963a5744bb

#Saves data when it's sunny :)
def saveData():
<<<<<<< HEAD
    time = datetime.datetime.now()

    while isDay() == True:
        imageName = takePicture()
        img = cv2.imread('img%d.jpg'%imagenumber)
        cloud = cloud_estimate(img)
        now_time= datetime.datetime.now()
        mag_x = round(mag["x"],2)
        mag_y = round(mag["y"],2)
        mag_z = round(mag["z"],2)
        iss.compute()
        locationDEC = iss.dec
        locationRA = iss.ra

        with open (filename, "a") as file:
            file.write("%s, %s, %s, %s, %s, %s, %s, %s,  \n" % (time, imageName, cloud,mag_x, mag_y, mag_z, locationDEC, locationRA))
        sleep(5)
    main()

def takePicture():
    global imagenumber
    imagenumber += 1
    os.chdir(dir_path + '/data/images') 
    camera.capture('img%d.jpg'%imagenumber)
    return('img%d.jpg'%imagenumber)

#Estimates cloud percentage.
def cloud_estimate(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,0,120), (180,30,255))
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    single_band_img = masked_img[:,:,0]>0
    ncloud_pixel = sum(sum(1*single_band_img))
    total_img_pixel = img[:,:,0].shape[0]*img[:,:,0].shape[1]
    return ncloud_pixel/total_img_pixel

#Using ISS TLE to compute the equatorial angle between the sun and the ISS
=======
	dir_path = os.path.dirname(os.path.realpath(__file__))
	filename = dir_path + '/test.csv'

	currentTime = datetime.datetime.now()

	with open (filename, "w") as file:
		file.write("time , Temperature , pressure \n")

	while now_time < start_time + duration:
		t = sense.get_temperature()
		p = sense.get_pressure()
		now_time= datetime.datetime.now()

		with open (filename, "a") as file:
			file.write("%s, %s, %s  \n" % (currentTime, t,p))
		sleep(1)

def takePicture():
	imagenumber += 1
	camera.capture('img%d.jpg'%imagenumber)


def commastart():
	pass

def getLocation():
	pass


#Using posistions from the TLE set to check if it's day on ISS
>>>>>>> 432798788455b96504889d500e280c963a5744bb
def isDay():
    iss.compute()
    
    sun = ephem.Sun()
    sun.compute()
    
    angle = float(repr(iss.ra))-float(repr(sun.ra))
    
    abs_angle = abs(angle)

    if 3/2*math.pi > abs_angle > math.pi/2:
        return False
    else:
        return True

def main():
    if isDay() == True:
        print('Daytime comma starting')
        saveData()
    elif isDay() == False:
        print('Nighttime comma waiting')
        sleep(600)
        main()

if __name__ == '__main__':
    main()

