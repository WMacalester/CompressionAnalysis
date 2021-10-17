# CompressionAnalysis
An app to aid in determining the Young's modulus of a material from compression testing data. This app takes load vs distance data acquired using a a STARRET FMS-500-L2 Force Measurement System. Please ensure that the data has been exported from the system as a .csv file before loading into the app.


# Installation
This app makes use of the tkinter and matplotlib libraries. These should be pre-installed if you are using the anaconda distribution of python

* To check if you have tkinter, please run the following in the command line:

python -m tkinter

* To check if you have matplotlib installed, please run the following in a new file:

import matplotlib

print(matplotlib.\_\_version\_\_)


### Please use the following resources to install these libraries if they are not installed

Tkinter - https://tkdocs.com/tutorial/install.html
Matplotlib - https://matplotlib.org/stable/users/installing.html

### Installing Compression Analysis App

Download the Compression Analysis app folder as a zip file and extract the folder to a new directory.

# Using the App

Run main.py to start the app. A prompt will open asking you to select which files you would like to open (this can be a batch of selected files). A new window will open, with the first dataset presented in the top graph. 

Using the sliders, enclose the region in the graph that corresponds to the linear elastic region. If necessary, you can use the zoom tool in the top toolbar to readjust the axes.

Select the shape of the object that you have compressed using the radio buttons, and input the relevant dimensions in mm. Note that the height is along the axis of compression here. 

Having entered all inputs, press the "Copy results to clipboard" button. This will perform the linear regression and add the name of the datafile, Young's modulus, regression intercept and regression R<sup>2</sup> to your clipboard. 

The graphs will update for visual confirmation that the calculation has been correctly calculated. In the top graph, please check that the red dotted line corresponds to the data in the region enclosed by the two sliders. In the bottom graph, please ensure that the black line is linear (hence in the linear elastic region), and that the green line is a faithful linear regression through those points.

When the data is suitable, paste the data in a separate spreadsheet for further analysis. Optionally, the graphs may be saved via the top toolbar for future reference if desired. If you have further datasets to process, the "Next data set" button will load the nextdata set. If you are finished analysing your datasets, please exit the app using the "Exit" button at the bottom of the app. 

![Example Window](/ExampleWindowLabelled.png)

### The Calculations

The Young's modulus is a mechanical property of a material that characterises the deformation (strain) that arises upon the application of a force (stress) along the axis of compression within the linear elastic region. 

<a href="https://www.codecogs.com/eqnedit.php?latex=E&space;=&space;\frac{stress}{strain}&space;=&space;\frac{F/A}{\Delta&space;l/L}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?E&space;=&space;\frac{stress}{strain}&space;=&space;\frac{F/A}{\Delta&space;l/L}" title="E = \frac{stress}{strain} = \frac{F/A}{\Delta l/L}" /></a>

where:
* E = Young's Modulus
* F = Force / N
* A = Area / m<sup>2</sup>
* Δl = Distance compressed
* L = Total length of object along the compressed axis

The Young's modulus can therefore be approximated by linear regression across the linear elastic region of the stress-strain curve. This app outputs the calculated Young's modulus for a given set of inputs, along with the calculated intercept and R<sup>2</sup> values from the regression.
  
##### Sample Shapes

2 separate models have so far been incorporated for if the samples were either cuboidal or cylindrical in shape. This will affect the area calculations, and hence there are separate inputs for either model type.
