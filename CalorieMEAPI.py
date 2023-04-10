from flask import Flask, request, jsonify
import Test, CaloriesEstimation,os
from ID_segmentation import getIdCard
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'CalorieMe API'


@app.route('/CalorieMe-V1', methods=['GET','POST'])
def predict():
    try:
        if request.method == 'POST':
            img_link = request.form['img_link']
            ref_pixels = request.form['ref_pixels']

            print(img_link, ref_pixels)

            label = Test.getFoodWeight(img_link, ref_pixels)
            json = CaloriesEstimation.getCalories(label)
            return jsonify(json)
    
    except Exception as e:
        return jsonify({'msg': 'error', 'error': str(e)})
    
@app.route('/CalorieMe-V2', methods=['GET','POST'])
def predictV2():
    try:
        if request.method == 'POST':
            img_link = request.form['img_link']
            print(img_link)
            # download image from link
            if os.path.exists('Food_Model/img.jpg'):
                os.system('rm Food_Model/img.jpg')
                os.system('wget -O Food_Model/img.jpg {}'.format(img_link))
                print("Image Downloaded")
            else:
                os.system('wget -O Food_Model/img.jpg {}'.format(img_link))
                print("Image Downloaded")

            try:
                ref_pixels = getIdCard('Food_Model/img.jpg')
            except:
                return jsonify({'msg': 'error', 'error': 'Reference object not found'})


            label = Test.getFoodWeightV2(img_link, 0.25, ref_pixels)
            if label == None:
                label = Test.getFoodWeightV2(img_link, 0.05, ref_pixels)
                
            json = CaloriesEstimation.getCalories(label)
            return jsonify(json)
    
    except Exception as e:
        return jsonify({'msg': 'error', 'error': str(e)})


@app.route('/refresh', methods=['GET'])
def refresh():
    try:
        if request.method == 'GET':
            os.system('sudo reboot')
            return jsonify({'msg': 'success'})
    except Exception as e:
        return jsonify({'msg': 'error', 'error': str(e)})
    

if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run(host='0.0.0.0', port=5000, debug=True)
