import requests
from PIL import Image

# Uses the imageID to get the image from Cloudinary API, and feeds it to the model
def handleImageID(imageID):
    url = "https://res.cloudinary.com/starenkysoftware/image/upload/v1595173473/charterhacks/"+ imageID +".jpg"
    response = requests.get(url)

    imageData = response.content

    imageFile = open("imageReceived.png", 'wb')
    imageFile.write(imageData)
    imageFile.close()

    image = Image.open("imageReceived.png")
    image.show()

def getURL():
    url = "https://res.cloudinary.com/starenkysoftware/image/upload/v1595173473/charterhacks/charter_hacks_image.jpg"
    response = requests.get(url)

    imageData = response.content

    imageFile = open("imageReceived.png", 'wb')
    imageFile.write(imageData)
    imageFile.close()

    image = Image.open("imageReceived.png")
    image.show()

getURL()