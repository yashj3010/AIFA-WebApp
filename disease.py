import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing import image

# ------- LOAD irrigationModel -------

model =tf.keras.models.load_model(r'Tensorflow Models\\DiseaseIdentification.h5',compile=False)

def model_predict(img_path):
    img = image.load_img(img_path, grayscale=False, target_size=(224, 224))
    show_img = image.load_img(img_path, grayscale=False, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds

def diagnose(file_path):
    preds = model_predict(file_path)

    disease_class = ['Potato___Early_blight',
                            'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                            'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                            'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                            'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
    a = preds[0]
    ind=np.argmax(a)
    print('Prediction:', disease_class[ind])
    result=disease_class[ind]
    return result
