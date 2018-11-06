import os
import tensorflow
import numpy as np

from utils import label_map_util
from utils import visualization_utils as vis_util

class DetectionModel:
  def __init__(self, num_classes=90):
    # By default I use an "SSD with Mobilenet" model here. See the detection model zoo (https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.
    # What model to download.
    self.num_classes = num_classes

    self.model_name = 'ssd_mobilenet_v1_coco_2018_01_28'
    self.model_file = self.model_name + '.tar.gz'
    self.download_base = 'http://download.tensorflow.org/models/object_detection/'

    self.path_to_ckpt = self.model_name + '/frozen_inference_graph.pb'

    # List of the strings that is used to add correct label for each box.
    self.path_to_labels = os.path.join('data', 'mscoco_label_map.pbtxt')

    self.init_graph()
    self.init_labelmap()
    self.init_tensorflow()


  def init_graph(self):
    self.detection_graph = tensorflow.Graph()
    with self.detection_graph.as_default():
      od_graph_def = tensorflow.GraphDef()
      with tensorflow.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tensorflow.import_graph_def(od_graph_def, name='')


  def init_labelmap(self):
    self.label_map = label_map_util.load_labelmap(self.path_to_labels)
    self.categories = label_map_util.convert_label_map_to_categories(
        self.label_map,
        max_num_classes=self.num_classes,
        use_display_name=True
    )
    self.category_index = label_map_util.create_category_index(self.categories)


  def init_tensorflow(self):
    # Definite input and output Tensors for detection_graph
    self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
    self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
    self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


  def detect(self, capture, frame, session):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(frame, axis=0)

    # Actual detection.
    (boxes, scores, classes, num) = \
      session.run(
        [
            self.detection_boxes, self.detection_scores,
            self.detection_classes, self.num_detections
        ],
        feed_dict={
            self.image_tensor: image_np_expanded
        }
      )

    # Visualization of the results of a detection.
    return vis_util.visualize_boxes_and_labels_on_image_array(
      capture.get(1),
      frame,
      np.squeeze(boxes),
      np.squeeze(classes).astype(np.int32),
      np.squeeze(scores),
      self.category_index,
      use_normalized_coordinates=True,
      line_thickness=4,
    )
