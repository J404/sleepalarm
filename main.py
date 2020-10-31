import cv2
from sound import *

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

video_capture = cv2.VideoCapture(0)

sound_playing = False
found_eyes = False
num_eyes = 0
frames_with_eyes_closed = 0

while True:
    ret, img = video_capture.read()
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grayscale, 1.05, 10)

    for (x, y, w, h) in faces:
        num_eyes = 0

        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        eye_gray = grayscale[y:y+h, x:x+w]
        eye_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(eye_gray, 1.03, 35, minSize=(int(w * 0.32), int(h * 0.32)), maxSize=(int(w * 0.35), int(h * 0.35)))

        for (eye_x, eye_y, eye_w, eye_h) in eyes:
            cv2.rectangle(eye_color, (eye_x, eye_y), (eye_x + eye_w, eye_y + eye_h), (0, 0, 255), 2)
            frames_with_eyes_closed = 0
            num_eyes += 1

            #print(f'Face width is {w} and eye width is {eye_w}. Eye percent of face is {eye_w / w}')
            #print(f'Face height is {h} and eye height is {eye_h}. Eye percent of face is {eye_h / h}')

        if found_eyes == False and num_eyes > 0:
            found_eyes = True
        
        if found_eyes == True and num_eyes == 0:
            #eyes closed
            print('Eyes closed!')
            frames_with_eyes_closed += 1

            if frames_with_eyes_closed > 100:
                found_eyes = False
                alarm()
                frames_with_eyes_closed = 0
            
        elif found_eyes == True and sound_playing == True:
            sound_playing = False
            print('Eyes open!')


    cv2.imshow('View', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
