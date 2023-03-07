from flask import Flask, request, render_template, send_file, redirect, jsonify
import os
import pika
import json
from markupsafe import escape

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['EDITED_FOLDER'] = 'static/edited'

# VARIABILE AMBIENTE PER I NOMI
app.config['NOMI'] = []

def sendPhoto_to_rabbitmq(foto):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='coda_foto')

    # crea il messaggio da inviare
    messaggio = {
        'foto': foto,
        'tipo_elaborazione': 'riconoscimento_facciale'
    }

    # invia il messaggio alla coda di messaggi
    channel.basic_publish(exchange='', routing_key='coda_foto', body=json.dumps(messaggio))
    print("Messaggio inviato alla coda di messaggi")

    connection.close()

@app.route('/')
def index():
    print("ciao")
    sendPhoto_to_rabbitmq("ciao")
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
        
        #return 'file uploaded successfully'
        #app.config['NOMI'] = rec.recognition()

        ##face_recognition_url = 'http://face_recognition:5000/recognition'
        #files = {'photo': open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')}
        #response = requests.post(face_recognition_url, files=files)

        sendPhoto_to_rabbitmq("/Users/lucadimarco/Desktop/Container/app/static/uploads" + filename)

        return filename

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['EDITED_FOLDER'], filename), mimetype='image/jpeg')

@app.route('/images')
def images():
    nomi = []
    files = os.listdir(app.config['EDITED_FOLDER'])
    images = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    #print(','.join(images))
    immagini = ','.join(images)
    nomi = list(app.config['NOMI'])
    return jsonify({'immagini': immagini, 'nomi': nomi})

# @app.route('/names')
# def names():
#     nomi = []
#     nomi = open("abc.txt", "r").read().split(',')

#     print(nomi)

#     return nomi

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
    sendPhoto_to_rabbitmq("ciao");
    app.run(debug=True)





