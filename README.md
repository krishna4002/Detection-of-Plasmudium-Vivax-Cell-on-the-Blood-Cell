
# Object Detection App

This project is a **Streamlit-based web application** for detecting infected (parasitized) cells in microscope images. It supports both **image upload** and **real-time camera capture** for processing.


## Features

-  Upload images or 📷 capture from your camera
-  Detect infected cells using contour-based analysis
-  Marks detected infected cells with numbered circles
-  Displays infection classification: `Parasitized` or `Uninfected`
-  Download annotated results


## Live Demo

👉 **Try the app here:** [Infected Cell Detection on Streamlit](https://detection-of-plasmudium-vivax-cell-on-the-blood-cell-arocvi7kp.streamlit.app/)


## 🛠 Requirements

Install Python dependencies:

```bash
pip install -r requirements.txt
```


## How to Run

1. Clone this repository or download the files.
2. Install dependencies.
3. Run the app with Streamlit:

```bash
streamlit run App.py
```

## File Structure

```
├── App.py                 # Main Streamlit app
├── image_processing.ipynb# (Optional) Notebook for image analysis development
├── requirements.txt       # Python packages
├── packages.txt           # System-level dependencies
├── test_result.png        # Example output image
└── output/                # Folder for saving processed images
```

## Detection Logic

- Image is resized to 224x224 pixels
- Converted to grayscale and thresholded to highlight dark areas
- Contours are extracted and filtered based on radius
- Valid contours are marked and numbered
- Classification:
  - **Parasitized**: One or more infected cells detected
  - **Uninfected**: No infected cells detected

## Camera Mode

- Starts webcam using OpenCV
- Captures frame on user command
- Applies the same detection logic

## Notes

- Works best with clear microscopic images.
- All processed images are saved to the `output/` folder.
