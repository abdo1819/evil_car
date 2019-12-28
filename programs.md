# lane detection
  - detect sepration line
  - find car current lane
  - [get road info from maps](#get-road-speed-limit)
  - classify lanes where we can and where cannot go based on traffic rules
  - if went to wrong lane report


# get road speed limit 
1. easy may not work in egpyt
  - use googlemaps api
    1. get nearest road (nearest)[https://developers.google.com/maps/documentation/roads/nearest]
    2. get speed limit (limit)[https://developers.google.com/maps/documentation/roads/speed-limits]

2. harder not  much reliable
  - use opencv
    1. detect Road Plates
    2. identify speed Plates
    3. read numbers
    
# get current speed 
  1. hard way
    * dirty implemtaion 
      - use gps module to get location
      - calculate speed from distance and time 
      - find accuracy of reading

  2. easy way
    - use android things 
      1. build/find driver for gps module
      2. use sdk to get speed accyracy the speed [andriond.loaction](https://developer.android.com/reference/android/location/Location.html#getSpeed())



# refrance :
[same project some ideas](https://www.raspberrypi.org/forums/viewtopic.php?t=212407)
