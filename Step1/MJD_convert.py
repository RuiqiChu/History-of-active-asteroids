import os
import pandas as pd
import numpy as np
import math

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

# Convert from local siderial time to modified julian dates, method from 'Practical astronomy with your calculator or spreadsheet'
def LST_to_MJD(mjd,lst,expose_time,longitude):
    jd = mjd + 2400000.5
    S = jd - 2451545
    T = S / 36525
    i = 0
    if 6.697374558 + (2400.051336*T)+(0.000025862*T*T) < 0:
        while ((6.697374558 + (2400.051336*T)+(0.000025862*T*T)+24*i)<0 or (6.697374558 + (2400.051336*T)+(0.000025862*T*T)+24*i)>24):
            i += 1
    else:
        while ((6.697374558 + (2400.051336*T)+(0.000025862*T*T)+24*i)<0 or (6.697374558 + (2400.051336*T)+(0.000025862*T*T)+24*i)>24):
            i -= 1
    T0 = 6.697374558 + (2400.051336*T)+(0.000025862*T*T)+24*i
    LST = (float((str(lst))[:-2])+(int(str(lst)[-2:])/60))+expose_time/60/2 # convert LST to mid-expose time in decimal hours
    GST = LST-longitude/15
    i = 0
    if GST - T0 >0 and GST - T0 <24:
        B = GST - T0
    elif GST - T0 >0:
        while(GST - T0 - 24*i > 0):
            i += 1
        B = GST - T0 - 24*i
    else:
        while(GST - T0 + 24*i < 0):
            i += 1
    UT = B * 0.9972695663
    MJD = mjd+float(UT/24)
    return MJD

data=pd.read_excel('matching_info.xlsx',converters={'Time': str}) # Avoid ignoring leading zeros
array = pd.DataFrame(data).to_numpy()
longitude = 149.07111 # Lognitude in degrees of Siding Spring Observatory, E
# Initialize a list to store matching information
matching_info = []
for i in range(len(array)):
    print(array[i])
    MJD = LST_to_MJD(array[i][2],array[i][4],array[i][5]/10,longitude)
    matching_info.append({
                            'Plate_ID': array[i][0],
                            'Asteroid_ID':array[i][1],  # Index represents the ID of the asteroid
                            'Date(MJD)': array[i][2],
                            "Date(UTC)":array[i][3],
                            "Mid-expose time(MJD)": MJD,
                            "Expose time(mmmt)":array[i][5],
                            'RA_plate': array[i][6],
                            "Dec_plate": array[i][7],
                        })
# Create a DataFrame from the matching_info list
matching_info_df = pd.DataFrame(matching_info)

# Save the matching information to an Excel file
matching_info_df.to_excel("MJD_time_info.xlsx", index=False)

print("Done,bro")