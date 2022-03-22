import io
import os
from flask import Flask, request, abort
import json                    
import base64
import logging             
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub

app = Flask(__name__)
model = tf.keras.models.load_model("model.h5",custom_objects={'KerasLayer':hub.KerasLayer})

@app.route("/")
def index():
    return "Hello World!"

@app.route("/test", methods=['POST'])
def test_method():         
    # print(request.json)      
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    im_b64 = request.json['image']

    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))
    img = img.resize((256,256))

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    img_arr = img_arr.reshape((1,256,256,3))

    # process your img_arr here
    result_array = model.predict(img_arr)
    result_values, result_indices  = tf.math.top_k(result_array, k=3)
    result_indices = np.array(result_indices)[0].tolist()
    result_values = np.array(result_values)[0].tolist()

    result_dict = {"result index": result_indices, "result confidence": result_values}
    return result_dict

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)