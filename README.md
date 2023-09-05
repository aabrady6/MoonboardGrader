# MoonboardGrader

## Overview

Bouldering is a physically demanding sport, that relies on the categorization of climbing routes into various difficulty levels. However, the process of grading rock climbing routes is inherently subjective and can vary significantly based on factors such as the climber's experience, the specific climbing holds, and routes. This subjectivity poses challenges for route setters aiming to accurately convey the nature of the climb to the climbing community. 

One tool which removes some variability of the sport's factors is The Moonboard (https://www.moonboard.com) training device. The Moonboard can provide a standardized framework to evaluate the multifaceted aspects that contribute to a route's difficulty. Factors such as hold types, overhang angles, and route length can be quantified and integrated into a comprehensive equation.The standardized holds aid in creating a large dataset which can be used for analysis.

This program can be used to mathematically calculate a route on the Moonboard Masters 2019 hold set. The challenge I faced with this project involves the redesign of the Moonboard website, now focussing on an app-first approach. The limited data that is provided on the Moonboard website affects the training data size and causes some inaccuracies in unrealistic problems.

## Key Topics
* [Prerequisites](#Prerequisites)
  * [Python3 packages](#python3-packages)
  * [Firefox](#firefox)
* [Using the Project](#using-the-project)  
  *  [Obtaining data to train the nueral network](#obtaining-data-to-train-the-nueral-network)
  *  [Create and train the nueral network](#create-and-train-the-nueral-network)
  *  [Testing a route's grade](#testing-a-route's-grade)
* [Future Improvements](#future-improvements) 


## Prerequisites
### Python3 Packages
Python3 and Jupyter notebooks are required to run this project. The required packages are:
* selenium
* requests_html
* numpy
* tensorflow

To install these packages, use the following commands:

```
pip install -U selenium
pip install requests_html
pip install numpy
pip install tensorflow==2.13.*
```

if package installations experience issues, reffer to that package's web documentation.

### Firefox
This project uses Firefox as the web driver for Selenium. Ensure the latest version is installed. If an error occurs when running Selenium, visit https://github.com/mozilla/geckodriver/releases to get the most recent geckodriver and replace the current driver uploaded in Web Scraper/Drivers.

## Using the Project
### Obtaining data to train the nueral network
To begin, the raw data will need to be extracted from the Moonboard webpage. Create an account on the Moonboard website and enter the username and password into the Web Scraper/user_info.txt file. Next, enter into the Web Scraper/scraper_driver.ipynb file and run all blocks. This will use the Selenium package to open a Firefox instance and automatically log into the Moonboard website. Once logged in, Selenium will change the board type to Moonboard Masters 2019 and will extract the URLs of the 438 benchmark problems. Once extracted, the browser will close.

The next step extracts the legal holds, starting hold(s), ending hold(s) and grade for each of the routes. This step visits each of the scraped URLs and takes approximtely 1-2 seconds per page, so takes estimated 10 mins to complete. Future opportunity to look into asyncronously request the data to significantly speed up this step. Once complete, the raw data will then be housed in the Raw Data folder.

### Create and train the Nueral Network
Navigate to the driver notebook file for the nueral network (TF/Conversion Driver.ipynb). The first step is to convert the raw data to useable tensors. This project creates a 3 dimensional tensor for each project, with the legal holds on one layer, the start hold(s) on the second and the finish hold(s) on the third layer. Next, these tensors will be used to create and train the model with the TensorFlow package. Once complete, we will be able to test the grade of a hypothetical problem.

### Testing a route's grade
Enter into the TF Data/Test Problem.txt file. The file contains an 11x18 matrix. Tho set a route, change the starting hold(s) from 0 -> S. Change legal holds from 0 -> 1. Change the finish holds from 0 -> F. Once saved, run the final block in the TF/Conversion Driver.ipynb. The resulted calculated grade will be printed.

## Future Improvements
The following are future improvements for this project:
* using async to scrape hold position data quicker
* create a UI for inputting test routes
