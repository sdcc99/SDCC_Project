import face_recognition as fr
import cv2
import numpy as np
import os
import pika
import json

path = "static/train/"

known_names = []
known_name_encodings = []


def elabora_foto_da_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='coda_foto')

    def callback(ch, method, properties, body):
        messaggio = json.loads(body)

        # verifica che il messaggio contenga la foto e il tipo di elaborazione richiesto
        if 'foto' in messaggio and 'tipo_elaborazione' in messaggio and messaggio['tipo_elaborazione'] == 'riconoscimento_facciale':
            foto = messaggio['foto']

            # esegui il riconoscimento facciale sulla foto
            nomi = recognition(foto)

        else:
            print("Messaggio non valido")

    channel.basic_consume(queue='coda_foto', on_message_callback=callback, auto_ack=True)

    print('In attesa di messaggi...')
    channel.start_consuming()


def recognition(immagine):
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
    
    nomi = []
    if immagine.endswith(('.jpeg', '.jpg', '.png')):
        image = cv2.imread(immagine)
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
    
    return nomi
   



