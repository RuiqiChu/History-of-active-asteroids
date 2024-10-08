import sys  
import os  

# Get the absolute path of the current file  
current_file_path = os.path.abspath(__file__)  

# Get the directory of the current file  
current_dir = os.path.dirname(current_file_path)  

# Get the parent directory of the current file's directory  
parent_dir = os.path.dirname(current_dir)  

# Import the main modulue
sys.path.append(parent_dir)  
from main import DataHandler


# Position of the zoomed area in the original map
zoom_position = (1200, 1400, 800, 1000)
# Positions of the object and companion stars in the zoomed area
object_positions = (107,86,30,64,151,143,22,112)
# Positions of the object and companions stars in the original map one by one
asteroid_position = (1295, 1315, 875, 895)
companion1_position = (1221, 1241, 854, 874)
companion2_position = (1341, 1361, 933, 953)
companion3_position = (1212, 1232, 902, 922)

handler = DataHandler("5215_02_intensity.fits", zoom_position)  
handler.overview(object_positions,'log')
handler.analysis_linear_aggresion(asteroid_position,'log',3.005)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position,'rotation')