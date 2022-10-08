from keras.models import load_model
from Preprocessing import ImgPreprocessing 
import numpy as np
import cv2





def load_prediction_model():
    model_cnn = load_model('./Inference/WilhemNet_86.h5')
    model_cnn.make_predict_function()
    return model_cnn
###------------------------------------------------------------------------------------------------------------
### 
## Predecir si la imagen corresponde a bacterial, virus, normal
###------------------------------------------------------------------------------------------------------------

def predict_label(img_path):
    #   1. call function to pre-process image: it returns image in batch format
    batch_array_img = ImgPreprocessing.preprocess(img_path)
    #   2. call function to load model and predict: it returns predicted class and probability      
    model = load_prediction_model()    
    # model_cnn = tf.keras.models.load_model('conv_MLP_84.h5')
    prediction = np.argmax(model.predict(batch_array_img))
    proba = round(np.max(model.predict(batch_array_img)) * 100, 2)
    label = ""
    if prediction == 0:
        label = "bacteriana"
    if prediction == 1:
        label = "normal"
    if prediction == 2:
        label = "viral"
    #   3. call function to generate Grad-CAM: it returns an image with a superimposed heatmap
  

    return label 
    
