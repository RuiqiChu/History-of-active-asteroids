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
zoom_position = (1133, 1533, 747, 1147)
# Positions of the object and companion stars in the zoomed area
object_positions = (200,200,73,226,197,250,259,270)
# Positions of the object and companions stars in the original map one by one
asteroid_position = (1320, 1350, 934, 964)
companion1_position = (1191, 1221, 958, 988)
companion2_position = (1314, 1344, 978, 1008)
companion3_position = (1375, 1405, 1001, 1031)

handler = DataHandler("14099_02_intensity.fits", zoom_position)  
handler.overview(object_positions,'log')
handler.analysis_linear_aggresion(asteroid_position,'log',3.09)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position,'rotation')