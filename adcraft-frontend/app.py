from flask import Flask, render_template, request, send_file
from PIL import Image, ImageOps
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Process the image (convert to black and white)
        processed_images = process_image(filename)

        return render_template('index.html', images=processed_images)

    else:
        return render_template('index.html', error='File type not allowed')


def process_image(filename):
    original_image = Image.open(filename)

    # Convert to black and white
    bw_image = ImageOps.grayscale(original_image)

    # Save processed images
    bw_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'bw_' + os.path.basename(filename))
    bw_image.save(bw_image_path)

    return [filename, bw_image_path]


@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
