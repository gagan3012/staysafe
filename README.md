# StaySafe

![1d80efd004b044e19368956446371821](https://user-images.githubusercontent.com/49101362/119253289-59589280-bb65-11eb-9c9f-749289c0d11d.png)

Staying safe is very important in workplace setting. 

82% percent of women have indicated that they have faced some form of harassment in the workplace, but only 19% percent of cases have been reported. 

This happens primarily because of the embarrassment of reporting. But what if there was a way to prevent this embarrassment and while simultaneously allow the authorities to check in with the person reporting!

### Presenting StaySafe!!

Stay safe allows everyone to report harassment to the authorities and removes the embarrasment part of reporting.

Using StaySafe can also reduce the delay time between crime and report. This promotes workplace safety!

Youtube video: https://youtu.be/RsULWHqJpNk

### Model

StaySafe uses a CNN model which has an accuracy of 99% and has been well tested! The model architecture is as follows:

```
----------------------------------------------------------------
        Layer (type)               Output Shape         Param #
================================================================
            Conv2d-1           [-1, 80, 24, 24]           2,080
       BatchNorm2d-2           [-1, 80, 24, 24]             160
         MaxPool2d-3           [-1, 80, 12, 12]               0
            Conv2d-4             [-1, 80, 8, 8]         160,080
       BatchNorm2d-5             [-1, 80, 8, 8]             160
         MaxPool2d-6             [-1, 80, 4, 4]               0
            Linear-7                  [-1, 250]         320,250
            Linear-8                   [-1, 25]           6,275
================================================================
Total params: 489,005
Trainable params: 489,005
Non-trainable params: 0
```

### Instructions to run


The `requirements.txt` file should list all Python libraries that your notebooks
depend on, and they will be installed using:

```
pip install -r requirements.txt
```

To run the web application:
```
python app.py -i 0.0.0.0 -o 8080
```
It will run your app on http://localhost:8080/

### Dataset used
Sign Language MNIST (https://www.kaggle.com/datamunge/sign-language-mnist)

Each training and test case represents a label (0-25) as a one-to-one map for each alphabetic letter A-Z (and no cases for 9=J or 25=Z because of gesture motions).

**Note**: Right hand gestures are marked `safe` and Left hand gestures are marked `unsafe`!

### Usage

#### `I am okay` status
![](https://github.com/gagan3012/staysafe/blob/master/images/Screenshot%202021-05-23%20014047.png)

#### `I need Help` Status
![](https://github.com/gagan3012/staysafe/blob/master/images/Screenshot%202021-05-23%20014417.png)
