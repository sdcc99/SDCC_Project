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

from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import library_rec as rec

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['EDITED_FOLDER'] = 'static/edited'

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
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        #return 'file uploaded successfully'
        rec.recognition()
        return filename
        #return redirect(url_for('index'))
    #return render_template('index.html', cards=cards)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['EDITED_FOLDER'], filename), mimetype='image/jpeg')

@app.route('/images')
def images():
    files = os.listdir(app.config['EDITED_FOLDER'])
    images = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    #print(','.join(images))
    return ','.join(images)


if __name__ == '__main__':
    app.run(debug=True)





