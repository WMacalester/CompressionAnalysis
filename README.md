# CompressionAnalysis
An app to aid in determining the Young's modulus of a material from compression testing data. This app takes load vs distance data acquired using a a STARRET FMS-500-L2 Force Measurement System. Please ensure that the data has been exported from the system as a .csv file before loading into the app.

# First Time Installation.

First navigate to the app directory. Create a new virtual environment within the app directory. Activate the virtual environment for use whenever loading the app, then install all required packages listed in requirements. The following is an example for python >= 3.3.

`cd .../CompressionAnalysis/` - change directory to the app folder   
`python3 -m venv venv`  - create the virtual environment  
`venv\Scripts\activate` - activate the virtual environment  
`pip install -r requirements.txt` - install required packages   

# Using the App

First change the directory to the app folder, then activate the virtual environment, then run main.py to start the app. When you are finished using the app, remember to deactivate the virtual environment.

`cd .../CompressionAnalysis/` - change directory to the app folder.   
`venv\Scripts\activate` - activate the virtual environment.  
`python main.py` - runs the app.  
`venv\Scripts\deactivate` - deactivate the virtual environment when finished.

A prompt will open asking you to select which files you would like to open (this can be a batch of selected files). A new window will open, with the first dataset presented in the top graph. 

![Example Window](/ExampleWindowLabelled.png)

Using the sliders, enclose the region in the graph that corresponds to the linear elastic region. If necessary, you can use the zoom tool in the top toolbar to readjust the axes.

Select the shape of the object that you have compressed using the radio buttons, and input the relevant dimensions in mm. Note that the height is along the axis of compression here. 

Having entered all inputs, press the "Copy results to clipboard" button. This will perform the linear regression and add the name of the datafile, Young's modulus, regression intercept and regression R<sup>2</sup> to your clipboard. 

The graphs will update for visual confirmation that the calculation has been correctly calculated. In the top graph, please check that the red dotted line corresponds to the data in the region enclosed by the two sliders. In the bottom graph, please ensure that the black line is linear (hence in the linear elastic region), and that the green line is a faithful linear regression through those points.

When the data is suitable, paste the data in a separate spreadsheet for further analysis. Optionally, the graphs may be saved via the top toolbar for future reference if desired. If you have further datasets to process, the "Next data set" button will load the nextdata set. If you are finished analysing your datasets, please exit the app using the "Exit" button at the bottom of the app. 



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
  
### Sample Shapes

2 separate models have so far been incorporated for if the samples were either cuboidal or cylindrical in shape. This will affect the area calculations, and hence there are separate inputs for either model type.
