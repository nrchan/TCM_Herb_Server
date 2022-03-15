import base64
import json                    
import requests
import sys

if sys.argv[1] == "local":
    api = "http://localhost:8000" + sys.argv[2]
else:
    api = "https://herb-server-mj26pnawdq-uc.a.run.app/" + sys.argv[2]

if sys.argv[2] == "/":
    print(requests.get(api).text)
else:

    image_file = 'test_images/X1.jpg'

    with open(image_file, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    payload = json.dumps({"image": im_b64, "other_key": api})
    response = requests.post(api, data=payload, headers=headers)
    try:
        data = response.json()
        print("1st: X" + str(data["result index"][0]+1) + ", confidence = " + str(data["result confidence"][0]))
        print("2nd: X" + str(data["result index"][1]+1) + ", confidence = " + str(data["result confidence"][1]))
        print("3rd: X" + str(data["result index"][2]+1) + ", confidence = " + str(data["result confidence"][2]))
    except requests.exceptions.RequestException:
        print(response.text)