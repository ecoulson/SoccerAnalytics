import yaml
import sys
import os
import random
from PIL import Image
from subprocess import Popen

config = None

with open("config.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
    
print(config['testImage'])

# config variables
frames = config['testSequence']['frames']
imgHeight = config['testImage']['width']
imgWidth = config['testImage']['width']
circles = config['testImage']['circles']
circleColor = config['testImage']['circleColor']
circleRadius = config['testImage']['circleRadius']

def createCircles():
    circleData = {}
    nonCollidingCircles = 0
    while nonCollidingCircles < circles:
        x = random.randrange(imgWidth)
        y = random.randrange(imgHeight)
        nonCollidingCircles += 1
    return circleData

# dir paths
sequenceCount = len(os.listdir("./test_sequences")) - 1
parentDir = "./test_sequences/sequence-{}".format(sequenceCount)
imageDir = "{}/images".format(parentDir)

#make dirs
os.mkdir(parentDir)
os.mkdir(imageDir)

#generateCircles
circles = createCircles()

color = [0,0,0]
black = [0,0,0]
white = [255,255,255]
for j in range(0, frames):
    color[1] += 1
    img = Image.new('RGB', (imgWidth, imgHeight))
    for x in range(0, imgWidth):
        for y in range(0, imgHeight):
            img.putpixel((x,y), (color[0], color[1], color[2]))
    img.save('{}/image-{}.png'.format(imageDir, j))

os.system("ffmpeg -f image2 -r 60 -i ./test_sequences/sequence-{}/images/image-%d.png -vcodec mpeg4 -y ./test_sequences/sequence-{}/out.mp4".format(sequenceCount, sequenceCount))