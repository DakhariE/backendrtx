#This file trains the model 
from ultralytics import YOLO
#This yaml file is config to where the train data is.
model = YOLO("yolov8n.yaml")
#This trains the actual model and puts it into a file called runs. epochs is the amount of iterations you want to model to train.
results = model.train(data="config.yaml", epochs=1000)