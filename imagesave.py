import requests


def imageSaver(url):
    img_data = requests.get(url).content
    with open('imagebank/downloaded_image.jpg', 'wb') as handler:
        handler.write(img_data)

imageSaver('https://2.bp.blogspot.com/-1F4CIsa0uJU/WQEao4Vn80I/AAAAAAAABTA/FBI7wnx0ryw2JRa3RC0O9Q2k35rNEr6ZgCLcB/s640/post_6_1.png')
