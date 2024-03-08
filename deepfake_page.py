import streamlit as st
from io import BytesIO
from PIL import Image

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


# Download the fixed image
# def convert_image(image):
#     buf = BytesIO()
#     image.save(buf, format="PNG")
#     byte_im = buf.getvalue()
#     return byte_im


# Push image
# def fix_image(upload):
#     image = Image.open(upload)
#     col1.write("Original Image :camera:")
#     col1.image(image)
#
#     fixed = remove(image)
#     col2.write("Fixed Image :wrench:")
#     col2.image(fixed)
#     st.sidebar.markdown("\n")
#     st.sidebar.download_button("Download fixed image", convert_image(fixed), "fixed.png", "image/png")


# Web application
st.sidebar.write("## Upload and download :gear:")
input_image = st.sidebar.file_uploader("**Upload an image**", type=["png", "jpg", "jpeg"])

st.write("## Thay đổi gương mặt theo người nổi tiếng mà mình mong muốn")
st.write(":dog: Bạn hãy thử chọn một tấm ảnh để xem bạn có hợp với người nổi tiếng đó không nhé! :grin:")

# if input_image is not None:
#     if input_image.size > MAX_FILE_SIZE:
#         st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
#     else:
#         fix_image(upload=input_image)
# else:
#     pass
