from flask import Flask, request, render_template, send_file, redirect, jsonify
import os
import pika
import json
from markupsafe import escape
import base64

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['EDITED_FOLDER'] = 'static/edited'

# VARIABILE AMBIENTE PER I NOMI
app.config['NOMI'] = []

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='coda_foto')

channel2 = connection.channel()
channel2.queue_declare(queue='coda_receive')

#CALLBACK DI CONSUMER
def callback(ch, method, properties, body):
    print("SONO QUI IN SERVER2!!!!!")
    #print("Received message:", body)
    decoded_image = base64.b64decode(body)
    with open(os.path.join(app.config['EDITED_FOLDER'],"received_image.png"), "wb") as image_file:
        image_file.write(decoded_image)
    return redirect("/")

#PRODUCER
def sendPhoto_to_rabbitmq(encoded_string):
    # crea il messaggio da inviare
    # messaggio = {
    #     'foto': foto,
    #     'tipo_elaborazione': 'riconoscimento_facciale'
    # }

    # invia il messaggio alla coda di messaggi
    channel.basic_publish(exchange='', routing_key='coda_foto', body=encoded_string)
    print("Messaggio inviato alla coda di messaggi")

    channel2.basic_consume(queue='coda_receive', on_message_callback=callback, auto_ack=True)
    print('In attesa di messaggi...')
    channel.start_consuming()

    #connection.close()

@app.route('/')
def index():
    return render_template('index.html')    #cards=cards

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    nomi = []
    if request.method == 'POST':
        #ciclo per eliminare tutto ciò che è contenuto nella cartella UPLOAD
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))       

        #ciclo per eliminare tutto ciò che è contenuto nella cartella EDITED
        for filename in os.listdir(app.config['EDITED_FOLDER']):
            file_path = os.path.join(app.config['EDITED_FOLDER'], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        
        #return 'file uploaded successfully'
        #app.config['NOMI'] = rec.recognition()

        sendPhoto_to_rabbitmq(encoded_string)

        return filename

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['EDITED_FOLDER'], filename), mimetype='image/jpeg')

@app.route('/images')
def images():
    nomi = []
    print("SONO QUI IN SERVER3!!!!!")
    files = os.listdir(app.config['EDITED_FOLDER'])
    images = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    #print(','.join(images))
    immagini = ','.join(images)
    nomi = list(app.config['NOMI'])
    return jsonify({'immagini': immagini, 'nomi': nomi})

@app.route('/sendemail/<nome>', methods=['GET', 'POST'])
def send_email(nome):
    #print(nome)
    if request.method == 'POST':
        ##sendemail.send("Come procede la giornata?", nome)
        return redirect("/")
        #return 0
        #return redirect(url_for('index'))
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





