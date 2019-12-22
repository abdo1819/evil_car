# car self reporting for trafic violation:

## overview
instead of fixed point as traffic man or lidar for detectinng trafic violation we will be using in car sensors or planting others like cameras or gps module for detecting various vilations

## use case:
1. for speed violation a computer placed in car -raspberry for out prototype- will connect to car obd to read the car speed  ,same time it will retrive the speed limit from the server , if the car passed the limit for extended period it will report it to server

2. for one way road if car_2 happen to pass car_1 from the coming diraction a camera 
placed in car_1 can detect it and report the violation for car car_2

## for communication methods :
1. fixed point in the road entry were information exchange occur the 
	* the car send any violation 
	* the point update the road roles
2. gsm communication were car gets continuse updates and report any violation


## prototype _ideas_:
1. a respery pi witch read the data from car using obd then transmiting using wifi to computer server
2. maquette of rouad with two _traffic sign plate_ as server and car . at the route start the car recive the speed limit from first plate,
at the road end the car report if it has passed the speed and get the new speed
