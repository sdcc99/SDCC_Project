import face_recognition as fr
import cv2
import numpy as np
import os

path = "static/train/"

known_names = []
known_name_encodings = []

def recognition():
    images = os.listdir(path)

    #print(images)
    
    #ciclo per imparare i volti
    for _ in images:
        #print(path + _)
        if not _.startswith('.'):
            image = fr.load_image_file(path + _)
            image_path = path + _
            encoding = fr.face_encodings(image)[0]
            
            #print(encoding)

            known_name_encodings.append(encoding)
            known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

    #print(known_names)

    #test_image = "static/uploads/imageP.png"
    
    #ciclo che scorre tutte le foto nella cartella uploaded e per ognuna verifica se conosce 
    # qualcuno e mette nella cartella modified l'output 
    uploaded = os.listdir("static/uploads/")
    nomi = []
    for immagine in uploaded:
        if immagine.endswith(('.jpeg', '.jpg', '.png')):
            image = cv2.imread("static/uploads/" + immagine)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            face_locations = fr.face_locations(image)
            face_encodings = fr.face_encodings(image, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(known_name_encodings, face_encoding)
                name = ""

                face_distances = fr.face_distance(known_name_encodings, face_encoding)
                best_match = np.argmin(face_distances)

                if matches[best_match]:
                    name = known_names[best_match]
                    if (name not in nomi):
                        nomi.append(name)
                
                
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(image, (left, bottom - 60), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left + 6, bottom - 6), font, 3.0, (255, 255, 255), 2)


            #cv2.imshow("Result", immagine)
            percorso = "static/edited/" + immagine
            #print(percorso)
            cv2.imwrite(percorso, image)
    #print(nomi)
    return nomi
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()



