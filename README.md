# Python Program for computing leaf conductance


Current version is: **2.0**

<img src="img/B22_LITU_BL_09.png" width="65%" height="65%">

## A new version of Gmin


### Highlights

Improvement of gmin estimation:
- VPD can be corrected
- Leaf shrinkage can be corrected

Program flow:
- Work directly frow raw files
- A batch mode is implemented
- Conf file can be used



### Work directly from raw files

You can directly use the files from the climatic. 
It should contain at least the following columns:
- date_time : time **(default is dd/mm/yyyy H:M)**
- Campaign: campaign name
- Comment
- T_C : temperature (°C)
- RH : Relative Humidity
- Weight measured: 1 column = 1 sample, the column header should be the 

you can see an example in the folder [input files](https://github.com/xbouteiller/gmin/tree/main/input_files)

### A metadata file is mandatary

It must necessarly contains the following columns:

- sample_ID : ID of the sample, should be **unique** for each sample
- position : the **unique** position in the climatic chamber, it should match the sample column header in the datafile
- Area_m2 : area of the leaf (m2)
- Patm : atmospheric pressure (KPa)

Following columns must be in metadatafile but can be empty, if empty a default behaviour is adopted
- Fresh_weight : fresh (saturated) weight of the leaf (g)
- Dry_weight : dry weight of the leaf (g)
- rwc_sup: superior threshold for filtering rwc
- rwc_inf: inferior threshold for filtering rwc
- a, b, c, d, e: parameters for computing leaf shrinkage
- eps, p0: parameters for correcting VPD
- TLP

Note that if you name your file : **metadata.csv**, it can be included in the data folder

### A conf file is needed

A file named conf.cfg is expected in the program folder. It can be modified by the user
-[config] section is mandatory
-[optional] section contains info for executing the program without prompting the menu, **use_opt** should be set to True is you want to use
-[batch] is only useful for the batch mode


## How to install?

### Install Python version if needed

[Miniconda](https://docs.conda.io/en/latest/miniconda.html)


### Download full folder from git

1. Direct download

From the green box  named 'clone' in the right corner > download .zip

2. From the terminal

>
> git clone https://github.com/xbouteiller/gmin.git
>


### Install dependencies


>
> pip install -r requirements.txt 
>

### Install package

Open a terminal in the DetectEvent folder, then :

>
> python setup.py install
>


### Program Execution


In a terminal 


>
> python gminExec.py
>



I also provided some additonal for simplifying execution in the **exec** folder

if you are on a windows platform:

- create a shorcut for the *launch.bat* file
- place the shortcut in an ampty folder and double click on it
- the program will be executed in the terminal and files & figures will be saved in the empy folder


if you are on a linux platform:

1. in the *bash-ex-linux.sh* file
    - replace the path */home/xavier/anaconda3/bin/python* with the path linking to your python version 
    - if you use anaconda you should have to replace only *xavier* with you user name
    - replace the path */home/xavier/Documents/development/gmin/gminExec.py* with the correct path linking to the *gminExec.py* file
2. in the *launch-linux.desktop*
    - replace the path */home/xavier/Documents/development/gmin/exec/bash-ex-linux.sh* with the correct path to *bash-ex-linux.sh*
    - you can now copy the *launch-linux.desktop* file in a new folder and double click on it



### Installing updates

>
> git pull origin main
>
> python setup.py install
>

<br> </br>

## Program flow


#### Step 1
1. The program ask to chose:
    - A folder that will be parsed 
    - Some unique ID from a single file
<img src="img/Screenshot from 2021-04-28 15-38-37.png" width="75%" height="75%">

The program writes the number of files found
<img src="img/Screenshot from 2021-04-28 15-39-10.png" width="75%" height="12%">

#### Step 2
2. You have to chose which method you will use:
    - Select time interval manually then compute gmin in the interval time
    - Filtering the data based on RWC and then compute gmin in the interval time
<img src="img/Screenshot from 2021-04-28 15-39-13.png" width="75%" height="120%">

#### Step 3 - Option 1
3. If you chose the manual points selection:
    - You have to select two points on the curve
    - Gmin is computed based on a linear regression between these two points
<img src="img/B17_LITU_BL_11.png" width="75%" height="75%">


#### Step 3 - Option 2
4. If you chose the method based on RWC:
    - the semi auto method will plot curve each time
    - the full auto will precede to the gmin computation automatically


5. The data are first filtered based on RWC:
<img src="img/VIAL12.png" width="75%" height="75%">

Default values for the RWC filtering are 80% and 50%, but thsi can be changed manually:
>
> python gminExec.py --rwc_sup 90 --rwc_inf 20 # Superior threshold : 90%, inferior : 20%  
> 
> python gminExec.py -rs 90 -ri 20 # It is a shortcut for the code above
>

6. **New** if the columns Dry_weight and Fresh_weight are provided, he software use the provided values to compute RWC    


7. Gmin is computed based on a linear regression between the two boundaries of the RWC filtered data
<img src="img/VIAL12 g.png" width="75%" height="75%">

#### Step 5
8. Synthetic figures and data frames are saved within the output_fig and output_files folder

<br> </br>

## Data format

Data must be stored within files
For a better files recognition, first row of the csv file should contain the string "conductance" otherwise all csv from a folder will be parsed

Columns should be named as follows:


#### Quantitative columns

- weight_g : leaf weight as a function of time (g)
- T_C : temperature (°C)
- RH : Relative Humidity
- Patm : atmospheric pressure (KPa)
- Area_m2 : area of the leaf (m2)
- Fresh_weight : fresh (saturated) weight of the leaf (g)
- Dry_weight : dry weight of the leaf (g)

#### Qualitative columns

- campaign : campaign name
- sample_ID : ID of the sample, should be unique for each sample

#### Date

- date_time : time **(best with the format YEAR/MONTH/DAY HOUR:MINUTE )**

<br> </br>

