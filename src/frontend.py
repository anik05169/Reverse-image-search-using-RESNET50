import streamlit as st
import requests
from PIL import Image
import io
import os

# ---------------------------------------------
# CONFIG
# ---------------------------------------------
BACKEND_URL = "http://127.0.0.1:8000/search"  # Change when deploying
DATA_PATH = "data/raw/256_ObjectCategories"   # Local image folder

st.set_page_config(
    page_title="Reverse Image Search",
    layout="wide",
)

# ---------------------------------------------
# HEADER
# ---------------------------------------------
st.markdown(
    """
    <h1 style="text-align:center;">🔍 Reverse Image Search</h1>
    <p style="text-align:center; font-size:18px;">
        Upload an image and find visually similar images from the Caltech-101 dataset.
    </p>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------
# FILE UPLOADER
# ---------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a query image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:

    # Display uploaded image
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Your Query Image", use_container_width=True)

    # Convert image to bytes for API
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)


    with st.spinner("⏳ Searching for similar images..."):
        try:
            response = requests.post(
                BACKEND_URL,
                files={"file": ("query.jpg", img_bytes, "image/jpeg")},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection failed:\n\n{e}")
            st.stop()

    results = data.get("results", [])

    # -----------------------------------------
    # DISPLAY RESULTS
    # -----------------------------------------
    if len(results) == 0:
        st.warning("No similar images found in database.")
    else:
        st.subheader("📸 Top Similar Images")

        # Display images in a grid of 3 columns
        cols = st.columns(3)

        for idx, item in enumerate(results):

            filename = item["filename"]
            category = item["category"]
            distance = item["distance"]

            img_path = os.path.join(DATA_PATH, category, filename)

            with cols[idx % 3]:
                try:
                    result_img = Image.open(img_path)
                    st.image(
                        result_img,
                        caption=f"{category} (Dist: {distance:.4f})",
                        use_container_width=True,
                        
                    )
                except Exception:
                    st.error(f"Missing image: {img_path}")

else:
    st.info("👆 Upload an image to begin searching!")

