import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image

# Create output folder if it doesn't exist
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

def process_image(image):
    test_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    test_img = cv2.resize(test_img, (224, 224))
    gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    count = 0
    sorted_contours = sorted(contours, key=lambda c: cv2.contourArea(c), reverse=True)

    for i, contour in enumerate(sorted_contours, start=1):
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        if radius > 5:
            count += 1
            cv2.circle(test_img, center, radius, (0, 255, 0), 2)
            cv2.putText(test_img, str(count), (center[0] - 10, center[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)

    label = "Parasitized" if count > 0 else "Uninfected"
    cv2.putText(test_img, f"Infected Cells: {count}", (5, 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    output_path = os.path.join(output_folder, "test_result.png")
    cv2.imwrite(output_path, test_img)

    return test_img, label, count, output_path

# Streamlit UI
st.set_page_config(layout="wide")
st.sidebar.title("🧪 Infected Cell Detection")
mode = st.sidebar.radio("Choose input type:", ["Upload Image", "Use Real-Time Camera"])

st.title("🦠 Infected Cell Detection App")

if mode == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Detect Infected Cells"):
            with st.spinner("Processing..."):
                result_img, label, count, path = process_image(image)
                result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                st.image(result_img_rgb, caption=f"{label} - Infected Cells: {count}", use_container_width=True)
                with open(path, "rb") as f:
                    st.download_button("Download Result", f, file_name="test_result.png")
                st.success(f"Detection Complete: {label} - {count} infected cells.")

elif mode == "Use Real-Time Camera":
    st.session_state.setdefault("camera_started", False)
    st.session_state.setdefault("captured_image", None)

    col1, col2 = st.columns(2)
    if col1.button("▶ Start Camera"):
        st.session_state.camera_started = True
        st.session_state.captured_image = None

    if col2.button("📸 Capture Image"):
        st.session_state.captured_image = "capture_now"

    if st.session_state.camera_started:
        stframe = st.empty()
        cap = cv2.VideoCapture(0)

        while st.session_state.camera_started:
            ret, frame = cap.read()
            if not ret:
                st.warning("Camera failed to open.")
                break

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, channels="RGB", use_container_width=True)

            if st.session_state.captured_image == "capture_now":
                image = Image.fromarray(frame_rgb)
                st.session_state.camera_started = False
                st.session_state.captured_image = image
                break

        cap.release()

    if isinstance(st.session_state.captured_image, Image.Image):
        st.image(st.session_state.captured_image, caption="Captured Frame", use_container_width=True)

        if st.button("Detect Infected Cells"):
            with st.spinner("Processing..."):
                result_img, label, count, path = process_image(st.session_state.captured_image)
                result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
                st.image(result_img_rgb, caption=f"{label} - Infected Cells: {count}", use_container_width=True)
                with open(path, "rb") as f:
                    st.download_button("Download Result", f, file_name="test_result.png")
                st.success(f"Detection Complete: {label} - {count} infected cells.")
