from imageai.Detection import ObjectDetection
from os.path import isfile, join
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
input_img= "person.jpg"



def imganalyze(pathtoimages):
    path = f'{execution_path}/imagebank/'
    onlyimgs = [f for f in os.listdir(path) if isfile(join(path, f))]
    for image in onlyimgs:

        detections = detector.detectObjectsFromImage(input_image=os.path.join(path, image), output_image_path=os.path.join(path , f'analyzed_photos/Analysed{image}'))

        for eachObject in detections:
            print(image, eachObject["name"] , " : " , eachObject["percentage_probability"] )

imganalyze(execution_path)