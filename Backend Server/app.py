from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/getResults')
def getResults():
    imageID = request.args.get('imageID')

    # Use the imageID to access cloudinary and fetch results from the model here

    return "you made a request for imageID: " + imageID

@app.route('/')
def index():
    return "welcome"

if __name__ == '__main__':
    app.run(debug=True)