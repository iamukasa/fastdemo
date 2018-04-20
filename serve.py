from flask import Flask, render_template, request, session,url_for
import messengerbot as a
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/root/fast-style-transfer-1/output'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg',])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def startdis():
  return render_template("base.html")
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['generatefile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('generatedfile',
                                    filename=filename))


@app.route('/generate', methods=['GET','POST'])
def runai():
    image = request.files['generatefile']
    print (image.filename)  
    filename =image.filename
    print(filename)
    theanswer=a.getimagelocal(filename)
    print(theanswer)
   

    return render_template("main.html",theanswer=theanswer)




# app.run(debug=True)
app.run(port=420)
