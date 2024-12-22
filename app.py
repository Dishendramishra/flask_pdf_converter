from flask import *
from flask_cors import CORS
from fileinput import filename
import pdf_converter
from werkzeug.utils import secure_filename
import os
import glob
import uuid
from pprint import pprint

ALLOWED_EXTENSIONS = {'pdf'}
UPLOAD_FOLDER = 'data'

app = Flask(__name__)
app.secret_key = "yesthatmuchstrong"
CORS(app, expose_headers=["Content-Disposition"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/upload_file', methods = ['POST'])   
def upload_file():
    if request.method == 'POST':   
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file'] 
        
        if file.filename == '':
            return('No selected file')

        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                prefix = uuid.uuid4().hex
                
                input_filename = prefix+filename
                filename_with_path = os.path.join(app.root_path, "data", input_filename)
                file.save(filename_with_path)            
                output_filename = pdf_converter.convert_pdf(filename_with_path)
                return render_template("download.html", filename=output_filename)
            
            except Exception as e:
                return render_template("convert_error.html")
        else:
            return """<div class="alert alert-danger" role="alert">
                    Only PDF files are allowed!
                    </div>"""

@app.route('/uploaded_info')
def uploaded_info():
    return "200"

@app.route('/download_file/<name>')
def download_file(name): 
    # return send_from_directory(app.config["UPLOAD_FOLDER"], name)

    return send_file(
        os.path.join(app.config["UPLOAD_FOLDER"], name),
        as_attachment=True,
    )

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0', port='80')