import cv2
import mediapipe as mp
import pyautogui
#Obtendo o video da webcam ou seja 0
cap = cv2.VideoCapture(0)

#obtem as marcações das mãos 
hand_detector = mp.solutions.hands.Hands()

#Ferramenta de desenho mediapipe
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

index_y = 0
INDICATOR_LANDMARK = 8
THUMB_LANDMARK = 4

#loop de ação infinita do video 
while True:
    _,frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame,hand)
            landmarks = hand.landmark

            for id,landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
               
                #print(x,   y)
                if id == INDICATOR_LANDMARK:
                    cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    pyautogui.moveTo(index_x, index_y)
                
                if id == THUMB_LANDMARK:
                    cv2.circle(img=frame, center=(x,y) , radius=10,color=(0,255,255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y

                    #print(abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 28:
                        pyautogui.click()
                        pyautogui.sleep(1)
      
    cv2.imshow('Virtual Mouse',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break