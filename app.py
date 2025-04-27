from flask import Flask, request, render_template, redirect, url_for
import boto3
import os
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__)

# AWS S3 configuration
S3_BUCKET = 'file-share-teamx-2025'  # Replace with your S3 bucket name
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types
s3 = boto3.client('s3')  # S3 client setup

# Function to check if file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for uploading files
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    download_url = None  # Variable to store the generated download link
    if request.method == 'POST':
        # Check if the 'file' is in the request
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        
        # If the user didn't select a file
        if file.filename == '':
            return 'No selected file'

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Secure the filename before uploading
            filename = secure_filename(file.filename)
            
            # Upload the file to S3
            s3.upload_fileobj(file, S3_BUCKET, filename)

            # Generate the download URL for the file
            download_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

            return render_template('upload.html', download_url=download_url)  # Show the download link

    return render_template('upload.html', download_url=download_url)  # Render the page

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)



