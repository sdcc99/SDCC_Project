# from flask import Flask, render_template
# app = Flask(__name__)

# @app.route('/')
# def index():
#   return render_template('index.html')

# @app.route('/my-link/')
# def my_link():
#   print ('I got clicked!')

#   return 'Click.'

# if __name__ == '__main__':
#   app.run(debug=True)

from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import os
import library_rec as rec
import sendemail

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['EDITED_FOLDER'] = 'static/edited'

# VARIABILE AMBIENTE PER I NOMI
app.config['NOMI'] = []

@app.route('/')
def index():
    # #return render_template('index.html')
    # # ottieni una lista di tutti i file presenti nella cartella "uploads"
    # files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if not f.startswith('.') and not f.endswith('.DS_Store')]
    
    # # crea una lista di card Bootstrap per ogni file presente nella cartella "uploads"
    # cards = []
    # for file in files:
    #     card = """
    #     <div class="card" style="width: 18rem;">
    #         <img src="{{ url_for('static', filename='uploads/%s') }}" class="card-img-top" alt="...">
    #         <div class="card-body">
    #             <p class="card-text">%s</p>
    #         </div>
    #     </div>
    #     """ % (file, file)
    #     cards.append(card)
    
    # restituisci la pagina HTML con tutte le card Bootstrap
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
        app.config['NOMI'] = rec.recognition()
        #print(nomi)
        return filename
        #return redirect(url_for('index'))
    #return render_template('index.html', cards=cards)

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

@app.route('/names')
def names():
    nomi = []
    nomi = open("abc.txt", "r").read().split(',')

    print(nomi)

    return nomi

@app.route('/sendemail/<nome>', methods=['GET', 'POST'])
def send_email(nome):
    print(nome)
    if request.method == 'POST':
        #sendemail.send("helo")
        return 0
        #return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





