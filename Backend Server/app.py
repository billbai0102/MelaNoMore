# imports
from flask import Flask
from flask import request
from flask_ngrok import run_with_ngrok
import numpy as np
import imageIDHandler
import NeuralNetwork
import torch
from torch.nn import functional as F

# instantiates flask app, sets flask to run with ngrok
app = Flask(__name__)
# run_with_ngrok(app)

'''
returns model's output given the image's ID
'''
@app.route('/getResults')
def get_results():
    # class to idx dict - maps model output to class
    class_to_idx = {0: 'Melanoma', 1: 'NotMelanoma'}

    # gets imageID from parameters
    imageID = request.args.get('imageID')

    # fetch image from cloudinary
    image = imageIDHandler.handle_image_id(imageID)

    image_np = np.asarray(image).transpose(2, 0, 1)     # transpose image from (H, W, C) to (C, H, W)
    image_np = np.expand_dims(image_np, axis=[0])       # add a dimension (batch)
    image_t = torch.Tensor(image_np).float().cuda()     # convert image array to cuda float32 tensor
    out = F.softmax(net(image_t))                       # gets output of network (normalized between 0 and 1)

    # create json object to store model results
    out_json = {
        'out': out.argmax(dim=1).item(),
        'class': class_to_idx[out.argmax(dim=1).item()],
        'model_out': str(out.detach().cpu().numpy()[0])
    }

    # return model results
    return out_json


'''
default app route /
'''
@app.route('/')
def index():
    return 'Server status - WORKING'


'''
instantiates the model and starts server with ngrok
'''
if __name__ == '__main__':
    net = torch.load('./model/melanoma_classification_model.pt').cuda()
    net.eval()
    app.run(debug=True)
