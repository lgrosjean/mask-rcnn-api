import os
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
from .utils import download_trained_weights
from .model  import MaskRCNN
from . import visualize
from .config import Config

class CocoConfig(Config):
    """Configuration for training on MS COCO.
    Derives from the base Config class and overrides values specific
    to the COCO dataset.
    """
    # Give the configuration a recognizable name
    NAME = "coco"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Uncomment to train on 8 GPUs (default is 1)
    # GPU_COUNT = 8

    # Number of classes (including background)
    NUM_CLASSES = 1 + 80  # COCO has 80 classes


class InferenceConfig(CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

# config = InferenceConfig()
# config.display()


# Root directory of the project
# ROOT_DIR = os.path.abspath("./")


#import coco

# Directory to save logs and trained model
# MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# # Local path to trained weights file
# COCO_MODEL_PATH = os.path.join("mask_rcnn_coco.h5")
# # Download COCO trained weights from Releases if needed
# if not os.path.exists(COCO_MODEL_PATH):
#     download_trained_weights(COCO_MODEL_PATH)

# print("Weights load ok")


# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')



class Mask():

  config = InferenceConfig()
  ROOT_DIR = os.path.abspath("./")
  MODEL_DIR = os.path.join(ROOT_DIR, "logs")

  class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

  COCO_MODEL_PATH = os.path.join("mask_rcnn_coco.h5")
  # Download COCO trained weights from Releases if needed
  if not os.path.exists(COCO_MODEL_PATH):
    download_trained_weights(COCO_MODEL_PATH)

  def __init__(self):

    self.model = MaskRCNN(mode="inference", model_dir=self.MODEL_DIR, config=self.config)
    self.model.load_weights(self.COCO_MODEL_PATH, by_name=True)

# def fit_mask_rcnn():
#   model_rcnn = MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
#   model_rcnn.load_weights(COCO_MODEL_PATH, by_name=True)
#   return model_rcnn

  def mask_detection(self, image,verbose=1):
    assert verbose in [0, 1]
  # model_rcnn = MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)
  # model_rcnn.load_weights(COCO_MODEL_PATH, by_name=True)
    results = self.model.detect([image], verbose=0)
    r = results[0]

    if verbose==1:
      for (class_id, score) in zip(r['class_ids'], r['scores']):
        print(self.class_names[class_id], ", score : ", score)

    return visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                            self.class_names, r['scores'])