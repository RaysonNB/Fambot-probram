import cv2
print(cv2.haarcascades)
path = cv2.haarcascades + "haarcascade_frontalface_default.xml"
model = cv2.CascadeClassifier(path)
print(model)
camera = cv2.VideoCapture(0)
while camera.isOpened(): 
    success,frame = camera.read()
    if not success:
        break


    fh, fw, fc = frame.shape
    rx1, rx2 = fw//2-150, fw//2+150
    ry1, ry2 = fh//2-150, fh//2+150
    cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)
    outputs = model.detectMultiScale(frame)

    print(outputs)
    for box in outputs:
        x,y,w,h=box
        inside = True
        if x < rx1 or x >= rx2 or y < ry1 or y > ry2:
            inside = False
        if x+w < rx1 or x+w >= rx2 or y+h < ry1 or y+h > ry2:
            inside = False
        color = (0, 255, 0)
        if not inside:
            color = (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    '''    if x+w/2 > fw/2:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0,0), 5)
    h,w,c=frame.shape
    frame[0:h//2, 0:w//2, (1, 2)] = 0
    frame[0:h//2, w//2:w, (0, 2)] = 0
    frame[h//2:h, 0:w//2 ,(0,1)] = 0
    frame[h//2:h:, w//2:w, 0] = 0
    frame[h//4:h//4*3, w//4:w//4*3, (0, 1)] = 255'''
    cv2.imshow("i am funking you", frame)
    key_code = cv2.waitKey(1)
    if key_code in [27, ord('q')]: 
        break
camera.release()
cv2.destroyAllWindows()
