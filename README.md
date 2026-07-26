# Flask Image Dehazing Web App

A simple web application for single image dehazing using a trained deep learning model in Flask.

## Setup

1. Install requirements:

2. (Optional) Train your own model:
- Place paired images in `data/raw` (hazy) and `data/clean` (clean)
- Run: `python model/train.py`

3. Run the web app:

4. Open `http://127.0.0.1:5000` in your browser.

## Folder Structure

- `app.py`: Flask backend.
- `dehaze/`: Dehazing and model utility code.
- `model/`: Model training and weights.
- `static/uploads/`: Uploaded and dehazed images.
- `templates/`: HTML pages.
- `static/css/`: Styles.

## Notes

- Default model is a simple U-Net. For better results, train with large high-quality data.
- Clean up `static/uploads/` regularly to save space.
