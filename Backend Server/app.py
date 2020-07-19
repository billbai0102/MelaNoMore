from flask import Flask
from flask import request
import imageIDHandler
import torch
import numpy as np
import NeuralNetwork
from torchsummary import summary

app = Flask(__name__)


@app.route('/getResults')
def get_results():
    class_to_idx = {0: 'Melanoma', 1: 'NotMelanoma'}

    imageID = request.args.get('imageID')

    # Use the imageID to access cloudinary and fetch results from the model here
    image = imageIDHandler.handle_image_id(imageID)
    image_np = np.asarray(image).transpose(2, 0, 1)
    image_np = np.expand_dims(image_np, axis=[0])
    image_t = torch.Tensor(image_np).float()
    out = net(image_t)
    out_json = {
        'out': out.argmax(dim=1).item(),
        'class': class_to_idx[out.argmax(dim=1).item()],
        'model_out': str(list(out.detach().numpy()[0]))
    }
    print(str(list(out.detach().numpy()[0])))
    return out_json


@app.route('/')
def index():
    return 'Server status - WORKING'


if __name__ == '__main__':
    net = torch.load('./model/melanoma_classification_model.pt').cpu()
    net.eval()
    app.run(debug=True)
