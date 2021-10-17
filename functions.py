import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, Frame, filedialog
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
matplotlib.use('TkAgg')
from scipy import stats

class CompressionAnalysis():

    def __init__(self) -> None:
        #Creating the tkinter window and frames
        self.root = tk.Tk()
        self.fig = plt.figure(figsize=(7,7), dpi=100)
        self.ax = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.fig.tight_layout(pad=3.0)
        self.scaleLabelFrame = Frame(self.root)
        self.scalesFrame = Frame(self.root)
        self.radioFrame = Frame(self.root)
        self.dimensionFrame = Frame(self.root)
        self.dimensionEntryFrame = Frame(self.root)
        self.copyLabelFrame = Frame(self.root)
        self.buttonsFrame = tk.Frame(self.root)
        self.quitButtonFrame = tk.Frame(self.root)

        #Choose data
        self.dataFile = filedialog.askopenfilenames()
        #Force window focus back to main page
        self.root.focus_force()
        #Holder for keeping track of which dataset to use
        self.dataCounter = 0
        
        #tkinter styles
        s = ttk.Style()
        s.configure("Scale1.Horizontal.TScale", background="black")
        s.configure("Scale2.Horizontal.TScale", background="red")
        s.configure("TButton",font=('Helvetica', 12))
        s.configure("TRadiobutton",font=('Helvetica', 12))
        s.configure("TLabel",font=('Helvetica', 12))
        s.configure("TEntry",font=('Helvetica', 12))

        #Holder for choosing model type, will be more relevant as I add more.
        self.modelChosen = tk.StringVar()
        self.modelChosen.set("cylinder")

        #Holder for cylinder model dimension inputs
        self.heightVar=tk.StringVar()
        self.heightVar.set("2")
        self.diameterVar = tk.StringVar()
        self.diameterVar.set("2")
        self.widthVar=tk.StringVar()
        self.lengthVar=tk.StringVar()
        self.widthVar.set("2")
        self.lengthVar.set("2")

        #Holder for Young's Modulus output data
        self.slopeVar = tk.DoubleVar()
        self.interceptVar = tk.DoubleVar()
        self.rSquaredVar = tk.DoubleVar()

        #Used to limit inputs to positive integers. %P used to check on key press in Entry widget.
        self.vcmd = (self.root.register(self.validateCommand), "%P")

    def processData(self):
        #Process data for the current data set
        self.dataFileString = self.dataFile[self.dataCounter].split("/")
        self.data = pd.read_csv(self.dataFile[self.dataCounter], usecols=(["distance","load"]),encoding="utf_16_le",sep="\t")
        self.data["load"] = -self.data["load"]
        self.data["distance"] = -self.data["distance"]
        self.yMax = self.data["load"].max()
        self.xMax = self.data["distance"].max()
        self.data.plot(x = "distance", y = "load", kind="scatter", legend=True, ax=self.ax)

    def toolbar(self):
        #create the interactive toolbar for plt
        frameToolbar = Frame(self.root)
        chartFrame = Frame(self.root)
        self.canvas = FigureCanvasTkAgg(self.fig, chartFrame)
        toolbar = NavigationToolbar2Tk(self.canvas, frameToolbar)
        toolbar.update()
        frameToolbar.pack()
        self.canvas.get_tk_widget().pack(side = tk.TOP)
        chartFrame.pack()

    def graphDecorators(self):
        self.ax.set_xlabel("Distance / mm")
        self.ax.set_ylabel("Load / N")
        self.ax.set_title(self.dataFileString[-1])
        #For some reason xlims do not get updated automatically when going to next dataset
        self.ax.set_xlim([0,self.xMax])

        self.ax2.set_xlabel("Strain / N m")
        self.ax2.set_ylabel("Stress")
        self.ax2.set_title('Stress-Strain Curve')

    def update(self,val):
    #Update vline x based on scale
        xvLine1 = self.xSlider1.get()
        xvLine2 = self.xSlider2.get()
        # Clear axis, removes old vlines that were persitent
        self.ax.cla()   
        # Create new vline
        self.ax.vlines(xvLine1,0,self.yMax,colors='k')
        self.ax.vlines(xvLine2,0,self.yMax,colors='r')
        # Replot data
        self.data.plot(x = "distance", y = "load", kind="scatter", legend=True, ax=self.ax)
        #Draw updated plot
        self.graphDecorators()
        self.fig.canvas.draw_idle()

    def sliders(self):
        sliderLabel = ttk.Label(self.scaleLabelFrame,text="Adjust the sliders to enclose the linear region", justify=tk.CENTER)
        self.xSlider1 = ttk.Scale(self.scalesFrame,from_=0,to=self.xMax,variable = self.xSliderValue1, orient="horizontal", command = self.update, style="Scale1.Horizontal.TScale" ) 
        #xLabel2 = ttk.Label(frame1,textvariable=xSliderValue2, font=(None,18))
        self.xSlider2 = ttk.Scale(self.scalesFrame,from_=0,to=self.xMax,variable = self.xSliderValue2, orient="horizontal", command = self.update,style="Scale2.Horizontal.TScale" ) 
        sliderLabel.pack()
        self.xSlider1.pack(side = tk.LEFT,padx = 10)
        #xLabel2.pack(side = tk.RIGHT, padx=40)
        self.xSlider2.pack(side = tk.LEFT,padx = 10)

        self.ax.vlines(self.xvLine1,0,self.yMax,colors='k')
        self.ax.vlines(self.xvLine2,0,self.yMax,colors='r')

        self.scaleLabelFrame.pack()
        self.scalesFrame.pack(pady=(0,10))

    def chooseModel(self):
        #Radio buttons to choose which model you would like to use
        self.radioLabel = ttk.Label(self.radioFrame, text = "Select the shape of object compressed").grid(row = 0, column=0,columnspan = 2)
        self.cylinderRadio = ttk.Radiobutton(self.radioFrame, text = "Cylinder",value = "cylinder",variable=self.modelChosen,command = self.clearEntryFrames).grid(row = 1, column=0)
        self.cuboidRadio = ttk.Radiobutton(self.radioFrame, text = "Cuboid", value = "cuboid",variable=self.modelChosen,command = self.clearEntryFrames).grid(row = 1, column=1)
        self.radioFrame.pack(pady=(0,10))

    def clearEntryFrames(self):
        self.unpackWidgetsAfterGraphs()
        self.widgetsAfterGraphs()

    
    #Check in input character is a digit in entry widgets. Reject addition of input if it is not.
    def validateCommand(self,P):
        if str.isdigit(P) or str(P) == "":
            return True
        else: 
            return False
    
    def cylinderEntries(self):
        #Input for cylinder model
        
        #Height label
        ttk.Label(self.dimensionFrame,text="Input height / mm").grid(row=0,column=0,padx=20)
        #Height textbox
        tk.Entry(self.dimensionEntryFrame, textvariable = self.heightVar,validatecommand=(self.vcmd),validate="all",width = 8).grid(row=0,column=0,padx=60)
        
        #Diameter label
        ttk.Label(self.dimensionFrame,text="Input diameter / mm").grid(row=0,column=1,padx=20)
        #Diameter Textbox
        tk.Entry(self.dimensionEntryFrame,textvariable = self.diameterVar,validatecommand=(self.vcmd),validate='all',width = 8).grid(row=0,column=1,padx=60)

        self.dimensionFrame.pack()
        self.dimensionEntryFrame.pack(pady=(0,5))

    def cuboidEntries(self):
        #Input for cuboid model
        
        #Height label        
        ttk.Label(self.dimensionFrame,text="Input height / mm").grid(row=0,column=0,padx=20)
        #Height textbox
        tk.Entry(self.dimensionEntryFrame, textvariable = self.heightVar,validatecommand=(self.vcmd),validate="all",width = 8).grid(row=0,column=0,padx=60)

        #Width Label
        ttk.Label(self.dimensionFrame,text="Input width / mm").grid(row=0,column=1,padx=20)
        #Width Textbox
        tk.Entry(self.dimensionEntryFrame,textvariable = self.widthVar,validatecommand=(self.vcmd),validate="all",width = 8).grid(row=0,column=1,padx=60)

        #Length Label
        ttk.Label(self.dimensionFrame,text="Input Length / mm").grid(row=0,column=2,padx=20)
        #Length Textbox
        tk.Entry(self.dimensionEntryFrame,textvariable = self.lengthVar,validatecommand=(self.vcmd),validate="all",width = 8).grid(row=0,column=2,padx=60)

        self.dimensionFrame.pack()
        self.dimensionEntryFrame.pack(pady=(0,5))

    def findIndex(self,value, df, colname):
        #Finding the index of the data that corresponds best to slider input value
        
        #limiting scope of dataframe that is being iterated through
        df = df[colname]
        maxIndex = len(df)-1
        minIndex = 0
        #Creating a guess index that will be tried first
        guessIndex = 1
        previousGuess = 0
        #begin the index finding process. This takes the central index in df and compares input value to df[index]. If the value was not found (e.g. too big or too small), the range is limited to the half the value lies in and the process is repeated until either the value is matched, or it is determined to be between two adjacent indices
        while previousGuess != guessIndex:
            previousGuess = guessIndex
            guessIndex = (maxIndex+minIndex)//2
            if df[guessIndex] == value:
                return guessIndex
            #In case the exact value desired is not in the array, this stops when the guesses are no longer making meaningful changes and returns the lower indexValue
            if maxIndex == minIndex:
                return min(previousGuess,guessIndex)
            #if guess is greater than value, move to sample below the guess index
            elif df[guessIndex] > value:
                maxIndex = guessIndex-1
            #if guess is greater than value, move to sample below the guess index
            elif df[guessIndex] < value:
                minIndex = guessIndex+1
        return guessIndex

    def linearRegression(self):
    #convert length and width to m, then get area
        if self.modelChosen.get() == "cuboid":
            area = (float(self.lengthVar.get())/1000)*(float(self.widthVar.get())/1000)
        elif self.modelChosen.get() == "cylinder":
            radius = float(self.diameterVar.get())/2000 # 
            area = np.pi * (radius**2)
        index1 = self.findIndex(self.xSliderValue1.get(),self.data,'distance')
        index2 = self.findIndex(self.xSliderValue2.get(),self.data,'distance')
        
        assert not index1 == index2, "Can't run the linear regression on a single point. Adjust the sliders to give a range of values over the linear region"

        if index1>index2:
            upperbound,lowerbound = index1,index2
        else:
            upperbound,lowerbound = index2,index1
    
        ###Checking area over which linear regression is going to happen

        #Plot the selected region in the raw data graph to visually confirm input.
        self.ax2.cla()
        self.update(None) # None value to compensate for val normally returned by buttons
        newdf2 = pd.concat([self.data[lowerbound:upperbound]["distance"],self.data[lowerbound:upperbound]["load"]],axis = 1,keys = ["x","y"])
        newdf2.plot(x = "x", y = "y", kind="line", ax=self.ax, color="red", style = "--", label = "Selected Region")

        ###Process input data to get Young's modulus
        df = pd.DataFrame()
        df["strain"] = self.data[lowerbound:upperbound]["distance"]/float(self.heightVar.get()) #mm/mm
        df["stress"] = self.data[lowerbound:upperbound]["load"]/area #N/m^2
        strain = df["strain"]
        stress = df["stress"]

        slope, intercept, r_value, p_value, std_err = stats.linregress(strain,stress)
        self.slopeVar.set(slope)
        self.interceptVar.set(intercept)
        self.rSquaredVar.set(r_value)
        
        ###Plotting the determined regression line for visual confirmation of linear region

        #Plot the regressione line
        self.graphDecorators()
        newdf = pd.concat([self.data[0:len(self.data)]["distance"],(self.data[0:len(self.data)]["distance"]*slope)+intercept],axis = 1,keys = ["x","y"])
        newdf.plot(x = "x", y = "y", kind="line", ax=self.ax2, color="green", style = "--", label="Fitted Line")
        
        #Plotting Stress-Strain Curve
        df.plot(x = "strain", y = "stress", kind="line", ax=self.ax2, color="black", style = "--", label = "Stress-Strain Curve for Selected Region")
        right = df.iloc[-1]["strain"]
        left = df.iloc[0]["strain"]
        top = df.iloc[-1]["stress"]
        bottom = df.iloc[0]["stress"]
        self.ax2.set_xlim(left,right)
        self.ax2.set_ylim(bottom,top)

        self.fig.canvas.draw_idle()

    def unpackWidgetsAfterGraphs(self):
        #Unpacking widgets so that they can be updated
        self.dimensionFrame.pack_forget()
        self.dimensionEntryFrame.pack_forget()  
        self.copyLabelFrame.pack_forget()
        self.buttonsFrame.pack_forget()
        self.quitButtonFrame.pack_forget()
        self.radioFrame.pack_forget()
        
    def widgetsAfterGraphs(self):
        #Repacking widgets to update
        self.radioFrame = Frame(self.root)
        self.dimensionFrame = Frame(self.root)
        self.dimensionEntryFrame = Frame(self.root)
        self.copyLabelFrame = Frame(self.root)
        self.buttonsFrame = tk.Frame(self.root)
        self.quitButtonFrame = tk.Frame(self.root)

        self.chooseModel()
        if self.modelChosen.get() == "cuboid":
            self.cuboidEntries()
        elif self.modelChosen.get() == "cylinder":
            self.cylinderEntries()
        self.copyButton()
        self.nextButton()
        self.quitButton()
        
    def copyResults(self):
        self.linearRegression()
        self.root.clipboard_clear()
        self.root.clipboard_append(str(self.dataFileString[-1])+"\t"+str(self.slopeVar.get())+"\t"+str(self.interceptVar.get())+"\t"+str(self.rSquaredVar.get()))
        self.root.update() # now it stays on the clipboard after the window is closed

    def copyButton(self):
        ttk.Label(self.copyLabelFrame,text = "Press the copy button to get results on clipboard:\nFile name, Young's Modulus / Pa, Regression intercept and R\u00b2",justify=tk.CENTER, style="CopyLabel.TLabel").pack(pady=10)
        ttk.Button(self.buttonsFrame,text="Copy results to clipboard",command = self.copyResults).pack(side = tk.LEFT)
        self.copyLabelFrame.pack()
        self.buttonsFrame.pack()
    
    def nextButtonCommand(self):
        #Updating dataset used, and updating all widgets to match the new dataset
        self.dataCounter += 1
        self.processData()
        self.graphDecorators()
        self.update(None)
        self.unpackWidgetsAfterGraphs()
        self.scalesFrame.pack_forget()
        self.scaleLabelFrame.pack_forget()
        self.scalesFrame = tk.Frame(self.root)
        self.scaleLabelFrame = tk.Frame(self.root)
        self.sliders()
        self.widgetsAfterGraphs()
        self.ax2.cla()
        self.fig.canvas.draw_idle()
    
    def nextButton(self):
        #First check if there is another dataset left to be processed from selection. If not, disable the button. 
        if self.dataCounter < len(self.dataFile)-1:
            ttk.Button(self.buttonsFrame,text="Next data set",command=self.nextButtonCommand).pack(side = tk.LEFT)
            self.buttonsFrame.pack()
        else:
            ttk.Button(self.buttonsFrame,text="Next data set",command=self.nextButtonCommand,state="disabled").pack(side = tk.LEFT)
            self.buttonsFrame.pack()
   
    def quitButtonCommand(self):
        self.root.quit()
        self.root.destroy()

    def quitButton(self):
        ttk.Button(self.quitButtonFrame, text="Exit",command = self.quitButtonCommand).pack()
        self.quitButtonFrame.pack()

    def start(self):
        self.processData()
        self.xSliderValue1 = tk.DoubleVar(self.root, value=0)
        self.xSliderValue2 = tk.DoubleVar(self.root, value=self.xMax)
        self.xvLine1 = 0
        self.xvLine2 = self.xMax
        self.toolbar()
        self.processData()
        self.graphDecorators()
        self.sliders()
        self.widgetsAfterGraphs()

        self.root.mainloop()