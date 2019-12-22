# car self reporting for trafic violation:

> project state : under decision

## overview
instead of fixed point as traffic man or lidar for detectinng trafic violation we will be using in car sensors or planting others like cameras or gps module for detecting various vilations

## use case:
1. for speed violation a computer placed in car -raspberry for our prototype- will connect to car obd to read the car speed  ,same time it will retrive the speed limit from the server , if the car passed the limit for extended period it will report it to server

2. for one way road if car_2 happen to pass car_1 from the coming diraction a camera 
placed in car_1 can detect it and report the violation for car car_2

~~3. reporting a problem in road like hole or open side .. etc~~
> seems prety hard for fast cars [roadai](https://www.vaisala.com/en/blog/2019-09/how-road-condition-analysis-computer-vision-changing-cities-and-transportation-departments) i think we still can propose it


## for communication methods :
~~1. fixed point in the road entry were information exchange occur the 
	* the car send any violation 
	* the point update the road roles~~
>we will not use v2x communication we only regulate human behavior with low cost unreliable device can be placed in car without the mad security concern or low latency war [why_not_DSRC](https://hackaday.com/2019/02/21/when-will-our-cars-finally-speak-the-same-language-dsrc-for-vehicles/) 


2. gsm celular communication where car gets continuse updates and report any violation

3. wifi bse station for car to report 

## prototype _ideas_:
1. a respery pi witch read the data from car using obd then transmiting using wifi to computer server
~~2. maquette of road with two _traffic sign plate_ as server and car . at the route start the car recive the speed limit from first plate,
at the road end the car report if it has passed the speed and get the new speed~~
> we use celular data / wifi

3. maquette of road where car will pass certain speed and report it when connecting to wifi network at road stop


## final version _concept_
a camera placed in front of car like dvr with inboard computer, gps, ultrasonic 
the model would be able to 
* find visaul detectable violations like wrong passing or turn checking ..etc
* speed violation with gps 
~~* space from front car with ultrasonic ~~
> seems unreliable and hard to use
