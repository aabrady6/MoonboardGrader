# MoonboardGrader

## Overview

Bouldering is a physically demanding sport, that relies on the categorization of climbing routes into various difficulty levels. However, the process of grading rock climbing routes is inherently subjective and can vary significantly based on factors such as the climber's experience, the specific climbing holds, and routes. This subjectivity poses challenges for route setters aiming to accurately convey the nature of the climb to the climbing community. 

One tool which removes some variability of the sport's factors is The Moonboard (https://www.moonboard.com) training device. The Moonboard can provide a standardized framework to evaluate the multifaceted aspects that contribute to a route's difficulty. Factors such as hold types, overhang angles, and route length can be quantified and integrated into a comprehensive equation.The standardized holds aid in creating a large dataset which can be used for analysis.

This program can be used to mathematically calculate a route on the Moonboard Masters 2019 hold set. The challenge I faced with this project involves the redesign of the Moonboard website, now focussing on an app-first approach. The limited data that is provided on the Moonboard website affects the training data size and causes some inaccuracies in unrealistic problems.

## Key Topics
* [Prerequisites](#Prerequisites)
  * [Python3 packages](#python3-packages)
  * Firefox (version 
* [Using the Project](#using-the-project)  
  *  Obtaining data to train the nueral network
  *  Create and train the nueral network
  *  Testing a route's grade


## Prerequisites
### Python3 Packages
Python3 and Jupyter notebooks are required to run this project. The required packages are:
* selenium
* numpy
* tensorflow

To install these packages, use the following commands:

```
pip install -U selenium
pip install numpy
pip install tensorflow==2.13.*
```

if package installations experience issues, reffer to that package's web documentation.

## Using the Project
### Obtaining data to train the nueral network
To begin, the raw data will need to be extracted from the Moonboard webpage. Create an account on the Moonboard website and enter the username and password into the Web Scraper/user_info.txt file. Next, enter into the Web Scraper/scraper_driver.ipynb file and run all blocks. This will use the Selenium package to open a 
