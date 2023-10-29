# eBike-Route-Info-Calculator
This repository contains a program that, when given a gpx file and a dataset of the consumption rate and most efficient speed of an e-bike corresponding to specific gradients, can calculate the total energy consumed from the battery of an e-bike across a route and the total time it would take to traverse the route, assuming the battery doesn't discharge.

The purpose of this program is to give insight as to how far of a distance an e-bike could travel on a full charge. 

One single number for the range of an e-bike would not be accurate when traversing hilly terrain, so this program also considers the elevation change along a route.

The program is currently configured to extract route data from a file called route.gpx and simulation data from a file called wattage.txt.

The simulation data was obtained from https://ebikes.ca/tools/simulator2.html 

The program works in three parts.

**Part 1: Route Segmentation:**
The longitude, latitude, and elevation of each point on a gpx route are extracted. 
Then, the length and average gradient of each segment between two adjacent points are calculated.

**Part 2: Simulation Data Extraction:**
The simulation set is run with specific parameters and a changing gradient, from -30% to 30%.
The consumption rate and most efficient speed along each gradient, along with said gradient, are extracted from the data set.

**Part 3: Summations**
An average consumption rate and average speed are assigned to every segment along a route.
Then, for each segment, the total energy consumption and the time taken to cover that distance is calculated.
Then, the summations for the energy consumption and time of each segment are found, giving the total energy consumed and the total time to traverse the route.

The program asks for the voltage and amp hours of the battery that the e-bike uses.
Using this information, the capacity of the battery, in Wh, can be calculated. 
The total energy consumed is divided by the capacity of the battery to give the number of full charges the e-bike needs to traverse the route.
The program will then tell you if the e-bike can traverse the route on one full charge.

Credit for some of the methods used in Part 1 goes to Better Data Science and their Data Science for Cycling Series.
Link to their video playlist here: https://youtube.com/playlist?list=PLQ5j-FTc2VhDj93jQas0a8AvNfSMEiDxz&si=atgGAVAD4T_PM7ME 
