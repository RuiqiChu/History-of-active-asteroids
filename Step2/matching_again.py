import os
import pandas as pd
import numpy as np
import math
from astropy.time import Time
# Define the file names
file_names = [
    "Bennu_positions.txt", "Ceres_positions.txt", "Didymos_positions.txt",
    "Elst_Pizarro_positions.txt", "Gault_positions.txt", "Griseldis_positions.txt",
    "Oljato_positions.txt", "Phaethon_positions.txt", "Scheila_positions.txt",
    "Wilson_Harrington_positions.txt","lasagra.txt"
]
# Get the current working directory
current_directory = os.getcwd()

# Initialize an empty list to store the data
asteroid_list = []

def convert_date_format(date_str):
    # Define a dictionary to map month names to numbers
    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    
    parts = date_str.split('-')
    year = parts[0][-2:]  # Extract the last two digits of the year
    month = month_map[parts[1]]  # Convert month name to number
    day = parts[2]       # Day
    return f"{year}{month}{day}"

def convert_position_angle(ra_ast,dec_ast,ra_pla_rad,dec_pla_rad):
    # Convert the RA and Dec of asteroids(hhmmss.ff±ddmmss.f)
    # 1 hour = 60 minutes = 3600 seconds = pi/12 rad
    ra_ast_rad = ra_ast[0]*math.pi/12 + ra_ast[1]*math.pi/12/60 + ra_ast[2]*math.pi/12/3600
    if dec_ast[0] >= 0:
        dec_ast_rad = dec_ast[0]*math.pi/180 + dec_ast[1]*math.pi/180/60 + dec_ast[2]*math.pi/180/3600
    if dec_ast[0] < 0:
        dec_ast_rad = dec_ast[0]*math.pi/180 - dec_ast[1]*math.pi/180/60 - dec_ast[2]*math.pi/180/3600
    a = np.array([ra_pla_rad,dec_pla_rad])
    b = np.array([0,0])
    c = np.array([ra_ast_rad,dec_ast_rad])
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # Calculate the difference of position in unit of radians
    xi = (math.cos(dec_ast_rad)*math.sin(ra_ast_rad-ra_pla_rad))/cosine_angle
    eta = (math.sin(dec_ast_rad)*math.cos(dec_pla_rad)-math.cos(dec_ast_rad)*math.sin(dec_pla_rad)*math.cos(ra_ast_rad-ra_pla_rad))/cosine_angle
    return xi, eta, ra_ast_rad, ra_pla_rad, dec_ast_rad, dec_pla_rad

def radians_to_hms(angle_in_radians):
    # Convert radians to degrees
    angle_in_degrees = math.degrees(angle_in_radians)
    
    # Calculate the fractional part of a full circle
    fraction_of_circle = angle_in_degrees / 360.0
    
    # Convert the fraction to hours
    hours = int(fraction_of_circle * 24)
    
    # Calculate the remaining fraction after converting to hours
    remaining_fraction = fraction_of_circle * 24 - hours
    
    # Convert the remaining fraction to minutes
    minutes = int(remaining_fraction * 60)
    
    # Calculate the remaining fraction after converting to minutes
    remaining_fraction = remaining_fraction * 60 - minutes
    
    # Convert the remaining fraction to seconds
    seconds = int(remaining_fraction * 60)
    
    return hours, minutes, seconds

def radians_to_dms(angle_in_radians):
    # Convert radians to degrees
    angle_in_degrees = math.degrees(angle_in_radians)
    
    # Extract the whole number part as degrees
    degrees = int(angle_in_degrees)

    # Calculate the decimal part in minutes and seconds
    remaining_minutes = (angle_in_degrees - degrees) * 60
    minutes = int(remaining_minutes)
    seconds = (remaining_minutes - minutes) * 60

    return degrees, minutes, seconds
# Loop over the file names
for file_name in file_names:
    file_path = os.path.join(current_directory, file_name)
    with open(file_path, 'r') as file:
        # Read lines until the line with "$$EOE"
        lines = file.readlines()
        data_started = False  # Flag to indicate when data should be captured
        
        # Initialize a list to store the data for this file
        file_data = []
        
        for line in lines:
            if line.strip() == "$$EOE":
                break  # Stop reading when "$$EOE" is encountered
            
            if data_started:
                # Convert the date format and split the line into elements
                elements = line.strip().split()[:9]
                                # Check if element[2] is a space or a letter string
                if elements[2].isnumeric():
                    # Element[2] is a letter string, so delete it
                   pass
                else:
                    # Element[2] is not a letter string, so do nothing
                    del elements[2]
                elements[0]=convert_date_format(elements[0])
                # Combine indices 
                combined_indices = [elements[0],elements[1],elements[2],elements[3],elements[4],elements[5],elements[6],elements[7]]
                file_data.append(combined_indices)
                #print(file_data)
            if line.strip() == "$$SOE":
                data_started = True
        
        # Append the file data to the main data list
        asteroid_list.append(file_data)
asteroid_array = np.array(asteroid_list)
new_asteroid_array = []
for i in range(len(asteroid_array)):
    new_asteroid_array = new_asteroid_array + asteroid_array[i]
data=pd.read_excel('MJD_time_info.xlsx')
new_plate_array = pd.DataFrame(data).to_numpy()

#print(len(new_asteroid_array),len(new_plate_array))
#exit()
# Initialize a list to store matching information
position_info = []
# Iterate through each row in asteroid_data_df
for ID in range(len(new_asteroid_array)):
    #print(new_asteroid_array[ID],new_plate_array[ID])
    #exit()
    ra_ast = np.array([int(new_asteroid_array[ID][2]),int(new_asteroid_array[ID][3]),float(new_asteroid_array[ID][4])])
    ra_pla_rad = new_plate_array[ID][6]
    dec_ast = np.array([int(new_asteroid_array[ID][5]),int(new_asteroid_array[ID][6]),float(new_asteroid_array[ID][7])])
    dec_pla_rad = new_plate_array[ID][7]
    #print(ra_ast,ra_pla_rad,dec_ast,dec_pla_rad)
    #exit()
    xi, eta, ra_ast_rad, ra_pla_rad, dec_ast_rad, dec_pla_rad = convert_position_angle(ra_ast,dec_ast,ra_pla_rad,dec_pla_rad)
    #print(xi, eta, ra_ast_rad, ra_pla_rad, dec_ast_rad, dec_pla_rad)
    #exit()
    position_info.append({
        'Plate_ID': new_plate_array[ID][0],
        'Asteroid_ID':new_plate_array[ID][1],  
        "Date(UTC)":new_plate_array[ID][3],
        "Time(MJD)": new_plate_array[ID][4],
        "Expose time(min)":new_plate_array[ID][5],
        'RA_plate': ra_pla_rad,
        "Dec_plate": dec_pla_rad,
        "RA_asteroid": ra_ast_rad,
        "Dec_asteroid": dec_ast_rad,
        "RA_asteroid_number":radians_to_hms(ra_ast_rad),
        "Dec_asteroid_number":radians_to_dms(dec_ast_rad),
        "RA_difference(mm)":177.5-xi/0.00032550391,
        "Dec_difference(mm)":177.5+eta/0.00032550391
    })
    #print(new_plate_array[plate])
    print(position_info)
    #exit()

#print(matching_info)
# Create a DataFrame from the matching_info list
matching_info_df = pd.DataFrame(position_info)

# Save the matching information to an Excel file
matching_info_df.to_excel("matching_info.xlsx", index=False)

print("Done,bro")