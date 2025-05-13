from flask import Flask, request, render_template
from skimage.metrics import structural_similarity
import cv2
import imutils
import numpy as np
from PIL import Image
import os
import time

app = Flask(__name__)

# Configure directories
app.config['INITIAL_FILE_UPLOADS'] = 'uploads'
app.config['EXISTING_FILE'] = 'existing'
app.config['GENERATED_FILE'] = 'static/generated'  # Ensure it's under static for web access

# Create directories if they don't exist
os.makedirs(app.config['INITIAL_FILE_UPLOADS'], exist_ok=True)
os.makedirs(app.config['EXISTING_FILE'], exist_ok=True)
os.makedirs(app.config['GENERATED_FILE'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    # Handle GET request (show form)
    if request.method == "GET":
        return render_template("index.html")

    # Handle POST request (process uploaded image)
    if request.method == "POST":
        # Get uploaded image
        file_upload = request.files['file_upload']
        filename = file_upload.filename

        # Validate file type (only allow images)
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return render_template('index.html', error="Invalid file type. Only PNG, JPG, or JPEG images are allowed.")

        # Save the uploaded image
        uploaded_image_path = os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.png')
        uploaded_image = Image.open(file_upload).resize((250, 160))
        uploaded_image.save(uploaded_image_path)

        # Load and resize the original image
        original_image_path = os.path.join(app.config['EXISTING_FILE'], 'original.png')
        try:
            original_image = Image.open(original_image_path).resize((250, 160))
            original_image.save(original_image_path)  # Save resized version
        except FileNotFoundError:
            return render_template('index.html', error="Original image (original.png) not found on server.")

        # Read images with OpenCV
        original_image_cv = cv2.imread(original_image_path)
        uploaded_image_cv = cv2.imread(uploaded_image_path)

        # Check if images loaded correctly
        if original_image_cv is None or uploaded_image_cv is None:
            return render_template('index.html', error="Failed to load images for processing.")

        # Convert to grayscale
        original_gray = cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image_cv, cv2.COLOR_BGR2GRAY)

        # Calculate SSIM
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")

        # Calculate threshold and contours
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Draw contours
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_image_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(uploaded_image_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save output images
        original_out = os.path.join(app.config['GENERATED_FILE'], 'image_original.png')
        uploaded_out = os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.png')
        diff_out = os.path.join(app.config['GENERATED_FILE'], 'image_diff.png')
        thresh_out = os.path.join(app.config['GENERATED_FILE'], 'image_thresh.png')

        # Save images and check if successful
        if not cv2.imwrite(original_out, original_image_cv):
            return render_template('index.html', error="Failed to save original image.")
        if not cv2.imwrite(uploaded_out, uploaded_image_cv):
            return render_template('index.html', error="Failed to save uploaded image.")
        if not cv2.imwrite(diff_out, diff):
            return render_template('index.html', error="Failed to save difference image.")
        if not cv2.imwrite(thresh_out, thresh):
            return render_template('index.html', error="Failed to save threshold image.")

        # Generate user-friendly message based on SSIM score
        percentage = round(score * 100, 2)
        if score > 0.95:
            message = "The uploaded image matches the original closely. It appears to be genuine."
        elif score > 0.7:
            message = "The uploaded image is similar to the original but has some differences. It may have minor changes."
        else:
            message = "The uploaded image differs significantly from the original. It is likely tampered."
        
        timestamp = str(int(time.time()))
        
        # Return results to template
        return render_template('index.html', 
                               pred=f"{percentage}% correct",
                               message=message,
                               original_img='generated/image_original.png',
                               uploaded_img='generated/image_uploaded.png',
                               thresh_img='generated/image_thresh.png',
                               timestamp=timestamp)

if __name__ == '__main__':
    app.run(debug=True)