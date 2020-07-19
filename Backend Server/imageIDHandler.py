import requests
from PIL import Image


def resize_img(image: Image):
    image = image.crop((576, 0, 4032, 3456))
    image = image.resize((224, 224))
    return image


# Uses the imageID to get the image from Cloudinary API, and feeds it to the model
def handle_image_id(imageID):
    url = "https://res.cloudinary.com/starenkysoftware/image/upload/v1595173473/charterhacks/"+ imageID +".jpg"
    response = requests.get(url)

    imageData = response.content

    imageFile = open("imageReceived.png", 'wb')
    imageFile.write(imageData)
    imageFile.close()

    image = Image.open("imageReceived.png")
    image = resize_img(image)
    return image


def get_url():
    url = "https://res.cloudinary.com/starenkysoftware/image/upload/v1595173473/charterhacks/charter_hacks_image.jpg"
    response = requests.get(url)

    imageData = response.content

    imageFile = open("imageReceived.png", 'wb')
    imageFile.write(imageData)
    imageFile.close()

    image = Image.open("imageReceived.png")
    # image.show()
