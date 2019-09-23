import requests


def imageSaver(url):
    img_data = requests.get(url).content
    with open('content_detection/imagebank/downloaded_image.jpg', 'wb') as handler:
        handler.write(img_data)
