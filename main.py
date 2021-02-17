from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep
import os
import datetime
import ephem
import math
import cv2

start_time = datetime.datetime.now()
now_time = datetime.datetime.now()

sense = SenseHat()
camera = PiCamera()

imagenumber = 0

#Two-line element set for ISS https://www.celestrak.com/NORAD/elements/stations.txt
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   21043.27289556  .00003336  00000-0  68749-4 0  9997"
line2 = "2 25544  51.6440 240.5646 0002850   6.0842 149.2030 15.48970429269234"
iss = ephem.readtle(name, line1, line2)

#Create and write to csv file
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = dir_path + '/data/data.csv'
with open (filename, "w") as file:
        file.write("time , Image Name , cloud %, mag_x, mag_y, mag_z, pressure, pitch, roll, yaw, equatorial angle, issRA, issDEC\n")
file.close()

#Saves data when it's sunny :)
def saveData():
    while isDay() == True:
        time = datetime.datetime.now()
        mag_x, mag_y, mag_z = get_magnetometer()
        angle, issRA, issDEC = get_isslocation()
        pitch, roll, yaw = get_orientation()
        pressure = get_pressure()
        imageName = takePicture()
        img = cv2.imread('img%d.jpg'%imagenumber)
        cloud = cloud_estimate(img)
        
        with open (filename, "a") as file:
            file.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \n" % (time, imageName, cloud, mag_x, mag_y, mag_z, pressure, pitch, roll, yaw, angle, issRA, issDEC))
        sleep(5)
    main()

def takePicture():
    global imagenumber
    imagenumber += 1
    os.chdir(dir_path + '/data/images') 
    camera.capture('img%d.jpg'%imagenumber)
    return('img%d.jpg'%imagenumber)

#Rough unreliable estimation of cloud percentage with opencv2. Better estimation will be done in phase 4 with pytorch 
def cloud_estimate(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0,0,120), (180,30,255))
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    single_band_img = masked_img[:,:,0]>0
    ncloud_pixel = sum(sum(1*single_band_img))
    total_img_pixel = img[:,:,0].shape[0]*img[:,:,0].shape[1]
    return ncloud_pixel/total_img_pixel

def get_orientation():
    ori = sense.get_orientation()
    pitch = ori["pitch"]
    roll = ori["roll"]
    yaw = ori["yaw"]
    return(pitch, roll, yaw)

#Magnetometer data to be compared with cloud percentage.
def get_magnetometer():
    mag = sense.get_compass_raw()
    mag_x = round(mag["x"],2)
    mag_y = round(mag["y"],2)
    mag_z = round(mag["z"],2)
    return(mag_x, mag_y, mag_z)

def get_isslocation():
    iss.compute()
    sun = ephem.Sun()
    sun.compute()
    angle = float(repr(iss.ra))-float(repr(sun.ra))
    abs_angle = abs(angle)
    return(abs_angle, iss.ra, iss.dec)
  
def get_pressure():
    pressure = sense.get_pressure()
    pressure = round(pressure, 1)
    return(pressure)

#Using ISS TLE to compute the equatorial angle between the sun and the ISS to distingush between night and day
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
    while (now_time < start_time + datetime.timedelta(minutes=2)):
        if isDay() == True:
            print("comma running")
            saveData()
        elif isDay() == False:
            print("comma waiting")
            sleep(600)
            main()
        now_time = datetime.datetime.now()
    print('2 minutes')

if __name__ == '__main__':
    main()