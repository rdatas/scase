import os
from flask import Flask, render_template, request, redirect, send_file
from s3_functions import upload_file, show_image, detect_labels
from werkzeug.utils import secure_filename
from logging import FileHandler,WARNING

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
BUCKET = "imagesrg"
UPLOAD_EXTENSIONS = {'png', 'jpg', 'jpeg'}



filename = "Capture.JPG"

@app.route("/")
def home():
    return render_template('index.html')
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

           
@app.route("/upload", methods=['POST','GET'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        if f.filename != '':
            file_ext = f.filename.rsplit('.', 1)[1].lower() 
            if file_ext not in UPLOAD_EXTENSIONS:
                return "Invalid image", 400
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"{UPLOAD_FOLDER}/{f.filename}", BUCKET)
        #labels = detect_labels(f"{UPLOAD_FOLDER}/{f.filename}", BUCKET)
        #return labels
        #return render_template('collection.html', contents=labels)
    #return redirect(url_for('index.html'))
        return redirect("/") 
            
        
@app.route("/pics")
def list():
    contents = show_image(BUCKET)
    return render_template('collection.html', contents=contents)        

@app.route("/analyse")
def rekog(filename):
    #if request.method == "GET":
        #f = request.files['file']
    labels = detect_labels(filename, BUCKET)
    return labels




if __name__ == '__main__':
    app.run(debug=True)