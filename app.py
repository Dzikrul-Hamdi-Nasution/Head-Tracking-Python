import cv2
import serial


from pygame import mixer

mixer.init()
mixer.music.load("suara.mp3")



 

arduino = serial.Serial('COM3', 9600)

# distance from camera to object(face) measured
# centimeter
Known_distance = 130
offset = 70 
offset_bicara = 50



Known_width = 5
jarak_koordinat = 0
jarak = 0
pengunci = 0
kunci_tengah = 1
# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
# defining the fonts
fonts = cv2.FONT_HERSHEY_COMPLEX
 
# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
 
# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
 
    # finding the focal length
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length
 
# distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
 
    distance = (real_face_width * Focal_Length)/face_width_in_frame
 
    # return the distance
    return distance
 


def face_data(image):
 
    face_width = 0  # making face width to zero
 
    global kunci_tengah
    global pengunci
   
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    # detecting face in the image
    faces = face_detector.detectMultiScale(gray_image, 1.2, 8)
 
    # looping through the faces detect in the image

    for (x, y, h, w) in faces:
        
        # draw the rectangle on the face
        jarak_koordinat = x
        cv2.putText(image, str(jarak), (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (RED), 2)

        

        if jarak < offset :
            cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 5)
        else:
            cv2.rectangle(image, (x, y), (x+w, y+h), RED, 3)
     
        if jarak_koordinat > 510 :
            arduino.write(bytes("1", 'utf-8'))
            print("Hadap Kanan " + str(jarak_koordinat) )
            kunci_tengah = 1

            
        if jarak_koordinat > 510 and jarak_koordinat < 490:
            arduino.write(bytes("4", 'utf-8'))

        
            
        if jarak_koordinat < 490 :
            arduino.write(bytes("2", 'utf-8'))
            print("Hadap Kiri " + str(jarak_koordinat))
            kunci_tengah = 2


        if jarak < offset_bicara :
            if pengunci == 0 :
                pengunci = 1
                arduino.write(bytes("5", 'utf-8'))
                arduino.write(bytes("3", 'utf-8'))
                mixer.music.play()
    
        
                
           
            
        
 
        face_width = w
    return face_width
 
 
ref_image = cv2.imread("objeto_0.jpg")
 
ref_image_face_width = face_data(ref_image)
 
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)
 
print(Focal_length_found)
 

#cv2.imshow("ref_image", ref_image)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    
    # reading the frame from camera
    _, frame = cap.read()
 
    face_width_in_frame = face_data(frame)
 
    if face_width_in_frame != 0:
       
        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)
 
        # draw line as background of text
       
        
        jarak = round(Distance,2)
        
            
              
            
            


    else :
        arduino.write(bytes("4", 'utf-8'))
        print("Netral " + str(jarak_koordinat))
        pengunci = 0
        
    
   
        

    # show the frame on the screen
    cv2.imshow("frame", frame)
 
    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break
 

cap.release()

cv2.destroyAllWindows()