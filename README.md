# python-scikit-raspberrypi-garage-door-twilio-alert

## What

Ohai! This is my fun (overkill) project to use a raspberry pi camera plus data science to alert me when it classifies the garage door as being open.

## How

### The kit

- Raspberry pi 3 
- NoIR v2 camera
- IR floodlight

### Traning

Take a look at the `IR detection.ipynb` for the robust solution (using a NoIR v2 camera).

An overview:

* Capture 640x480 images using the motion debian package.
* Label the images as open/closed garage door images (I did a first pass using a crude classification heuristic to reduce the tedium of this).
* Convert the images to gray-scale, then to a vector.
* Make an intelligent train/test split (I figured that adjacent images might be very similar to each other and that randomly selecting train/test might therefor leak the target label).
* Train a simple LogisticRegression classifier.
* ?
* (Fun and) profit!

Note that I haven't uploaded the images to the github repo (`images` and `IR images` directories).

### Deployment

TODO