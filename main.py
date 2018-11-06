#!/usr/bin/python

from lib.data_logger import DataLogger
from lib.video_capture import VideoCapture
from lib.detection_model import DetectionModel
from lib.vehicle_detector import VehicleDetector

class Main:
  def __init__(self):
    print('Starting app')
    self.data_logger = DataLogger()
    self.video_capture = VideoCapture('sub-1504614469486.mp4')
    self.detection_model = DetectionModel()
    self.vehicle_detector = VehicleDetector(
      self.video_capture,
      self.detection_model,
      self.data_logger
    )

    # Local config
    self.total_passed_vehicle = 0


main = Main()
