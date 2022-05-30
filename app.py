import io
import os
from flask import Flask, request, abort
import base64
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.layers import Resizing, Rescaling

app = Flask(__name__)
model = tf.keras.models.load_model("model_v19.h5",custom_objects={'KerasLayer':hub.KerasLayer})
#model = tf.keras.models.load_model("model-effnetb1.h5")

image_size = 256
resize_and_rescale = tf.keras.Sequential([
    Resizing(image_size, image_size),
    Rescaling(1./255)
])

@app.route("/")
def index():
    return "Hello World!"

@app.route("/test", methods=['POST'])
def test_method():   
    if not request.json or 'image' not in request.json: 
        abort(400)
             
    # get the base64 encoded string
    im_b64 = request.json['image']

    # convert it into bytes  
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))
    img = resize_and_rescale(img)

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    img_arr = img_arr.reshape((1,256,256,3))

    # process your img_arr here
    result_array = model.predict(img_arr)
    result_values, result_indices  = tf.math.top_k(result_array, k=3)
    result_indices = np.array(result_indices)[0].tolist()[0:3]
    result_values = np.array(result_values)[0].tolist()[0:3]

    result_dict = {"result index": result_indices, "result confidence": result_values}
    return result_dict

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)