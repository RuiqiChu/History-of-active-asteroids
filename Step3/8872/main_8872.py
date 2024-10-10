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
zoom_position = (1000, 1600, 600, 1200)
# Positions of the object and companion stars in the zoomed area
object_positions = (332,305,185,167,344,132,437,530)
# Positions of the object and companions stars in the original map one by one
asteroid_position = (1315, 1365, 876, 926)
companion1_position = (1160, 1210, 742, 792)
companion2_position = (1319, 1369, 707, 757)
companion3_position = (1412, 1462, 1105, 1155)

handler = DataHandler("8872_Scheila_02_intensity.fits", zoom_position)  
handler.overview(object_positions,'nolog')
handler.analysis_linear_aggresion(asteroid_position,'nolog',5000)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position,'rotation')