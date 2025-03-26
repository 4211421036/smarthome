import cv2
import mediapipe as mp
import time
import controller as cnt
 
time.sleep(2.0)

mp_draw=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands

tipIds=[4,8,12,16,20]

video=cv2.VideoCapture(0)

cnt.sendTelMessage("Selamat Datang!")

with mp_hand.Hands(min_detection_confidence=0.5,
               min_tracking_confidence=0.5) as hands:
    while True:
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList=[]
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands=results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers=[]

        valuePir = cnt.pirPin.read()
        valueHujan = cnt.hujanPin.read()
        valueAsap = cnt.asapPin.read()
        print(f"Sensor PIR Value: {valuePir}")
        print(f"Sensor Hujan Value: {valueHujan}")
        print(f"Sensor Asap Value: {valueAsap}")
        cnt.sleep(0.5)
        if float(valuePir) < 0.30:
            cnt.alarmAnnou(cnt.buzzerPin, "Terdeteksi Gerakan!")
            cnt.sleep(0.5)
        elif float(valueHujan) > 0.80:
            cnt.alarmAnnou(cnt.buzzerPin, "Cuaca Hujan!")
            cnt.sleep(0.5)
        elif float(valueAsap) > 0.30:
            cnt.alarmAnnou(cnt.buzzerPin, "Terdeteksi Gas Bocor!")
            cnt.sleep(0.5)
        else:
            cnt.sendTelMessage("Aman")
            cnt.sleep(2)
        if len(lmList)!=0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total=fingers.count(1)
            cnt.led(total)
            if total==0:
                cv2.putText(image, "Relay 1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "Menyala", (300, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
            elif total==1:
                cv2.putText(image, "Relay 1", (45, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
                cv2.putText(image, "Mati", (220, 375), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 5)
        cv2.imshow("Smart Home App",image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('w'):
            break

video.release()
cv2.destroyAllWindows()
