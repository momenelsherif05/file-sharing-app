from flask import Flask, request, render_template, redirect, url_for
import boto3
import os
from werkzeug.utils import secure_filename

# Initialize the app
app = Flask(__name__)

# S3 Configuration
S3_BUCKET = 'file-share-teamx-2025'  # <-- Replace with your real bucket name
S3_REGION = 'eu-north-1'     # <-- Example: us-east-1

s3 = boto3.client('s3', region_name=S3_REGION)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"

        file = request.files['file']

        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, S3_BUCKET, filename)
            file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
            return f"File uploaded successfully! <a href='{file_url}'>Download here</a>"

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

