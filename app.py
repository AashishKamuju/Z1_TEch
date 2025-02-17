from flask import Flask, render_template, request, redirect, url_for, flash
import os
from PIL import Image

app = Flask(__name__)
app.secret_key = os.urandom(24)  

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

IMAGE_SIZES = [
    (300, 250),
    (728, 90),
    (160, 600),
    (300, 600)
]

UPLOAD_FOLDER = 'static/uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path, output_path, size):
    try:
        with Image.open(image_path) as img:
            img = img.resize(size, Image.LANCZOS)
            img.save(output_path)
    except Exception as e:
        print(f"Error resizing image: {e}")
        flash("Error processing image resizing.")
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image uploaded.')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No image selected.')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a PNG, JPG, JPEG, or GIF image.')
            return redirect(request.url)

        try:
            width = int(request.form['width'])
            height = int(request.form['height'])
        except ValueError:
            flash('Invalid width or height.')
            return redirect(request.url)

        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            resized_filename = f"{width}x{height}_{file.filename}"
            resized_path = os.path.join(app.config['UPLOAD_FOLDER'], resized_filename)
            resize_image(filepath, resized_path, (width, height))

            image_url = f"https://yourwebsite.com/static/uploads/{resized_filename}"
            tweet_url = f"https://twitter.com/intent/tweet?text=Check+out+this+awesome+image!&url={image_url}"

            flash('Image uploaded and resized successfully!')
            return render_template('index.html', tweet_url=tweet_url)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            flash("An unexpected error occurred. Please try again.")
            return redirect(request.url)

    return render_template('index.html', tweet_url=None)


if __name__ == '__main__':
    app.run(debug=True)
