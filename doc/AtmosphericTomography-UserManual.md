% Atmospheric Tomography User Manual
% Sangeeta Bhatia

About the software
=================================

The Atmospheric Tomography software is a command line tool written in python to estimate the emission rate of a point source from concentration data. It implements an extension of the Bayesian inversion method outlined in [this](http://www.sciencedirect.com/science/article/pii/S187661021300550X) paper. 

This manual walks a user through the steps needed to run the Atmospheric Tomography program. Please report any errors or omissions to the author.

Plume Dispersion Model
=================================
A Lagrangian stochastic (LS) model [@thomson1987criteria] as implemented
in WindTrax Version 2.0.8.8 [@windtrax] was used for forward modeling
i.e. to predict the concentrations given other parameters. Bayesian
inference requires the use of a model that is cheap in terms of
computational cost, since it would be evaluated for a large number of
points in the parameter space. Since WindTrax software is GUI driven and
computationally expensive, it does not form a good choice for use in
Bayesian inference. Therefore we fitted a function to the output of the
Windtrax (which is two dimensional array of concentrations). For a
number of different stability conditions as measured by Monin-Obukov
length, plumes for a source of unit strength over a grid were generated.
For each such plume, the parameters of the function were determined by
fitting the function to WindTrax output. In this way we built a library
of plume functions, which was an input to the Bayesian inference.

Gaussian dispersion model {#subsec:gauss}
-------------------------

Gaussian plume model [@sutton1932theory] is one of the most popular
models used for atmospheric dispersion. The concentration $C(x,y,z)$ of
a pollutant at $(x, y, z)$ is given by the equation .
$$\label{equn:gauss_plume}
  C(x,y,z) = \frac{Q}{2 \pi U \sigma_y \sigma_z} exp(-\frac{y^2}{2\sigma_y^2})\left[ exp(-\frac{(z-H)^2}{2\sigma_z^2}) + exp(-\frac{(z+H)^2}{2\sigma_z^2})\right].$$
$C(x,y,z)$ is the concentration in grams per cubic meter. $H$ is the
height of the source, $Q$ is the rate of release in grams per second,
$U$ is the wind speed in meters per second. The parameters $\sigma_y$
and $\sigma_z$ are the standard deviations of the time averaged plume
concentration in downwind and vertical directions respectively.
$\sigma_y$ and $\sigma_z$ depend on the downwind distance $x$ and
atmospheric stability class. The most common form suggested for
$\sigma_y$ and $\sigma_z$ is a power law in the downwind distance $x$:

$$\begin{aligned}
\sigma_y &= a x^b \\
\sigma_z &= c x^d.
\end{aligned}$$ 

The coefficients $a, b, c$ and $d$ have also been determined by various
researchers for the atmospheric stability classes. In situations where
the assumptions made in determining the coefficients are met, these
coefficients may be used. We have used off-the-shelf values for these parameters. These parameters have been categorized according to
the Pasquill-Gifford atmospheric classification scheme while we use
the Monin-Obhukov length to determine the atmospheric stability class
and determine the coefficients to use. Table \[table:stab\_classes\]
shows the relation between the two classification schemes. The parameters can be changed as explained in Section.

  L                                                      Stability condition   PG stability class
  --------------------- -------------------------------- --------------------- --------------------
  Very large negative   $L < -10^5$ m                    Neutral               D
  Large negative        $-10^5$ m $\leq L \leq -100$ m   Unstable              B
  Small negative        $-100$ m $< L <0$                Very unstable         A
  Small positive        $0 < L <100$ m                   Very stable           F
  Large positive        $100$ m $\leq L \leq 10^5$ m     Stable                E
  Very large positive   $L > 10^5$ m                     Neutral               D

  : Monin-Obukhov Length L with respect to atmospheric stability
  [@seinfeld2012atmospheric][]{data-label="table:stab_classes"}


Installation
=================================

Atmospheric Tomography code is available on [github](https://github.com/GeoscienceAustralia/atmospheric_tomography_laser). If you have git installed on your machine, the code can be checked out 
```
git clone https://github.com/GeoscienceAustralia/atmospheric_tomography_laser.git
```
The code can also be downloaded as a zip file from the link above. The code itself does not require any installation but you need to install Python to be able to run the code.

Dependencies
=================================

1. Python (version 3 or later)
2. PyMC

Instructions for installing PyMC are available [here](https://pymc-devs.github.io/pymc/INSTALL.html). This page also has instructions for installing the correct version of Python. Using a prebuilt distribution such as [Anaconda](http://continuum.io/downloads) is highly recommended.

Test the environment
=================================

If the installation is successful, you should be able to run Python and import the PyMC module. To test this, open the terminal utility on Mac OS X or Linux or the DOS prompt on Windows. The DOS prompt can be opened by clicking on the Windows (or Run) button on your machine and typing CMD.

On the command prompt type 
```
> python --version
```

If Python installation was successful, the command should run successfully and output the version of Python on your machine. 
```
> python --version
Python 2.7.10
>

```
If you get an error at this step, check if the PATH environment variable on your machine contains the path to python binaries. The Troubleshooting section of this manual contains more information on how to resolve this issue.

Preparing the environment
=================================

Download the source and 

Data pre-processing 
===================

The first step is to get the data in the format expected by the scripts.
The input file should be a comma separated file with the following
columns:

1.  Temperature in degree Celsius,

2.  Pressure in pascals,

3.  Wind speed in metres per second,

4.  Wind direction in degrees North of East,

5.  Monin-Obukov length in metres,

6.  Reflector id (should be an integer) and

7.  Perturbation in PPM

The order of the columns cannot be changed. However the names of the columns do not impact the execution of the scripts. 

Often the data are stored in the wide rather than the long format that is required. That is, the weather data (temperature, pressure, wind speed and direction) are recorded separately and the concentration measurements are recorded as:
```
Date, Reflector_1, Reflector_2, Reflector_3...
```

Later sections have some suggestions for reformatting the concentration data and merging the weather and concentration records.

Another consideration is that the frequency at which the weather and concentration data are recorded could be different. For instance, the meteorological data might be collected every half an hour while the concentration data could be recorded several times in a minute. In this case, we found it useful to average the concentration records to the frequency of the weather records. A script has been provided to do this and instructions for using the script are provided in a later section.  

Customizing the model parameters 
================================

The following model parameters are likely to remain unchanged across
multiple data sets, hence they are stored in the file constants.py. This file is in the directory atmospheric-tomography/src in the downloaded source code. It consists of the following key-value pairs:

1.  samples: The number of samples to be taken along the line from the laser to
    the mirror. The default value is 100. If the path is very long, you might want to increase this number to improve accuracy.$(x, y)$ Co-ordinates of the reflectors

2.  H: Height of the source $z_0$ in metres. Do not write the unit.

3.  molar_mass: Molar mass of the gas in grams per mole. Height of the reflectors $z$ in metres,

4. elevation: The height of each reflectors in meters. Notice that this is a comma-separated list in square brackets. You should enter the height of each reflector in this list, even if they are all same. So if the experiment has $n$ reflectors, this list would have $n$ numbers  

5. mirror: The $(x, y)$ co-ordinates of the mirrors. This is a comma-separated list of $(x, y)$ co-ordinates where each set of co-ordinates is written within square brackets. The number of pairs in this list should be $n$ if you have $n$ reflectors.
 
6. reflectors : The $(x, y)$ co-ordinates of the reflectors. 

To change any of these values, open the file constants.py in a text editor such as notepad and edit the values. Make sure that the editor does not introduce any formatting in the file and that the file is saved with the extension ".py". 

Modifying plume dispersion model parameters
===========================================

As mentioned in a previous (Section)[#subsec:gauss], the Gaussian plume dispersion model makes use of $4$ parameters called $a, b, c$ and $d$. The values for these parameters for each stability class are stored in the file called params.py. To change the parameters, open this file in a text editor. The relevant section is 
```
gaussian = {
'A': {'a':0.0383,'b':1.281,'c':0.495,'d':0.873},
'B': {'a':0.1393,'b':0.9467,'c':0.310,'d':0.897},
'D': {'a':0.0856,'b':0.8650,'c':0.122,'d':0.916},
'E': {'a':0.1094,'b':0.7657,'c':0.0934,'d':0.912},
'F': {'a':0.05645,'b':0.8050,'c':0.0625,'d':0.911}
}
```

You can edit these values and save the file. Make sure the file is saved with the extension ".py" as text editors usually add the extension ".txt" when a file is saved.   

Choosing a plume dispersion model
=================================

The models implemented in the software are called ‘gaussian’,
‘semi-gaussian’, ‘gauss\_poly’ and ‘gaussian2’.

Choosing a method
=================

You can choose between line average (‘line\_average’) and line integral
(‘line\_integral’).

Atmospheric Tomography Scripts
==============================
Bring up the commandline (Terminal utility on Mac and Linux, DOS prompt on Windows) and navigate to the directory in which the source code has been downloaded. For instance, on my machine, since the source code is the path /Users/sangeetabhatia/GitWorkArea/atmospheric-tomography, I run the following commands in the directory /Users/sangeetabhatia/GitWorkArea/atmospheric-tomography.  
```
> pwd
> /home/atmospheric-tomography
```

The script to be executed is src/run-tomography.py. The argument to the script is a prefix for the output files (explained below). 
```
> python src/run-tomography.py gas-long
Enter the input file name : gas.csv 
Enter the number of iterations for the MCMC simulation: 3000
Enter the burn in for the MCMC simulation: 200
Enter the thining variable for the MCMC simulation: 1
[-------------    36%                  ] 1093 of 3000 complete in 0.5 sec
[-----------------69%------            ] 2083 of 3000 complete in 1.0 sec
[-----------------100%-----------------] 3000 of 3000 complete in 1.5 sec

```

As the above output shows, the script will ask the user for a number of inputs. The first input is the name of the file that contains the data.  The file can be placed anywhere on your filesystem. Enter the full path or a path relative to the current directory. For instance, if the input file, say gas.csv,  has been placed in /home/atmospheric-tomography/data, you can enter either 
```
Enter the input file name :/home/atmospheric-tomography/data/gas.csv
```
or
```
Enter the input file name : data/gas.csv
```

The script will now ask for the following inputs: the number of iterations for the MCMC simulation, burn in and the thinning variable. The script will now execute and display the progress. At the end of the execution, three output files will be produced : summary.csv, tau.png and Q.png. These files names  will be prefixed with the argument given to the run-tomography script. So for this example, since we entered
```
> python src/run-tomography.py gas-long
```

the output files are:gas-long-summary.csv, gas-long-Q.png and gas-long-tau.png. The summary files contains the mean, credible intervals and the quantiles for the parameters Q and tau of the model.
Data cleanup and pre-analysis
=============================

R is most suited to a lot of clean up and analysis tasks needed. This
section is a compilation of some useful R commands and code snippets
that were used.

Average over a fixed time interval
----------------------------------

The first step is to average the raw data over a fixed time interval for
each reflector. This needs to be done because the frequency of the
concentration data is collected every couple of seconds, which makes for
a massive dataset. Once the relevant columns have been extracted, the python script **average\_over\_reflector.py** can be used to average over a time
interval over each reflector. Note that the column headers are hard
coded in the script. While the order does not matter, the column
containing the date should be named ‘Date’, the reflector column should
be called ‘Reflector’ and the concentration data should be present in a
column called ‘PPM’.

    python util/average_over_reflector.py 
    Please enter name of the input data file :  
    gasFinder-relevant.csv
    Please enter the start time in the format 
    DD/MM/YYYY Hour:Min:Sec AM/PM :  11/05/2015 8:00:00 AM

    Please enter the end time in the format 
    DD/MM/YYYY Hour:Min:Sec AM/PM : 18/05/2015 05:00:00 PM

    Please enter the averaging interval in minutes : 30
    Please enter the number of reflectors: 7

This script will write the output in file output.csv. The output file
should be renamed appropriately since a subsequent run of the python
script **average\_over\_reflector.py** will overwrite any file called
output.csv in the same directory.

### Calculating background concentration

      gasfinder = read.csv("data/gasFinder-averaged.csv")
      gasfinder[is.na(gasfinder)] = 0
      for(i in 1:nrow(gasfinder))
      {
       vals = gasfinder[i,2:8]
       smallest.5 = sort(vals)[1:5]
       smallest.5 = data.frame(smallest.5[,apply(smallest.5>0,2,all)])
       bg = apply(smallest.5, 1, FUN=mean)
       gasfinder$Background[i] = bg
     }

### Plotting

Plotting is best done with the R package **ggplot2**.

    library(reshape2)
    library(plyr)
    library(ggplot2)
    # Use this palette since the default palette is 
    # very poor.
    cbPalette = c("#999999", "#E69F00", "#56B4E9",   
                   "#009E73", "#F0E442", "#0072B2", 
                   "#D55E00", "#CC79A7") 
                   
    # ggplot requires data in long format. Use reshape2.
    gas.long = melt(gasfinder, id.vars = "Date")
    gas.long = rename(gas.long, c("variable"="Reflector",
                                  "value"="PPM"))

    gas.long = gas.long[gas.long$PPM>0,]
    gas.long$Reflector = factor(gas.long$Reflector)
    # Meaningful column names. Requies plyr
    gas.long = gas.long[complete.cases(gas.long),]
    p = ggplot(gas.long, aes(Date, PPM, color=Reflector)) + 
        geom_point() 
    p = p + scale_colour_manual(values=cbPalette)
    p = p + xlab("Date") + scale_x_discrete(breaks=NULL)          
    p = p + ggtitle("Averaged concentration data from 
                     11th May to 18th May")              
    p = p + theme(plot.title = element_text(lineheight=1.0, 
                                            face="bold"))       
    print(p)

Filtering out data based on time
--------------------------------

R can be used to apply a filter based on the time of day. E.g., suppose
we wish to exclude the data from 11:56 AM to 12:02 PM for 12^th^ May.

    gasfinder = read.csv("data/1105-1805-raw.csv")
    # What we would do with unix command line tools.
    gasfinder$Date = paste(gasfinder$Date, gasfinder$Hour, 
                           sep = " ")
    gasfinder$Date = strptime(gasfinder$Date, 
                              format = "%d/%m/%Y %I:%M:%S %p")
    gasfinder = gasfinder[,c(2,4,8)]
    start.high = as.POSIXct("2015-05-12 11:56:00")
    end.high = as.POSIXct("2015-05-12 12:02:00")
    first.few = gasfinder[gasfinder$Date < start.high, ]
    last.few = gasfinder[gasfinder$Date > end.high, ]
    gasfinder = rbind(first.few, last.few)
    write.csv(gasfinder, file = "1105-1805-raw-filtered.csv", 
        quote = F, row.names = F)

### Filtering out very low values

Very low concentration values can mess up the analysis. To filter out
the rows for a reflector where the concentration is smaller than the
standard deviation of data for that reflector, we can use the
split-apply-combine strategy.

      library(plyr)
      filter_sd <- function(x){return(x[x$PPM > sd(x$PPM),])}
      tmp = ddply(gas.long, .(Reflector), filter_sd)

Merging weather and concentration data
--------------------------------------

The concentration data for a time perios needs to be affixed to the
weather data for the same period. To do this read in both data sets in
the wide format and use the **merge** utility in R.

    weather = read.csv("1105-1805-weather.csv")
    tmp = merge(weather, gasfinder.wide, all.y = TRUE)

Reshaping data
--------------

### Wide to long

The python scripts for tomogrpahy need the data to be in long format.
Data can be reshaped from wide to long format using the **reshape2**
library in R.

    library(reshape2)
    # melt does not work with Date columns. 
    # We need to convert it to character.
    tmp$Date = as.character(tmp$Date)
    tmp.melt = melt(tmp, id.vars = c("Date","T","WindSpeed",
                                     "WindDirection","MO.Length"))
    # Remove rows with incomplete data.
    tmp.melt = tmp.melt[complete.cases(tmp.melt),]

### Long to wide

Troubleshooting
===============

Cannot install python or PyMC.
Make sure you have administrator priviliges.

Script cannot find module.
Edit pythonpath variable.
