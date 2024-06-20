from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import simple_norm
from photutils.aperture import CircularAperture, aperture_photometry
from matplotlib.patches import Circle
from scipy.stats import linregress
from scipy.ndimage import rotate
# Open the FITS file
fits_file_path = "18097_02_intensity.fits"
hdul = fits.open(fits_file_path)

# Extract the data
data = hdul[0].data

# Close the FITS file
hdul.close()

# Extract the zoomed-in region for the fourth set of coordinates
x_start4, x_end4, y_start4, y_end4 = 1310,1360,863,913
zoomed_data4 = data[y_start4:y_end4, x_start4:x_end4]

# Calculate the normalized light profile for the fourth region
light_profile_x4 = np.sum(zoomed_data4, axis=0)
reduced_light_x4 = light_profile_x4-min(light_profile_x4)
factor = np.max(reduced_light_x4)
x_coords4 = np.arange(0, light_profile_x4.shape[0])

# Define the coordinates of the region you want to zoom in
x_start1, x_end1, y_start1, y_end1 = 1056, 1106, 638, 688
x_start2, x_end2, y_start2, y_end2 = 1206, 1256, 698, 748
x_start3, x_end3, y_start3, y_end3 = 1513, 1563, 1005, 1055



# Extract the zoomed-in region
zoomed_data1 = data[y_start1:y_end1, x_start1:x_end1]
zoomed_data2 = data[y_start2:y_end2, x_start2:x_end2]
zoomed_data3 = data[y_start3:y_end3, x_start3:x_end3]


# Sum the pixel values along the y-axis for each x-coordinate
light_profile_x1 = np.sum(zoomed_data1, axis=0)
reduced_light_x1 = light_profile_x1-min(light_profile_x1)

# Determine the normalization factor to scale the peak to 346441
peak_flux1 = np.max(reduced_light_x1)
normalization_factor1 = factor / peak_flux1

# Normalize the light profile along the x-axis
normalized_light_profile_x1 = reduced_light_x1 * normalization_factor1

# Determine the x-coordinates for the profile
x_coords1 = np.arange(0, light_profile_x1.shape[0])

# Calculate the normalized light profile for the second region
light_profile_x2 = np.sum(zoomed_data2, axis=0)
reduced_light_x2 = light_profile_x2-min(light_profile_x2)
peak_flux2 = np.max(reduced_light_x2)
normalization_factor2 = factor / peak_flux2
normalized_light_profile_x2 = reduced_light_x2 * normalization_factor2
x_coords2 = np.arange(0, light_profile_x2.shape[0])

# Calculate the normalized light profile for the third region
light_profile_x3 = np.sum(zoomed_data3, axis=0)
reduced_light_x3 = light_profile_x3-min(light_profile_x3)
peak_flux3 = np.max(reduced_light_x3)
normalization_factor3 = factor / peak_flux3
normalized_light_profile_x3 = reduced_light_x3 * normalization_factor3
x_coords3 = np.arange(0, light_profile_x3.shape[0])



# Now create a plot to compare all four light profiles
plt.figure(figsize=(10, 5))
plt.plot(x_coords1, normalized_light_profile_x1, 'o-', color='blue', label='Companion 1')
plt.plot(x_coords2, normalized_light_profile_x2, 's-', color='red', label='Companion 2')
plt.plot(x_coords3, normalized_light_profile_x3, '^-', color='green', label='Companion 3')
plt.plot(x_coords4, reduced_light_x4, 'd-', color='purple', label='Object')
plt.xlabel('Pixel Position along x-axis')
plt.ylabel('Summed Flux along y-axis')
plt.title('Comparative Light Profiles along x-axis')
plt.legend()
plt.grid(True)
plt.show()
