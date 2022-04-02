import base64
import json                    
import requests
import sys
import datetime

indexToXIndex = (1,10,11,12,13,14,15,16,17,18,19,2,20,21,22,23,24,25,26,27,28,29,3,30,31,32,33,34,35,36,37,38,39,4,40,41,5,6,7,8,9)

start_time = datetime.datetime.now()

if sys.argv[1] == "local":
    api = "http://localhost:8000" + sys.argv[2]
else:
    api = "https://herb-server-mj26pnawdq-uc.a.run.app/" + sys.argv[2]

if sys.argv[2] == "/":
    print(requests.get(api).text)
else:

    image_file = "test_images/" + sys.argv[3] + ".jpg"

    with open(image_file, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    payload = json.dumps({"image": im_b64, "other_key": api})
    response = requests.post(api, data=payload, headers=headers)
    try:
        data = response.json()
        print("1st: X" + str(indexToXIndex[data["result index"][0]]) + ", confidence = " + str(data["result confidence"][0]))
        print("2nd: X" + str(indexToXIndex[data["result index"][1]]) + ", confidence = " + str(data["result confidence"][1]))
        print("3rd: X" + str(indexToXIndex[data["result index"][2]]) + ", confidence = " + str(data["result confidence"][2]))
    except requests.exceptions.RequestException:
        print(response.text)

end_time = datetime.datetime.now()
print(str((end_time - start_time).seconds) + "." + str((end_time - start_time).microseconds) + "s")