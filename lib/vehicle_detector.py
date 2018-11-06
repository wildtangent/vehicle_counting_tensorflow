import cv2
import tensorflow

from utils import visualization_utils as vis_util
from lib.vehicle_detector_ui import VehicleDetectorUI

class VehicleDetector:
  def __init__(self, video, model, logger):
    self.video = video
    self.model = model
    self.logger = logger

    # Setup UI
    self.ui = VehicleDetectorUI(
      self.video.width,
      self.video.height
    )

    self.total_vehicles = 0 # todo: move into parent

    self.cv_window = 'vehicle detection'
    self.frame_filename = 'webcam.jpg'

    self.speed = 'Waiting...'
    self.direction = 'Waiting...'
    self.size = 'Waiting...'
    self.color = 'Waiting...'

    self.init_roi_line()
    self.detect()


  # ROI line setup (move somewhere else?)
  def init_roi_line(self):
    # vis_util.ROI_POSITION = int(self.video.height / 2)
    vis_util.ROI_POSITION = 200
    # print("ROI Line: %sx%s" % self.ui.roi_line)


  # Detection loop
  def detect(self):
    detection_graph = self.model.detection_graph

    with detection_graph.as_default():
      with tensorflow.Session(graph=detection_graph) as session:
        while self.video.capture.isOpened():
          (ret, frame) = self.video.capture.read()

          if self.handle_eof(ret):
            break

          (total, data) = self.handle_video(frame, session)

          self.total_vehicles = total

          self.handle_data(data)

          if self.handle_exit():
            break

        self.clean_up()


  def handle_video(self, frame, session):
    # Handle detection
    (counter, data) = self.model.detect(
      self.video.capture,
      frame,
      session
    )

    # Increment total
    total = self.total_vehicles + counter

    # UI Layout
    self.handle_ui(frame, total, counter)

    # Display and write the video frame
    self.display_video(frame)
    self.write_frame(frame)

    return (total, data)


  def handle_ui(self, frame, total, counter):
    # Vehicle info
    self.ui.write_vehicle_count_text(frame, total)

    # ROI line
    # start = (0, vis_util.ROI_POSITION)
    # end = (self.video.width, vis_util.ROI_POSITION)
    start = (0, 200)
    end = (640, 200)

    self.ui.draw_roi_line(frame, start, end, counter)

    # insert information text to video frame
    self.ui.draw_info_box(frame)
    self.ui.write_last_vehicle_info_text(frame)
    self.ui.write_movement_direction_text(frame, self.direction)
    self.ui.write_speed_text(frame, self.speed)
    self.ui.write_color_text(frame, self.color)
    self.ui.write_size_text(frame, self.size)


  def display_video(self, frame):
    cv2.imshow(self.cv_window, frame)


  def write_frame(self, frame):
    cv2.imwrite(self.frame_filename, frame)


  def handle_exit(self):
    return cv2.waitKey(1) & 0xFF == ord('q')


  def handle_eof(self, ret):
    if not ret:
      print('End of the video file...')
    return not ret


  def clean_up(self):
    self.video.capture.release()
    cv2.destroyAllWindows()


  def handle_data(self, data):
    if data != 'not_available':
      (self.size, self.color, self.direction, self.speed) = data.split(',')
      self.logger.log([self.size, self.color, self.direction, self.speed])
