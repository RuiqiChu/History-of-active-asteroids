# The aim of these codes in step1:
# 1. Manage the plates information, read and select needed data, which are time, position and ID.
# 2. From HORIZON system generated the ephemeris of several objects that we are interested in during the time period of plates, read the needed information, time and position from the ephemris and saved in an array
# 3. Compare the data of asteroids and plates, find the plates with asteroids information of the same date and similar location (less than 0.05rad in both RA and Dec from the center of the plate), date in converted to MJD and the calculation of position is based on the local plane coordinates, output the information of the plate and asteroid to matching_info.xlsx, including ID of the plate, ID of the asteroid, Date in MJD,LST of start of exposure, RA of the center of the plate in radians, Dec of the center of the plate, RA of the asteroid, Dec of the asteroid, difference in RA and Dec of asteroid and plate in mm shown on the plate.

# To run:

python matching.python

# This will generate a .xlsx file names matching_info.xlsx which contains the matching information
# ID of object would be the order of position files loaded into the code, similarly, to modify the objects checked, 
# change the input 'file_names' from line 7

# Then

python MJD_convert.py

# This will generate a file called MJD_time_info.xlsx which gives the precise mid-exposure time of 
# each interested plates in MJD

# For next step, copy the MJD_time_info.xlsx file to the other folder for step2
