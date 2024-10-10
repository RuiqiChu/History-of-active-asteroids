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
zoom_position = (861,1461,688,1288)
# Positions of the object and companion stars in the zoomed area
object_positions = (300,300,298,85,114,269,494,182)
# Positions of the object and companions stars in the original map one by one
asteroid_position = (1149,1199,963,1013)
companion1_position = (1132, 1182, 748, 798)
companion2_position = (948, 998, 930, 980)
companion3_position = (1328, 1378, 845, 895)

handler = DataHandler("19228_02_intensity.fits", zoom_position)  
handler.overview(object_positions,'log')
handler.analysis_linear_aggresion(asteroid_position,'log',3)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position,'rotation')