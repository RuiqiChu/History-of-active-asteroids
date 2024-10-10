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
object_positions = (275,309,112,91,272,399,503,459)
# Positions of the object and companions stars in the original map one by one
asteroid_position = (1287, 1337, 875, 925)
companion1_position = (1126, 1176, 654, 704)
companion2_position = (1286, 1336, 962, 1012)
companion3_position = (1516, 1566, 1020, 1070)

handler = DataHandler("18098_02_intensity.fits", zoom_position)  
handler.overview(object_positions,'log')
handler.analysis_linear_aggresion(asteroid_position,'nolog',2000)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position,'rotation')