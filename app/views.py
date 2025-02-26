import os
import cv2
from app.facerecognition import faceRecognitionPipeline
from flask import render_template,request
import matplotlib.image as mating

UPLOAD_FOLDER='static/upload'
def index():
    return render_template('index.html')

def app():
    return render_template('app.html')

def genderapp():
    if request.method == 'POST':
        f=request.files['image_name']
        filename=f.filename
        #save image in upload folder
        path=os.path.join(UPLOAD_FOLDER,filename)
        f.save(path)

        #get predictions
        pred_image, predictions=faceRecognitionPipeline(path)
        pred_filename='predicted_image.jpg'
        cv2.imwrite(f'./static/predict/{pred_filename}',pred_image)
        print('ML model predicted succesfully')
        # print(predictions)

        #generate report
        report=[]
        for i,obj in enumerate(predictions):
            gray_image=obj['roi']  #grayscale image
            eigen_image= obj['eig_img'].reshape(100,100)  #eigen image
            gender_name= obj['prediction_name']  #male or female
            score=round( obj['score']*100,2 ) #probability score

            #save frayscale and eigen images in predict folder
            gray_image_name=f'roi_{i}.jpg'
            eigen_image_name=f'eigen_{i}.jpg'
            mating.imsave(f'./static/predict/{gray_image_name}',gray_image,cmap='gray')
            mating.imsave(f'./static/predict/{eigen_image_name}',eigen_image,cmap='gray')

            #save report
            report.append([gray_image_name,eigen_image_name,gender_name,score])

        return render_template('gender.html',fileupload=True,report=report)



    return render_template('gender.html',fileupload=False)