import os
import pandas as pd
import numpy as np
import math
from astropy.time import Time
# Define the file names
file_names = [
    "Bennu_positions.txt", "Ceres_positions.txt", "Didymos_positions.txt",
    "Elst-Pizarro_positions.txt", "Gault_positions.txt", "Griseldis_positions.txt",
    "Oljato_positions.txt", "Phaethon_positions.txt", "Scheila_positions.txt",
    "Wilson-Harrington_positions.txt","233P_la_sagra_positions.txt"
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

def convert_position_angle(ra_ast,dec_ast,ra_pla,dec_pla):
    # Convert the RA and Dec of asteroids(hhmmss.ff±ddmmss.f) and plate(hhmmt±ddmm) to radians
    # 1 hour = 60 minutes = 3600 seconds = pi/12 rad
    ra_ast_rad = ra_ast[0]*math.pi/12 + ra_ast[1]*math.pi/12/60 + ra_ast[2]*math.pi/12/3600
    ra_pla_rad = ra_pla[0]*math.pi/12 + ra_pla[1]*math.pi/12/60 + ra_pla[2]*math.pi*6/12/3600
    if dec_ast[0] >= 0:
        dec_ast_rad = dec_ast[0]*math.pi/180 + dec_ast[1]*math.pi/180/60 + dec_ast[2]*math.pi/180/3600
    if dec_ast[0] < 0:
        dec_ast_rad = dec_ast[0]*math.pi/180 - dec_ast[1]*math.pi/180/60 - dec_ast[2]*math.pi/180/3600
    if dec_pla[0] >= 0:
        dec_pla_rad = dec_pla[0]*math.pi/180 + dec_pla[1]*math.pi/180/60
    if dec_pla[0] < 0:
        dec_pla_rad = dec_pla[0]*math.pi/180 - dec_pla[1]*math.pi/180/60
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
                if elements[2].isalpha():
                    # Element[2] is a letter string, so delete it
                   del elements[2]
                else:
                    # Element[2] is not a letter string, so do nothing
                    pass
                elements[0]=convert_date_format(elements[0])
                # Combine indices 
                combined_indices = [elements[0],elements[1],elements[2],elements[3],elements[4],elements[5],elements[6],elements[7]]
                file_data.append(combined_indices)
            if line.strip() == "$$SOE":
                data_started = True
        
        # Append the file data to the main data list
        asteroid_list.append(file_data)
asteroid_array = np.array(asteroid_list)

# Define the file path
file_path = 'catlog_ukstu.lis'

# Initialize an empty list to store the data
plate_list = []

# Read the .lis file line by line
with open(file_path, 'r') as file:
    for line in file:
        plate_list.append(list(line))

# Define the sub-element indices in the original line
sub_element_indices = [(2, 7),(20, 22),(22,24),(24,25),(25,28),(28,30),(30,36),(36, 40), (52, 56)]

# Initialize an empty list to store the new data
new_plate_list = []

# Iterate through the plate_list and extract sub-elements based on the indices
for line in plate_list:
    new_line = []
    for start, end in sub_element_indices:
        if start is None:
            new_element = ""
        else:
            new_element = "".join(line[start:end])
        new_line.append(new_element)
    new_plate_list.append(new_line)

# Convert the new_plate_list into a NumPy array
new_plate_array = np.array(new_plate_list)

# Initialize a list to store matching information
matching_info = []
# Iterate through each row in asteroid_data_df
for ID in range(len(asteroid_array)):
    for Date_index in range(len(asteroid_array[ID])):
        for plate in range(len(new_plate_array)):
            Date = (asteroid_array[ID][Date_index][0])          # Check for same date
            if Date == (new_plate_array[plate][6]):
                # Two conditions for anti-star cases in RA and Dec directions
                if ((int(asteroid_array[ID][Date_index][5]) >= 0 and int(new_plate_array[plate][4]) >= 0) or 
                (int(asteroid_array[ID][Date_index][5]) < 0 and int(new_plate_array[plate][4]) < 0)):
                    ra_ast = np.array([int(asteroid_array[ID][Date_index][2]),int(asteroid_array[ID][Date_index][3]),float(asteroid_array[ID][Date_index][4])])
                    ra_pla = np.array([int(new_plate_array[plate][1]),int(new_plate_array[plate][2]),int(new_plate_array[plate][3])])
                    dec_ast = np.array([int(asteroid_array[ID][Date_index][5]),int(asteroid_array[ID][Date_index][6]),float(asteroid_array[ID][Date_index][7])])
                    dec_pla = np.array([int(new_plate_array[plate][4]),int(new_plate_array[plate][5])])
                    xi, eta, ra_ast_rad, ra_pla_rad, dec_ast_rad, dec_pla_rad = convert_position_angle(ra_ast,dec_ast,ra_pla,dec_pla)
                    date_yymmdd = Date  # Example: September 24, 2023

                    # Construct a string in the '20YY-MM-DD'/'19YY-MM-DD' format from the YYMMDD input
                    if int(date_yymmdd[:2])>50:
                        date_iso = f'19{date_yymmdd[:2]}-{date_yymmdd[2:4]}-{date_yymmdd[4:6]}'
                    else:
                        date_iso = f'20{date_yymmdd[:2]}-{date_yymmdd[2:4]}-{date_yymmdd[4:6]}'

                    # Create a Time object from the ISO formatted date
                    time_obj = Time(date_iso, format='iso')

                    # Get the Modified Julian Day (MJD) from the Time object
                    mjd = time_obj.mjd
                    time = new_plate_array[plate][7]
                    if abs(xi) < 0.05 and abs(eta) < 0.05:
                        matching_info.append({
                            'Plate_ID': new_plate_array[plate][0],
                            'Asteroid_ID':ID+1,  # Index represents the ID of the asteroid
                            'Date(MJD)': mjd,
                            "Date(UTC)":Date,
                            "Time": time,
                            "Expose time(min)":new_plate_array[plate][8],
                            'RA_plate': ra_pla_rad,
                            "Dec_plate": dec_pla_rad,
                            "RA_asteroid": ra_ast_rad,
                            "Dec_asteroid": dec_ast_rad,
                        })
                        
# Create a DataFrame from the matching_info list
matching_info_df = pd.DataFrame(matching_info)

# Save the matching information to an Excel file
matching_info_df.to_excel("matching_info.xlsx", index=False)

print("Done,bro")