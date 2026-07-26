from flask import Flask, render_template, request, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from dehaze.dehaze_utils import dehaze_image

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('dashboard.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('dashboard.html', error='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uniq = uuid.uuid4().hex[:8]
            base, ext = os.path.splitext(filename)
            input_filename = f"{base}_{uniq}{ext}"
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            file.save(input_path)
            output_filename = f"dehazed_{base}_{uniq}{ext}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            try:
                output_path, metrics = dehaze_image(input_path, output_path)
            except Exception as e:
                return render_template('dashboard.html', error=f'Processing failed: {str(e)}')
            dehazed_img_url = url_for('static', filename=f'uploads/{output_filename}')
            input_img_url = url_for('static', filename=f'uploads/{input_filename}')
            return render_template('dashboard.html',
                                   input_img=input_img_url,
                                   output_img=dehazed_img_url,
                                   metrics=metrics)
        else:
            return render_template('dashboard.html', error='Invalid file type')
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
