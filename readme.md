# Dots, Moving Dots
This repository contains two toy datsets - dots and moving dots, which can be used for mechanistic interpretability analyses and other applications. Both are classificatino datasets, where the input is a sequence of 2D coordinates.

## Description

### Dots data
In the dots data, the classes are regular polygons(here: triangle, square, pentagon, hexagon, heptagon, octagon). A datapoint is constructed by having a regular polygon in random orientation, scale, and position in the positive 1x1 space and then sampling N points from its perimeter, including the vertices. 
The code for generating data allows to generate as many data points with the specified number of sampling points. 
The orientation, scale, and position give variability while maintaining the characteristic structure, which is the shape. 

![Dots](images/dots.png)

### Moving dots data
In moving dots data, there are 4 ordered dots that are moving. One dot can move in any one of the three ways - stationary, line, or circle. The pattern in which each dot is moving characterizes a class. The motion is sampled into thirteen frames. For variability - the line has a random orientation and direction; the circle has a random scale and direction; and the stationary has a random position. 

The six classes which were used here are as follows (in order of dots):

- line, line, line, line
- circle, circle, circle, circle
- line, stationary, stationary, stationary
- circle, stationary, stationary, stationary
- stationary, line, line, stationary
- stationary, circle, circle, stationary

![Moving Dots](images/moving_dots.png)

This dataset has a dynamic character. (frame, dot, 2) shaped datapoint is reshaped into (frame x dot, 2), and this sequence of 2D coordinates is used as input to models(sequence length = 13 x 4 = 52). The positions are meaningful; for example, the first four positions in the input sequence correspond to the first frame, and so on. i.e., there is a semantic associated with the inputs just by virtue of their position.

## Usage

Use the `make_data.ipynb` notebook in the corresponding folder to generate data with a specified set of parameters. The data will be generated as four `.npy` files - `X_train`, `X_test`, `y_train`, `y_test`. A dataloader file which access these `.npy` files is also provided. 

In each, there is a ready to use dataset as well, which can be direclty used: 
- Dots : 10K datapoints per class, 12 samples in each datapoint, ordered.
- Moving dots : 10K datapoints per class, 13 frames.

Make changes in `dots.py`, `moving_dots.py` for tweaking the code; for example changing classes, adding classes, visualizing, etc. 