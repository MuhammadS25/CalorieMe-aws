import numpy as np
from tensorflow import keras
import tensorflow as tf
import numpy as np
import requests

class FoodModel:
    def __init__(self ,modelpath , imgpath):
        self.modelpath = modelpath
        self.imgpath = imgpath
        self.imgSize = (256,256)

    def loadmodel(self):
        model = keras.models.load_model(self.modelpath)
        return model

    def read_image(self,image_url):
    
        #image = tf.io.read_file(image_path)
        # load img from internet
        response = requests.get(image_url)
        image = response.content
        image = tf.image.decode_png(image, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)
        image = tf.image.resize(image, self.imgSize, method='nearest')

        return image

   
    def create_mask(self, pred_mask):
        pred_mask = tf.argmax(pred_mask, axis=-1)
        pred_mask = pred_mask[..., tf.newaxis]
        return pred_mask[0]
    
    
    def get_mask(self, image, model):
            pred_mask = self.create_mask(model.predict(image))
            return pred_mask.numpy().astype("uint8").squeeze(axis=2)

    def data_generator(self,image_paths, mask_paths, buffer_size, batch_size):

        image_list = tf.constant(image_paths) 
        mask_list = tf.constant(mask_paths)
        dataset = tf.data.Dataset.from_tensor_slices((image_list, mask_list))
        dataset = dataset.map(self.read_image, num_parallel_calls=tf.data.AUTOTUNE)
        dataset = dataset.cache().shuffle(buffer_size).batch(batch_size)
        
        return dataset
    
    def getSizeOfMask(self, mask, num):
        white_pixels = np.count_nonzero(mask == num)
        return white_pixels



if __name__ == "__main__":
    modelpath = '/mnt/00F26D4EF26D494C/college/gp/Calories-Estimator/Test Script/Food_Model/cp2.h5'
    imgpath = '/mnt/00F26D4EF26D494C/college/gp/GourmetNet/UECFOODPIXCOMPLETE/UECFOODPIXCOMPLETE/data/UECFoodPIXCOMPLETE/train/'
    foodmodel = FoodModel(modelpath, imgpath)
    model = foodmodel.loadmodel()
    image_paths = [imgpath+'img/5.jpg']
    mask_paths = [imgpath+'mask/5.png']
    image = foodmodel.read_image(image_paths[0])
    image = tf.expand_dims(image, 0)
    mask = foodmodel.get_mask(image, model)

    cat_values = np.unique(mask)
    print(cat_values)
    for cat in cat_values:
        white_pixels = foodmodel.getSizeOfMask(mask, cat)

        if cat == 0: 
            continue

        print("Number of white pixels in category {}: {}".format(cat, white_pixels))