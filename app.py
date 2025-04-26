from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure S3
s3_client = boto3.client('s3')
BUCKET_NAME = 'file-share-teamx-2025'

# File upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route to upload files
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Save file to S3
        s3_client.upload_fileobj(file, BUCKET_NAME, filename)
        return render_template('index.html', filename=filename)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
