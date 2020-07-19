from flask import Flask
from flask import request
import imageIDHandler
import torch
import numpy as np
import NeuralNetwork
import torch
from torch.nn import functional as F

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
    out = F.softmax(net(image_t))
    out_json = {
        'out': out.argmax(dim=1).item(),
        'class': class_to_idx[out.argmax(dim=1).item()],
        'model_out': str(out.detach().numpy()[0])
    }
    prediction = 'do NOT'
    if out_json['class'] == 'Melanoma': 
        prediction='DO'
    formatted_text = f'The model has determined that you {prediction} have Melanoma.'
    return formatted_text


@app.route('/')
def index():
    return 'Server status - WORKING'


if __name__ == '__main__':
    net = torch.load('./model/melanoma_classification_model.pt').cpu()
    net.eval()
    app.run(debug=True)
