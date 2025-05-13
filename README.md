# Image Tampering Detection App

A Flask-based web app to detect image tampering by comparing an uploaded image against a reference image (`original.png`) using Structural Similarity Index (SSIM). Displays a similarity percentage, a user-friendly message, and visual differences with contours.

## Features
- Upload an image to check for tampering.
- Compares against `existing/original.png`.
- Shows similarity as a percentage (e.g., "96.67% correct").
- Provides a message (e.g., "The uploaded image matches the original closely. It appears to be genuine.").
- Displays three images: Original (with contours), Uploaded (with contours), and Threshold (differences).

## Project Structure
```
image-tampering-detection/
├── app.py
├── templates/
│ └── index.html
├── static/
│ └── styles.css
├── uploads/ (created dynamically)
├── existing/
│ └── original.png (required reference image)
├── static/generated/ (created dynamically)
├── requirements.txt
├── Procfile
├── runtime.txt
└── README.md
```

## Prerequisites
- Python 3.11.12 (specified in `runtime.txt`).
- Heroku CLI: [Install](https://devcenter.heroku.com/articles/heroku-cli).
- Git: [Install](https://git-scm.com/downloads).
- Heroku account: [Sign up](https://www.heroku.com).

## Local Setup
1. **Clone or Copy Files**:
   ```bash
   git clone <repository-url>
   cd image-tampering-detection

2. **Install Dependencies:**

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. **Add Reference Image:**
- Place your reference image as ```existing/original.png``` (flattened PNG, no transparency).

4. **Run Locally:**
```python app.py```

# Deploy to Heroku

1. **Initialize Git:**
```git init```

2. **Add files:**
```git add . ```
3. **Commit:**
```git commit -m "Deploy to Heroku"```
4. **Login to Heroku:**
```heroku login```
5. **Create App:**
```heroku create your-app-name```
6. **Deploy:**
```git push heroku master```
7. **Scale Dyno:**
```heroku ps:scale web=1```
8. **Open App:**
```heroku open```
# Usage
- Upload an image (PNG, JPG, JPEG).

- Results include:

## Message:

- 95%: "The uploaded image matches the original closely. It appears to be genuine."

- 70–95%: "The uploaded image is similar to the original but has some differences. It may have minor changes."

- <70%: "The uploaded image differs significantly from the original. It is likely tampered."

- Similarity: E.g., "96.67% correct".

- Images: Original, Uploaded, and Threshold with red contours on tampered areas.

## Troubleshooting
- Images Not Showing: Check logs (heroku logs --tail). Ensure static/generated images are saved. Heroku’s file system is ephemeral; consider AWS S3 for persistent storage.

- Memory Issues: Free dynos have 512MB limit. Reduce image size or upgrade dyno if "R14 - Memory quota exceeded" occurs.

- Original Image Missing: Ensure existing/original.png is in the Git repository.

# Dependencies
- Flask, scikit-image, opencv-python-headless, imutils, Pillow, numpy, gunicorn (see requirements.txt).


---

### **Explanation of SSIM Algorithm**

**SSIM (Structural Similarity Index)** is an algorithm used to measure the similarity between two images. It compares the structural content of the images and calculates a score between 0 and 1 (or 0% to 100% when expressed as a percentage).

- **High SSIM value (close to 1 or 100%)** means that the images are **similar** or **identical**.
- **Low SSIM value (close to 0 or 0%)** indicates that the images are **significantly different**, which is often used to detect tampering or changes in images.

### **SSIM Steps:**
1. **Luminance Comparison**: Measures the brightness or intensity similarity between images.
2. **Contrast Comparison**: Measures the contrast similarity between the two images.
3. **Structure Comparison**: Measures the structural similarity, ensuring the image has similar textures and shapes.

### **Image Authentication Methods**:
- **SSIM (Structural Similarity Index)**: Compares structural changes between images, typically used for tampering detection.
- **MSE (Mean Squared Error)**: Measures pixel-by-pixel differences between two images.
- **Histogram Comparison**: Compares the color distribution of two images.
- **Hashing**: Generates a hash value of an image and compares it with another image’s hash.
- **Watermarking**: Embeds a hidden message or pattern inside an image to prove its authenticity.

---

### **Concise Terminal Instructions**

To **deploy your app** and use the **SSIM image comparison**, here are the terminal commands in sequence:

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd image-tampering-detection
2. **Create Virtual environment:**
```
python -m venv venv
source venv/bin/activate  
```
3. **Install dependencies:**
``` pip install -r requirements.txt```
4. **Run locally:**
```python app.py```
5. **Deploy to Heroku:**
```
git init
git add .
git commit -m "Deploy to Heroku"
heroku login
heroku create
git push heroku master
heroku ps:scale web=1
heroku open
```