from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from scipy.ndimage import rotate

# Open the FITS file
fits_file_path = "18097_02_intensity.fits"
hdul = fits.open(fits_file_path)

# Extract the data
data = hdul[0].data

# Close the FITS file
hdul.close()

# Define the coordinates of the region you want to zoom in
x_start, x_end, y_start, y_end = 1289, 1389, 838, 938

# Extract the zoomed-in region
zoomed_data = data[y_start:y_end, x_start:x_end]


# Measure the Light Profile
light_profile = np.sum(zoomed_data, axis=0)

# Display the original, rotated region, and light profile side by side
plt.figure(figsize=(10, 5))

# Display the zoomed-in region
plt.subplot(1, 2, 1)
plt.imshow(zoomed_data, cmap='viridis')
plt.colorbar()
plt.title("Original Zoomed data")


# Display the light profile
plt.subplot(1, 2, 2)
plt.plot(light_profile)
plt.title('Light Profile of the Trail')
plt.xlabel('Pixel Position Along X-axis')
plt.ylabel('Summed Intensity')

plt.tight_layout()
plt.show()
