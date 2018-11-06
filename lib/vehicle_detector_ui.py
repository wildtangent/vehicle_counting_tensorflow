import cv2

class VehicleDetectorUI:
  def __init__(self, width, height):
    self.width = width
    self.height = height


    self.font1 = cv2.FONT_HERSHEY_SIMPLEX
    self.font2 = cv2.FONT_HERSHEY_COMPLEX_SMALL
    self.colors = {
      'white': (0xFF, 0xFF, 0xFF),
      'red': (0, 0, 0xFF),
      'green': (0, 0xFF, 0),
      'yellow': (0, 0xFF, 0xFF)
    }

    self.text = {
      'roi_line': 'ROI Line',
      'vehicles_count': 'Detected Vehicles: ',
      'last_vehicle': 'LAST PASSED VEHICLE INFO: ',
      'direction': '- Movement direction: ',
      'speed': '- Speed: ',
      'type': '-Vehicle Size/Type: '
    }


  # When the vehicle passed over line and counted, make the color of ROI line green
  def draw_roi_line(self, frame, start, end, counter = 0):
    color = self.colors['red']
    width = 5

    if counter == 1:
      color = self.colors['green']

    cv2.line(frame, start, end, color, width)

    label_position = (int((end[0] - start[0]) / 2), int(start[1] + 20))
    self.write_roi_line_text(frame, label_position)


  def draw_info_box(self, frame):
    cv2.rectangle(frame, (10, 275), (230, 337), (180, 132, 109), -1)

  def write_roi_line_text(self, frame, position):
    cv2.putText(
      frame,
      'ROI Line',
      position,
      self.font1,
      0.6,
      (0, 0, 0xFF),
      2,
      cv2.LINE_AA,
    )

  def write_vehicle_count_text(self, frame, count = 0):
    cv2.putText(
      frame,
      'Detected Vehicles: ' + str(count),
      (10, 35),
      self.font1,
      0.8,
      (0, 0xFF, 0xFF),
      2,
      cv2.FONT_HERSHEY_SIMPLEX,
    )

  def write_last_vehicle_info_text(self, frame):
    cv2.putText(
      frame,
      'LAST PASSED VEHICLE INFO',
      (11, 290),
      self.font1,
      0.5,
      (0xFF, 0xFF, 0xFF),
      1,
      self.font1,
    )

  def write_movement_direction_text(self, frame, direction):
    cv2.putText(
      frame,
      '-Movement Direction: ' + direction,
      (14, 302),
      self.font1,
      0.4,
      (0xFF, 0xFF, 0xFF),
      1,
      self.font2,
    )

  def write_speed_text(self, frame, speed):
    cv2.putText(
      frame,
      '-Speed(km/h): ' + speed,
      (14, 312),
      self.font1,
      0.4,
      (0xFF, 0xFF, 0xFF),
      1,
      self.font2,
    )

  def write_color_text(self, frame, color):
    cv2.putText(
      frame,
      '-Color: ' + color,
      (14, 322),
      self.font1,
      0.4,
      (0xFF, 0xFF, 0xFF),
      1,
      self.font2,
    )

  def write_size_text(self, frame, size):
    cv2.putText(
      frame,
      '-Vehicle Size/Type: ' + size,
      (14, 332),
      self.font1,
      0.4,
      (0xFF, 0xFF, 0xFF),
      1,
      self.font2,
    )

