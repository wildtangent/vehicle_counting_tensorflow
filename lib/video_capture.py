import cv2

class VideoCapture:
  def __init__(self, source=0):
    self.capture = cv2.VideoCapture(source)
    self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Video size: %sx%s" % (self.width, self.height))
