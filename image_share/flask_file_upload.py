#!/usr/bin/env python3
"""
Python 3.8

Uploading images to S3.
"""
import mimetypes
import os
import uuid

import boto3
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename


BUCKET_NAME = 'image-share-public'
DIRECTORY = 'test'
FILE_FORM_NAME = 'file'


app = Flask(__name__)


def generate_unique_filename(filename):
    """Generates a unique filename with the correct extension."""

    uuid_ = uuid.uuid4()

    mime_type, _encoding = mimetypes.guess_type(filename)
    extension = mimetypes.guess_extension(mime_type)
    
    unique_filename = f"{uuid_}{extension}"

    return unique_filename


def upload_to_s3(key, file_to_upload, mime_type, bucket_name=BUCKET_NAME):
    """Uploads a file to S3."""
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(
        Key=key,
        Body=file_to_upload,
        ContentType=mime_type
    )


@app.route('/upload')
def upload_file_site():
    """Serves the upload page."""
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    """Handles the file upload from the form."""
    if request.method == 'POST':
        # Get file from form response.
        file_to_upload = request.files[FILE_FORM_NAME]

        # Generate filename.
        filename_from_user = file_to_upload.filename
        filename = generate_unique_filename(filename_from_user)

        # Extract the MIME type so that S3 knows what it is.
        mime_type, _encoding = mimetypes.guess_type(filename_from_user)
        
        key = os.path.join(DIRECTORY, filename)

        # Upload to S3.
        upload_to_s3(key, file_to_upload, mime_type)

        print(f"Succesfully uploaded file as {key}")
        public_file_url = f"https://{BUCKET_NAME}.s3-us-west-2.amazonaws.com/{key}"
        print(f"You should be able to access this file at {public_file_url}")

        response = {
            'url': public_file_url
        }

        return jsonify(response)


@app.route('/')
def image_clipboard():
    return app.send_static_file('index.html')


@app.route('/upload-image')
def image_clipboard_accept():
    return "Image"

		
if __name__ == '__main__':
    port = 1343
    site_url = f'http://localhost:{port}/upload'
    print(f"Site starting at {site_url}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True)