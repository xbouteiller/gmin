# gminComputation : a Python Program for estimating leaf conductance


Current version is: **2.0**

<img src="img/B22_LITU_BL_09.png" width="65%" height="65%">

## Highlights 

### Improvement in gmin estimation

- VPD can be corrected

<a href="https://www.codecogs.com/eqnedit.php?latex=WP=p_0/(&space;{\overline{RWC}}/{100})&plus;&space;max(-p_0-\varepsilon&space;\times(1-&space;{\overline{RWC}}/{100}),0)&space;\newline&space;\newline&space;VPD&space;=&space;611.21&space;\times&space;e^{(18.678-\overline{T}/234.5)\times\overline{T}/(257.14&plus;\overline{T})}&space;\times&space;e^{(WP\times2.16947115/(\overline{T}&plus;273.15))-\overline{RH}/100)}/1000" target="_blank"><img src="https://latex.codecogs.com/gif.latex?WP=p_0/(&space;{\overline{RWC}}/{100})&plus;&space;max(-p_0-\varepsilon&space;\times(1-&space;{\overline{RWC}}/{100}),0)&space;\newline&space;\newline&space;VPD&space;=&space;611.21&space;\times&space;e^{(18.678-\overline{T}/234.5)\times\overline{T}/(257.14&plus;\overline{T})}&space;\times&space;e^{(WP\times2.16947115/(\overline{T}&plus;273.15))-\overline{RH}/100)}/1000" title="WP=p_0/( {\overline{RWC}}/{100})+ max(-p_0-\varepsilon \times(1- {\overline{RWC}}/{100}),0) \newline \newline VPD = 611.21 \times e^{(18.678-\overline{T}/234.5)\times\overline{T}/(257.14+\overline{T})} \times e^{(WP\times2.16947115/(\overline{T}+273.15))-\overline{RH}/100)}/1000" /></a>
- Leaf shrinkage can be corrected

<a href="https://www.codecogs.com/eqnedit.php?latex=Shrinkage&space;=&space;a&space;&plus;&space;b&space;\times&space;rwc&plus;&space;c&space;\times&space;rwc^2&space;&plus;d&space;\times&space;rwc^3&space;&plus;&space;e&space;\times&space;rwc^4" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Shrinkage&space;=&space;a&space;&plus;&space;b&space;\times&space;rwc&plus;&space;c&space;\times&space;rwc^2&space;&plus;d&space;\times&space;rwc^3&space;&plus;&space;e&space;\times&space;rwc^4" title="Shrinkage = a + b \times rwc+ c \times rwc^2 +d \times rwc^3 + e \times rwc^4" /></a>

### Improvement in program flow

- Work directly frow raw files
- A batch mode is implemented
- A Conf file is used and can modified by the user

<br> </br>

## Using this new version of gmin

See the last section for more details about how to use the program 

### Work directly from raw files

You can directly use the files from the climatic chambers. The following columns are mandatory, but names can be customized (in the conf file ), if several sensors are used for measuring temperature or RH, mean value will be computed.

- **date_time** : time **(default is dd/mm/yyyy H:M)**
- **Campaign** : campaign name
- **Comment**
- **T_C** : temperature (??C)
- **RH** : Relative Humidity
- **Weight measured** : 1 column for each sample, the column header should match with the position in the metadata file.

you can see an example in the section [input files](https://github.com/xbouteiller/gmin/tree/main/input_files)



### A metadata file is mandatory

All the columns must have the **exact current names** indicated

The following columns must be filled, if not, it will raise an Error

- **sample_ID** : ID of the sample, should be **unique** for each sample
- **position** : the **unique** position in the climatic chamber, it should match the sample column header in the datafile
- **Area_m2** : area of the leaf (m2)
- **Patm** : atmospheric pressure (KPa)

Following columns must be in metadatafile but can be empty, if empty a default behaviour is adopted
- **Species**
- **site**
- **Fresh_weight** : fresh (saturated) weight of the leaf (g)
- **Dry_weight** : dry weight of the leaf (g)
- **rwc_sup**: superior threshold for filtering rwc
- **rwc_inf**: inferior threshold for filtering rwc
- **a, b, c, d, e**: parameters for computing leaf shrinkage
- **eps, p0**: parameters for correcting VPD
- **TLP**

you can see an example in the section [input files](https://github.com/xbouteiller/gmin/tree/main/input_files)

Note that if you named your file : **metadata.csv**, it can be included in the data folder

### A conf file is needed

A file named conf.cfg is expected in the program folder. It can be modified by the user.

-**config** section is mandatory
-**optional** section contains info for executing the program without prompting the menu, **use_opt** should be turned to True is you want to use
-**batch** parameters for the batch mode

Future version will allow the user to place its own conf file with the data

<br> </br>

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
    - A folder that will be parsed for the data files
    - A metatadata file
<img src="img/Screenshot from 2021-04-28 15-38-37.png" width="75%" height="75%">

The program writes the number of files found
<img src="img/Screenshot from 2021-04-28 15-39-10.png" width="75%" height="12%">

#### Step 2
2. You have to chose which method you will use:
    - Select time interval manually then compute gmin in the interval time
    - Filtering the data based on RWC and then compute gmin in the interval time
    - Batch mode
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

#### Step 3 - Option 3
4. If you chose the batch method:
    - A sliding RWC window is used to filter the files. Except that it is similar to the RWC method
    - Generated files are agregated within the same csv file

5. The data are first filtered based on RWC:
<img src="img/VIAL12.png" width="75%" height="75%">

Default values for the RWC filtering are 80% and 50%, but this can be changed manually:
>
> python gminExec.py --rwc_sup 90 --rwc_inf 20 # Superior threshold : 90%, inferior : 20%  
> 

or in the metadata file for each sample.

6. If the columns Dry_weight and Fresh_weight are provided, he software use the provided values to compute RWC 

7. **New** if values are provided in the column a, b, c, d, e the leaf shrinkage is corrected using the formula:

<a href="https://www.codecogs.com/eqnedit.php?latex=Shrinkage&space;=&space;a&space;&plus;&space;b&space;\times&space;rwc&plus;&space;c&space;\times&space;rwc^2&space;&plus;d&space;\times&space;rwc^3&space;&plus;&space;e&space;\times&space;rwc^4" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Shrinkage&space;=&space;a&space;&plus;&space;b&space;\times&space;rwc&plus;&space;c&space;\times&space;rwc^2&space;&plus;d&space;\times&space;rwc^3&space;&plus;&space;e&space;\times&space;rwc^4" title="Shrinkage = a + b \times rwc+ c \times rwc^2 +d \times rwc^3 + e \times rwc^4" /></a>


8. **New** if values are provided in the column eps, p0 the vpd is corrected using the formula:

<a href="https://www.codecogs.com/eqnedit.php?latex=WP=p_0/(&space;{\overline{RWC}}/{100})&plus;&space;max(-p_0-\varepsilon&space;\times(1-&space;{\overline{RWC}}/{100}),0)&space;\newline&space;\newline&space;VPD&space;=&space;611.21&space;\times&space;e^{(18.678-\overline{T}/234.5)\times\overline{T}/(257.14&plus;\overline{T})}&space;\times&space;e^{(WP\times2.16947115/(\overline{T}&plus;273.15))-\overline{RH}/100)}/1000" target="_blank"><img src="https://latex.codecogs.com/gif.latex?WP=p_0/(&space;{\overline{RWC}}/{100})&plus;&space;max(-p_0-\varepsilon&space;\times(1-&space;{\overline{RWC}}/{100}),0)&space;\newline&space;\newline&space;VPD&space;=&space;611.21&space;\times&space;e^{(18.678-\overline{T}/234.5)\times\overline{T}/(257.14&plus;\overline{T})}&space;\times&space;e^{(WP\times2.16947115/(\overline{T}&plus;273.15))-\overline{RH}/100)}/1000" title="WP=p_0/( {\overline{RWC}}/{100})+ max(-p_0-\varepsilon \times(1- {\overline{RWC}}/{100}),0) \newline \newline VPD = 611.21 \times e^{(18.678-\overline{T}/234.5)\times\overline{T}/(257.14+\overline{T})} \times e^{(WP\times2.16947115/(\overline{T}+273.15))-\overline{RH}/100)}/1000" /></a>

9. Gmin is computed based on a linear regression between the two boundaries of the RWC filtered data
<img src="img/VIAL12 g.png" width="75%" height="75%">

#### Step 5
10. Synthetic figures and data frames are saved within the output_fig and output_files folder or batch folder if batch mode was used

<br> </br>


<br> </br>

