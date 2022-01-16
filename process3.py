import cv2
import numpy as np
import os 
import json
import openpyxl
import time
from datetime import datetime

book = openpyxl.Workbook()
sheet = book.active 
now = time.strftime("%x")
book.save("Attendance.xlsx")
workbook_obj = openpyxl.load_workbook("Attendance.xlsx")
sheet_obj = workbook_obj.active
col1 = 'Name'
col2 = 'RollNumber'
col3 = 'Time'
sheet_obj.append([col1, col2,col3])
workbook_obj.save("Attendance.xlsx")

recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')   #load trained model
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter, the number of persons you want to include
id = 100 #two persons 

f = open('config/details_f.json')
names=[''] 
# returns JSON object as
# a dictionary
data = json.load(f)
#print(data)
for user in data:
   # print(data[user]["id_"])
   # print(data[user]["name"])
    #print(data[user]["rollnumber"])
    names.append(data[user]["name"])
print(names)
#names = ['','Praveen','wamika','kumar','nothing','pranay','kalyani',]  #key in names, start from the second place, leave first empty

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    img= cv2.flip(img, 1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        local_usr="user"+str(id)
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            first_column = sheet_obj['A']
            colums=[]

# Print the contents
            for x in range(len(first_column)):
                colums.append(first_column[x].value)
            if id not in colums:
                tt=datetime.now()
                tt=tt.strftime("%d/%m/%Y %H:%M:%S")
                sheet_obj.append([id, data[local_usr]["rollnumber"],tt])
                workbook_obj.save("Attendance.xlsx")    
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
