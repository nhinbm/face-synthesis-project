import streamlit as st
from Model import IMAGE_AND_IMAGE, IMAGE_AND_VIDEO, SWAP_FACE
import os
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import subprocess
import cv2
import av

# Constants
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def title():
    # Title
    st.write("## Thay đổi gương mặt theo người nổi tiếng")
    st.write("""
    <style>
        .justified {
            text-align: justify;
        }
    </style>
    <div class="justified">
        Chào mừng bạn đến với chức năng độc đáo của chúng tôi - thay đổi gương mặt theo người nổi tiếng! Với công nghệ AI 
        tiên tiến, chúng tôi đã phát triển một công cụ mạnh mẽ cho phép bạn chuyển đổi gương mặt của mình thành các nhân vật 
        nổi tiếng trên thế giới. Từ những ngôi sao điện ảnh, ca sĩ, người nổi tiếng trên mạng xã hội đến các nhân vật lịch sử, 
        bạn có thể trải nghiệm sự thú vị khi trở thành hình ảnh của những người được ngưỡng mộ. Với tính linh hoạt và dễ sử dụng, 
        bạn có thể tạo ra những bức ảnh, video thú vị một cách nhanh chóng và dễ dàng. Hãy khám phá và khẳng định phong cách 
        của riêng bạn trong thế giới ảo đầy sáng tạo của chúng tôi!
    <div>
    """, unsafe_allow_html=True)


def choose_option():
    # Option of function
    option = st.selectbox(
        '',
        ('Chức năng 1: Thay đổi ảnh của bạn theo ảnh của người nổi tiếng.',
         'Chức năng 2: Thay đổi video của bạn theo ảnh của người nổi tiếng.',
         'Chức năng 3: Thay đổi video real time của bạn theo ảnh của người nổi tiếng.'),
        index=None,
        placeholder="Lựa chọn chức năng...",
    )
    return option


def function_one():
    col1, col2, col3 = st.columns(3)

    with col1:
        famous_image = st.file_uploader("**Chọn ảnh người nổi tiếng:**", type=["png", "jpg", "jpeg", "webp"],
                                        key="famous")
        if famous_image is not None:
            with open(os.path.join("cache", "famous_image.jpeg"), "wb") as f:
                f.write(famous_image.getbuffer())
            st.image(famous_image)

    with col2:
        personal_image = st.file_uploader("**Chọn ảnh của bạn:**", type=["png", "jpg", "jpeg", "webp"], key="personal")
        if personal_image is not None:
            with open(os.path.join("cache", "person_image.jpeg"), "wb") as f:
                f.write(personal_image.getbuffer())
            st.image(personal_image)

    with col3:
        if famous_image is not None and personal_image is not None:
            st.write("**Kết quả:**")
            swap_image = IMAGE_AND_IMAGE("cache/famous_image.jpeg", "cache/person_image.jpeg")
            if swap_image is not None:
                st.image("cache/output_image.png")


def function_two():
    col1, col2, col3 = st.columns(3)

    if not os.path.exists("cache"):
        os.makedirs("cache")

    with col1:
        famous_image = st.file_uploader("**Chọn ảnh người nổi tiếng:**", type=["png", "jpg", "jpeg", "webp"],
                                        key="famous")
        if famous_image is not None:
            with open(os.path.join("cache", "famous_image.jpeg"), "wb") as f:
                f.write(famous_image.getbuffer())
            st.image(famous_image)

    with col2:
        personal_image = st.file_uploader("**Chọn ảnh của bạn:**", type=["webm", "avi", "mov", "mp4"], key="personal")
        if personal_image is not None:
            with open(os.path.join("cache", "person_video.mp4"), "wb") as f:
                f.write(personal_image.getbuffer())
            st.video(personal_image)

    with col3:
        if famous_image is not None and personal_image is not None:
            st.write("**Kết quả:**")
            swap_video = IMAGE_AND_VIDEO("cache/famous_image.jpeg", "cache/person_video.mp4")
            if swap_video is not None:
                command = ['ffmpeg', '-i', "cache/output_video.mp4", '-c:v', 'libx264', '-c:a', 'copy', "cache/output_video_st.mp4"]
                subprocess.run(command)
                st.video("cache/output_video_st.mp4")


def function_three():
    col1, col2, col3 = st.columns(3)

    if not os.path.exists("cache"):
        os.makedirs("cache")

    with col1:
        famous_image = st.file_uploader("**Chọn ảnh người nổi tiếng:**", type=["png", "jpg", "jpeg", "webp"],
                                        key="famous")

    with col2:
        if famous_image is not None:
            with open(os.path.join("cache", "famous_image.jpeg"), "wb") as f:
                f.write(famous_image.getbuffer())
            st.image(famous_image)
    if famous_image is not None:
        def CAPTURE_CAMERA_TEST(frame: av.VideoFrame):
            imgCeleb = cv2.imread("cache/famous_image.jpeg")
            print("------------------------ HELLO")
            img = frame.to_ndarray(format="bgr24")
            img = SWAP_FACE(imgCeleb, img)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        webrtc_streamer(key="example",
                        video_frame_callback=CAPTURE_CAMERA_TEST)



if __name__ == "__main__":
    title()
    option = choose_option()
    if option is not None:
        if "Chức năng 1" in option:
            function_one()
        elif "Chức năng 2" in option:
            function_two()
        elif "Chức năng 3" in option:
            function_three()
