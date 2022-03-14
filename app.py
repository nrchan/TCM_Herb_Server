import io
import os
from flask import Flask, request, abort
import json                    
import base64
import logging             
import numpy as np
from PIL import Image

app = Flask(__name__)

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
    img.show()

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    print('img shape', img_arr.shape)

    # process your img_arr here
    
    # access other keys of json
    # print(request.json['other_key'])

    result_dict = {'output': 'output_key'}
    return result_dict

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)