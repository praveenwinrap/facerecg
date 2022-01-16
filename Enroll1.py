import cv2
import os
import json
import shutil

details={"id_":"","name":"","rollnumber":""}

paths = ['dataset','config','trainer']


for path in paths:
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
      
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The {} directory is created!".format(path))
  

deci=input("Press Y to Enroll new entry or N to reset the previous records==> ")

if deci == "y":
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    #make sure 'haarcascade_frontalface_default.xml' is in the same folder as this code
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # For each person, enter one numeric face id (must enter number start from 1, this is the lable of person 1)
    face_id = input('\n enter user id end press <return> ==>  ')
    face_name = input('\n enter user name end press <return> ==>  ')
    face_roll = input('\n enter user rollnumber end press <return> ==>  ')
    # Serializing json

    user="user"+str(face_id)
    details.update(id_=face_id)
    details.update(name=face_name)
    details.update(rollnumber=face_roll)
    json_object = json.dumps(details, indent = 4)
    print(type(json_object))
    json_object='"{}":{}'.format(user,json_object)
    print(json_object)
    # Writing to sample.json
    with open("config/details.json", "a") as outfile:
        outfile.write(",")
        outfile.write(json_object)
        outfile.close()
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0
    while(True):

        ret, img = cam.read()
        img= cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 50: # Take 30 face sample and stop video
             break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
else:
    try:
        shutil.rmtree('dataset')
        shutil.rmtree('config')
        shutil.rmtree('trainer')
    except Exception as e:
        print("Folder not found=>"+str(e))
    
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1+ "}" 
        
        
# Driver code
try:
    fd = open("config/details.json","r")
    s=str(fd.read())
    s=list(s)
    #print(s)
    s[0]= str("{")
    conv=listToString(s)
except:
    pass
#add code to delete the content , and add processed content praveen

try:
    fd1 = open("config/details_f.json","w")
    fd1.write(conv)
    fd.close()
    fd1.close()
    print(conv)
except:
    pass
