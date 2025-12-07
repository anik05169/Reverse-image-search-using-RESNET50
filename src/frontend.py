import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="Reverse Image Search",
    layout="wide",
)

st.title("🔍 Reverse Image Search Engine")
st.write("Upload an image and find visually similar images from the Caltech-101 dataset.")

uploaded_file = st.file_uploader(
    "Choose an image", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")  
    st.image(img, caption="Your Query Image", use_column_width=True)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)


    with st.spinner("Searching for similar images..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/search",
                files={"file": ("query.jpg", img_bytes, "image/jpeg")},
                timeout=30
            )
            data = response.json()
        except Exception as e:
            st.error(f"Error contacting backend: {e}")
            st.stop()

    results = data.get("results", [])

    if len(results) == 0:
        st.warning("No similar images found in database.")
    else:
        st.subheader("📸 Top Matches")

        cols = st.columns(3)

        for i, item in enumerate(results):
            filename = item["filename"]
            category = item["category"]
            distance = item["distance"]

           
            img_path = f"data/raw/256_ObjectCategories/{category}/{filename}"

            try:
                result_img = Image.open(img_path)
                with cols[i % 3]:
                    st.image(
                        result_img, 
                        caption=f"{category}\nDist: {distance:.4f}",
                        use_column_width=True
                    )
            except Exception as e:
                st.error(f"Could not load image: {img_path}")
