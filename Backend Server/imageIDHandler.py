# imports
import requests
from PIL import Image


'''
resizes image to 224x224

:param image: PIL Image object that will be resized
:return image: new resized image object
'''
def resize_img(image: Image):
    image = image.crop((576, 0, 4032, 3456))
    image = image.resize((224, 224))
    return image


'''
obtains image from cloudinary

:param imageID: image id from cloudinary
:return image: PIL Image object
'''
def handle_image_id(imageID):
    # constructed link with imageID
    url = "https://res.cloudinary.com/starenkysoftware/image/upload/v1595200550/charterhacks/"+ imageID

    # sends GET request to the API to obtain the image
    response = requests.get(url)

    # extract image
    imageData = response.content

    imageFile = open("image.jpg", 'wb')        # open image
    imageFile.write(imageData)                 # write image
    imageFile.close()                          # close writer

    image = Image.open("image.jpg")            # create Image object
    image = resize_img(image)                  # resize image
    return image                               # return image object
