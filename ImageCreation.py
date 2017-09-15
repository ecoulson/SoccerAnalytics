import yaml
import math
import sys
import os
import random
import subprocess
import signal
import shutil
import time
from PIL import Image
from subprocess import Popen

config = None

with open("config.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# config variables
frames = config['testSequence']['frames']
imgHeight = config['testImage']['width']
imgWidth = config['testImage']['width']
circleCount = config['testImage']['circles']
circleColor = config['testImage']['circleColor']
circleRadius = config['testImage']['circleRadius']
moveDelta = config['testSequence']['movementDelta']

def createCircles():
    circleData = {}
    nonCollidingCircles = 0
    while nonCollidingCircles < circleCount:
        current = nonCollidingCircles
        x = random.randint(circleRadius, imgWidth - circleRadius)
        y = random.randint(circleRadius, imgHeight - circleRadius)
        if len(circleData) > 0:
            collisionExists = False
            for key in circleData:
                other = circleData[key]
                dist = math.sqrt((other['x'] - x) * (other['x'] - x) + (other['y'] - y) * (other['y'] - y))
                r = circleRadius * 2
                if (dist < r):
                    collisionExists = True
                    break
            if not collisionExists:
                nonCollidingCircles += 1
        if len(circleData) == 0:
            nonCollidingCircles += 1

        if (current < nonCollidingCircles):
            circleData[nonCollidingCircles] = { 'x': x, 'y': y }
    return circleData

def moveCircles(circles):
    for circle in circles:
        other = circles[circle]
        if other['x'] <= circleRadius + moveDelta or other['x'] >= imgWidth - circleRadius - moveDelta:
            if other['x'] <= circleRadius + moveDelta:
                other['x'] = circleRadius + moveDelta + 1
                return
            elif other['x'] >= imgWidth - circleRadius - moveDelta:
                other['x'] = imgWidth - circleRadius - moveDelta - 1
                return
        if other['y'] <= imgHeight + moveDelta or other['y'] >= imgHeight - circleRadius - moveDelta:
            if other['y'] <= circleRadius + moveDelta:
                other['y'] = circleRadius + moveDelta + 1
                return
            elif other['y'] >= imgHeight - circleRadius - moveDelta:
                other['y'] = imgHeight - circleRadius - moveDelta - 1
                return
        other['y'] += random.randint(-moveDelta, moveDelta)
        other['x'] += random.randint(-moveDelta, moveDelta)

#create dir
if not os.path.isdir("./test_sequences"):
    os.mkdir("./test_sequences")
if os.path.isfile("./test_sequences/.DS_Store"):
    os.remove("./test_sequences/.DS_Store")
sequenceCount = len(os.listdir("./test_sequences"))
parentDir = "./test_sequences/sequence-{}".format(sequenceCount)
imageDir = "{}/images".format(parentDir)
if not os.path.isdir(parentDir):
    os.mkdir(parentDir)
if not os.path.isdir(imageDir):
    os.mkdir(imageDir)

shutil.copyfile("./config.yml", "{}/test_config.yml".format(parentDir))

#generateCircles
circles = createCircles()

color = [0,0,0]
black = [0,0,0]
white = [255,255,255]

#generates frames
for j in range(0, frames):
    moveCircles(circles)
    color[1] += 1
    img = Image.new('RGB', (imgWidth, imgHeight))
    px = img.load()
    for circle in circles:
        other = circles[circle]
        for x in range (other['x'] - circleRadius, other['x'] + circleRadius):
            for y in range (other['y'] - circleRadius, other['y'] + circleRadius):
                dist = (x - other['x']) * (x - other['x']) + (y - other['y']) * (y - other['y'])
                r = circleRadius * circleRadius
                if dist < r:
                    px[x,y] = (white[0], white[1], white[2])
    img.save('{}/image-{}.png'.format(imageDir, j))

pro = subprocess.Popen(["ffmpeg", "-f", "image2", "-r", "60", "-i", "./test_sequences/sequence-{}/images/image-%d.png".format(sequenceCount), "-vcodec", "mpeg4", "-y", "./test_sequences/sequence-{}/out.mp4".format(sequenceCount)])

