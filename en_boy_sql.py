import cv2 as cv
import numpy as np
import sqlite3 as sq

vid=cv.VideoCapture(1,cv.CAP_DSHOW)
vid.set(11, -8)
vid.set(cv.CAP_PROP_CONTRAST, 500)
vid.set(cv.CAP_PROP_EXPOSURE, -4)


data = np.load("C:/Users/YAZILIM-TALHA/.spyder-py3/deneme/foto/kalibrasyon_sonuclari.npz")
cameraMatrix = data['cameraMatrix']
distCoeffs = data['distCoeffs']
path="C:/Users/YAZILIM-TALHA/.spyder-py3/deneme/foto/en_boy/"
file_number = 1

conn=sq.connect("test.db")
cursor=conn.cursor()

cm=780/16
def deneme(contour,area,image):
    approx=cv.approxPolyDP(contour, 0.01*cv.arcLength(contour, True), True)
    perimeter=cv.arcLength(cont, True)
    img_encode = cv.imencode('.jpg', image)[1] 
  
    data_encode = np.array(img_encode) 
    byte_encode = data_encode.tobytes() 
    
    (s,z,w,h)=cv.boundingRect(contour)
    M = cv.moments(contour) 
    if M['m00'] != 0.0: 
        x = int(M['m10']/M['m00']) 
        y = int(M['m01']/M['m00']) 
  
  
    if len(approx) == 3: 
        cv.putText(frame, 'ücgen', (x, y), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2) 
        
    elif len(approx) == 4:
        
        ratio=w/h
        if(1.2>=ratio>=0.9):
            cv.putText(frame, 'kare', (s, z-30), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            kenar=perimeter/4
            kenar=kenar/cm
            s=(s+(w//2))
            sekil="kare"
            cv.putText(frame, f'kenar: {kenar:.2f}', (x, y-100), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.putText(frame, f'kenar: {kenar:.2f}', (x+100, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            cursor.execute("SELECT * FROM Sekiller WHERE sekil = ?", (sekil,))
            if cursor.fetchone()== None:
                cursor.execute("INSERT INTO Sekiller (sekil, kenar,photo) VALUES ( ?, ?,?)", ( sekil, kenar,byte_encode))
                conn.commit()
            else:
                cursor.execute("UPDATE Sekiller SET kenar=?,photo=? WHERE sekil = ?", (kenar,byte_encode,"kare"))
                conn.commit()
                print("güncellendi.")
        elif(ratio>1.2):
            en=w/cm
            boy=h/cm
            cv.putText(frame, f'en: {en:.2f}', (x, y-100), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.putText(frame, f'boy: {boy:.2f}', (x+150, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.putText(frame, 'dortgen', (x, y-150), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cursor.execute("SELECT * FROM Sekiller WHERE sekil = 'dortgen'")
            if cursor.fetchone()== None:
                cursor.execute("INSERT INTO Sekiller (sekil, en,boy,photo) VALUES ( ?, ?,?,?)", ("dortgen", en,boy,byte_encode))
                conn.commit()
            else:
                cursor.execute("UPDATE Sekiller SET en=?,boy=?,photo=? WHERE sekil = ?", (en,boy,byte_encode,"dortgen"))
                conn.commit()
                print("güncellendi.")
            
        elif(ratio<0.9):
            en=h/cm
            boy=w/cm
            cv.putText(frame, f'en: {boy:.2f}', (x, y-100), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.putText(frame, f'boy: {en:.2f}', (x+150, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv.putText(frame, 'dortgen', (x, y-150), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cursor.execute("SELECT * FROM Sekiller WHERE sekil = 'dortgen'")
            if cursor.fetchone()== None:
                cursor.execute("INSERT INTO Sekiller (sekil, en,boy,photo) VALUES ( ?, ?,?,?)", ("dortgen", en,boy,byte_encode))
                conn.commit()
            else:
                cursor.execute("UPDATE Sekiller SET en=?,boy=?,photo=? WHERE sekil = ?", (en,boy,byte_encode,"dortgen"))
                conn.commit()
                print("güncellendi.")
 
  
    elif len(approx) > 12: 
        cv.putText(frame, 'daire', (x, y), 
                    cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cap=perimeter/np.pi
        cap=cap/cm
        cursor.execute("SELECT * FROM Sekiller WHERE sekil = 'daire'")
        if cursor.fetchone()== None:
            cursor.execute("INSERT INTO Sekiller (sekil,cap,photo) VALUES ( ?, ?,?)", ("daire", cap,byte_encode))
            conn.commit()
        else:
            cursor.execute("UPDATE Sekiller SET cap=?,photo=? WHERE sekil = ?", (cap,byte_encode,"daire"))
            conn.commit()
            print("güncellendi.")

        
        
def SS():
    file_name = f"kameradan_alinan_goruntu_{file_number}.jpg"
    cv.imwrite(path+file_name, frame)
    print(f"{file_name} dosyası başarıyla kaydedildi.")


   

while(vid.isOpened()):
    ret,frame=vid.read()
    if ret==True:
        h,  w = frame.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w,h), 1, (w,h))

        # undistort
        dst = cv.undistort(frame, cameraMatrix, distCoeffs, None, newcameramtx)
        x, y, w, h = roi
        frame = dst[y:y+h, x:x+w]
        frame=cv.resize(frame, [640,480])
        gri=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gaus=cv.GaussianBlur(gri, (3,3), 0)
        ret,thresh=cv.threshold(gaus, 49, 255, cv.THRESH_BINARY_INV)
        edges = cv.Canny(gaus, 71, 165)
        kenar=cv.Canny(gaus,  80, 130)
        kernel=np.ones((3,3),np.uint8)
        dil=cv.dilate(edges,kernel,2)
        
        contour,hi=cv.findContours(dil, cv.RETR_LIST ,cv.CHAIN_APPROX_SIMPLE)
        for cont in contour:
            # Konturun çevresini ve alanını hesapla
            
            area = cv.contourArea(cont)
            
            # Eğer alan belirli bir değerden büyükse (istenilen daireye yakınsa)
            if area > 1000 :
                # Konturun bulunduğu bölgeyi çiz
                contour=cont
                cv.drawContours(frame, [cont], -1, (255, 0, 0), 2)
              
                deneme(contour,area,frame)
        
        # SS()
        # file_number += 1
        # if(file_number==300):
        #     break
       
        cv.imshow("frame", frame)
     

        cv.imshow("kenar", kenar)
        cv.imshow("dil", dil)
        
       
        if cv.waitKey(1)& 0xff==ord('q'):
            cv.destroyAllWindows()
            break
      
    else:
        print("okumadı")
        cv.waitKey(0)
conn.close()
cv.destroyAllWindows()
