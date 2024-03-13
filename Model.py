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

def CAPTURE_VIDEO (pathImageCeleb, app, swapper):
    # Establish capture
    cap = cv2.VideoCapture(0)

    # Frame size
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Store Video
    #out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width,frame_height))

    # Loop through each frame
    while True:
        # Read frame 
        ret, frame = cap.read()
        # Show image
        imgCeleb = cv2.imread(pathImageCeleb)
        if imgCeleb is None or frame is None:
            break
        imgPerson = frame
        imgPerson_ = SWAP_FACE (imgCeleb, imgPerson, app, swapper)
        frame = cv2.flip(imgPerson_, 1)
        cv2.imshow('Video Player', frame)
        #out.write(frame)
        # Breaking out of the loop
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Close down everything
    cap.release()
    #out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pathImageCeleb='data/Son_Tung.png'

    # Load Model And Process 
    app = FaceAnalysis(name = 'buffalo_l')
    app.prepare(ctx_id = 0, det_size=(640, 640))
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download = False, download_zip = False)
    CAPTURE_VIDEO (pathImageCeleb, app, swapper)
