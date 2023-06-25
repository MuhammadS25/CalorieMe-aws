from flask import Flask, request, jsonify
import Test, CaloriesEstimation,os
from ID_segmentation import getIdCard
import os 
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

            # download image
            os.system('wget -O Food_Model/img.jpg ' + img_link)

            label = Test.getFoodWeight(img_link, ref_pixels)
            json = CaloriesEstimation.getCalories(label)
            return jsonify(json)
    
    except Exception as e:
        return jsonify({'msg': 'error', 'error': str(e)})
    
@app.route('/CalorieMe-V2', methods=['GET','POST'])
def predictV2():
    try:

        if request.method == 'POST':
            img_bytes = request.files['img_bytes']

            img_bytes.save("Food_Model/img.jpg")

            return run()
            
    except Exception as e:
        return jsonify({'msg': 'error', 'error': str(e)})
         

def run():

    try:
        print("Getting ID Pixels")
        ref_pixels = getIdCard("Food_Model/img.jpg")
        print("ID Pixels",ref_pixels)
    except Exception as e:
        return jsonify({'msg': 'error', 'error': "Reference object not found"})

    label = Test.getFoodWeightV2(0.25, ref_pixels)
    if label == None:
        label = Test.getFoodWeightV2(0.05, ref_pixels)
        
    json = CaloriesEstimation.getCalories(label)
    return jsonify(json)
    

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
    app.run(host='0.0.0.0', port=5000, ssl_context=('/home/calorieME/certs/cert.pem', '/home/calorieME/certs/key.pem'), debug=True)
