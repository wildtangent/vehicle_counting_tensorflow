import csv

class DataLogger:

  csv_line = 'Vehicle Type/Size, Vehicle Color, Vehicle Movement Direction, Vehicle Speed (km/h)'

  def __init__(self, file='traffic_measurement.csv'):
    self.file = file
    self.init_csv()


  def init_csv(self):
    with open(self.file, 'w') as f:
      self.writer = csv.writer(f)
      self.writer.writerows([self.csv_line.split(',')])


  def log(self, data):
    print(data)
    with open(self.file, 'a') as f:
      writer = csv.writer(f)
      writer.writerow(data)
