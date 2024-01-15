from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from scipy.ndimage import rotate
from matplotlib.patches import Circle

# Open the FITS file
fits_file_path = "18097_02_intensity.fits"
hdul = fits.open(fits_file_path)

# Extract the data
data = hdul[0].data

# Close the FITS file
hdul.close()

# Define the coordinates of the region you want to zoom in
x_start, x_end, y_start, y_end = 1039, 1639, 588, 1188
x_start_test, x_end_test, y_start_test, y_end_test = 1039, 1639, 588, 1188

# Extract the zoomed-in region
zoomed_data = data[y_start:y_end, x_start:x_end]
zoomed_data_log = zoomed_data

# Display the original, rotated region, and light profile side by side
plt.figure(figsize=(7, 7))

# Display the zoomed-in region
plt.imshow(zoomed_data, cmap='viridis')

# Draw the red circle for Object
object_circle1 = Circle((1339 - x_start_test, 888 - y_start_test), 20, color='red', fill=False)
plt.gca().add_patch(object_circle1)
# Label Companion 1
plt.text(1339 - x_start_test, 888 - y_start_test + 30, 'Object', color='red', ha='center')

# Draw the red circle for Companion 1
companion_circle1 = Circle((1081 - x_start_test, 663 - y_start_test), 10, color='red', fill=False)
plt.gca().add_patch(companion_circle1)
# Label Companion 1
plt.text(1081 - x_start_test, 663 - y_start_test + 15, 'Companion 1', color='red', ha='center')

# Draw the red circle for Companion 2
companion_circle2 = Circle((1231 - x_start_test, 723 - y_start_test), 10, color='red', fill=False)
plt.gca().add_patch(companion_circle2)
# Label Companion 2
plt.text(1231 - x_start_test, 723 - y_start_test + 15, 'Companion 2', color='red', ha='center')

# Draw the red circle for Companion 3
companion_circle3 = Circle((1538 - x_start_test, 1030 - y_start_test), 10, color='red', fill=False)
plt.gca().add_patch(companion_circle3)
# Label Companion 3
plt.text(1538 - x_start_test, 1030 - y_start_test + 15, 'Companion 3', color='red', ha='center')
plt.colorbar()
plt.title("Original Zoomed data")

plt.tight_layout()
plt.show()
