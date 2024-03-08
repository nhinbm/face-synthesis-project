import streamlit as st
from PIL import Image
from io import BytesIO

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


# Download the fixed image
def convert_image(image):
    buf = BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im


# Web application
st.sidebar.write("## Upload and download :gear:")
input_image = st.sidebar.file_uploader("**Upload an image**", type=["png", "jpg", "jpeg"])

st.write("## Thay đổi gương mặt theo người nổi tiếng mà mình mong muốn")
st.write("**Bạn hãy thử chọn một tấm ảnh để xem bạn có hợp với người nổi tiếng đó không nhé! :grin:**")

option = st.selectbox(
    'Chọn nhân vật bạn muốn thay thế:',
    ('Chris Evans', 'Chris Hemsworth', 'Robert Downey', 'Tom Holland', 'Scarlett Johansson'))

st.write('Lựa chọn của bạn:', option)

col1, col2, col3 = st.columns(3)

character = option.lower().replace(" ", "")

with col1:
    st.write("**Nhân vật:**")
    st.image(f"characters/{character}.png")

if input_image is not None:
    if input_image.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        with col2:
            st.write("**Hình bạn chọn:**")
            image = Image.open(input_image)
            col2.image(image)

        with col3:
            st.write("**Kết quả:**")
            st.image("https://static.streamlit.io/examples/owl.jpg")

        st.sidebar.download_button("Lưu bức ảnh chỉnh sửa:", convert_image(image), "fixed.png", "image/png")
