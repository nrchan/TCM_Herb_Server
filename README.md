# TCM_Herb_Server
 
This is a flask server that aims to classify traditional chinese medicine herb.

## To run the code
You can pack this server into a docker image and run it wherever you like:

```
docker build -t server .
docker run server
```

Or, simply download the code and run it with command line:

```
python app.py
```

Or, if for any reason a pipenv environment is set up:

```
pipenv run start
```

## To test the server
The file `localtest.py` provides a simple way to test the server.

```
python localtest.py LOCAL MODE IMAGE
```
- LOCAL: 
  - Should be `"local"` if tested on local machine.
  - Could be any other string if uploaded to server (ex: `"api"`). Remember to change the server url in the file.
- MODE: 
  - Use `/` to try to connect with server. A successful connection will get a `Hello World!` response.
  - Use `/test` to test an image.
- IMAGE:
  - Enter an image name to test images from the folder `test_images`.

### Example:
Testing X2.jpg on local machine:
```
python localtest.py local /test 2
```

Trying to get a hello world response from the server:
```
python localtest.py api /
```