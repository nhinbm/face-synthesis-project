# Import library
import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

# Swapping Method
def SWAP_FACE (imgCeleb, imgPerson, app, swapper):
    faceCeleb = app.get(imgCeleb)[0]
    facePerson = app.get(imgPerson)[0]
    imgPerson_ = imgPerson.copy()
    imgPerson_ = swapper.get(imgPerson_, facePerson, faceCeleb, paste_back = True)
    return imgPerson_

def IMAGE_AND_VIDEO (pathImageCeleb, pathVideo, app, swapper):
    # Establish capture
    cap = cv2.VideoCapture(pathVideo)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    # Total of frame in video
    lengthFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Frame size
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Store Video
    out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frameWidth,frameHeight))

    # Loop through each frame
    countFrame = 0.0
    while cap.isOpened():
        # Read frame 
        ret, frame = cap.read()
        # Show image
        imgCeleb = cv2.imread(pathImageCeleb)
        if imgCeleb is None or not ret:
            break
        imgPerson = frame
        imgPerson_ = SWAP_FACE (imgCeleb, imgPerson, app, swapper)
        frame = cv2.flip(imgPerson_, 1)
        out.write(frame)
        countFrame += 1
        print(f"Phan tram da xu ly: {round(countFrame / lengthFrame * 100)}%")

    # Close down everything
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def CAPTURE_CAMERA (pathImageCeleb, app, swapper):
    # Establish capture
    cap = cv2.VideoCapture(0)

    # Loop through each frame
    while True:
        # Read frame 
        ret, frame = cap.read()
        # Show image
        imgCeleb = cv2.imread(pathImageCeleb)
        if imgCeleb is None or not ret:
            break
        imgPerson = frame
        imgPerson_ = SWAP_FACE (imgCeleb, imgPerson, app, swapper)
        frame = cv2.flip(imgPerson_, 1)
        cv2.imshow('Video Player', frame)

        # Breaking out of the loop
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Close down everything
    cap.release()
    #out.release()
    cv2.destroyAllWindows()

def IMAGE_AND_IMAGE (pathImageCeleb, pathImagePerson, app, swapper):
        
    imgCeleb = cv2.imread(pathImageCeleb)
    imgPerson = cv2.imread(pathImagePerson)
    if imgCeleb is None or imgPerson is None:
        return
    imgPerson_ = SWAP_FACE (imgCeleb, imgPerson, app, swapper)
        
    cv2.imwrite('output_image.png', imgPerson_)

if __name__ == "__main__":

    # Load Model And Process 
    app = FaceAnalysis(name = 'buffalo_l')
    app.prepare(ctx_id = 0, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download = False, download_zip = False)
    # Select function
    choose = int(input("Chon chuc nang: "))
    if choose == 1:
        pathImageCeleb='data/Son_Tung.png'
        pathImagePerson='data/Person.jpg'
        IMAGE_AND_IMAGE (pathImageCeleb, pathImagePerson, app, swapper)
    elif choose == 2:
        pathImageCeleb='data/Son_Tung.png'
        pathVideo='data/input_video.mp4'
        IMAGE_AND_VIDEO (pathImageCeleb, pathVideo, app, swapper)
    else:
        pathImageCeleb='data/Son_Tung.png'
        CAPTURE_CAMERA (pathImageCeleb, app, swapper)

