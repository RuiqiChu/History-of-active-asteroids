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
zoom_position = (1039, 1639, 588, 1188)
# Positions of the object and companion stars in the zoomed area
object_positions = (300,300,42,75,192,135,499,442)
# Positions of the object and companions stars in the original map one by one
asteroid_position = (1310, 1360, 864, 914)
companion1_position = (1055, 1105, 638, 688)
companion2_position = (1206, 1256, 698, 748)
companion3_position = (1513, 1563, 1005, 1055)

handler = DataHandler("18097_02_intensity.fits", zoom_position)  
handler.overview(object_positions,'no_log')
handler.analysis('object',asteroid_position)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position)