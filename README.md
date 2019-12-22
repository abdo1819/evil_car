# car self reporting for trafic violation:

## overview
instead of fixed point as traffic man or lidar for detectinng trafic violation we will be using in car sensors or planting others like cameras or gps module

## use case:
1. for speed violation a computer placed in car -raspberry for out prototype- will connect to car obd to read the car speed  ,same time it will retrive the speed limit from the server , if the car passed the limit for extended period it will report it to server

2. for one way road if car_2 happen to pass car_1 from the coming diraction a camera 
placed in car_1 can detect it and report the violation for car car_2

## for communication methods :
1. fixed point in the road entry were information exchange occur the 
	* the car send any violation 
	* the point update the road roles
2. gsm communication were car gets continuse updates and report any violation


