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
x_start4, x_end4, y_start4, y_end4 = 1310, 1360, 864, 914
zoomed_data4 = data[y_start4:y_end4, x_start4:x_end4]

center_x4, center_y4 = (x_end4 - x_start4) // 2, (y_end4 - y_start4) // 2
center_position4 = (center_x4, center_y4)

# Generate apertures of radii 0.5 to 10 in steps of 0.5 and calculate mean flux
radii = np.arange(0.5, 10.5, 0.5)
mean_fluxes4 = []
for r in radii:
    aperture4 = CircularAperture(center_position4, r=r)
    photometry4 = aperture_photometry(zoomed_data4, aperture4)
    area4 = aperture4.area  # Area of the aperture
    mean_flux4 = photometry4['aperture_sum'][0] / area4  # Calculate the mean flux
    mean_fluxes4.append(mean_flux4)  # Append the mean flux to the list

# Measure the Light Profile
reduced_mean_flux4 = mean_fluxes4-min(mean_fluxes4)

# Calculate the normalized light profile for the fourth region
factor = np.max(reduced_mean_flux4)
x_coords4 = np.arange(0, reduced_mean_flux4.shape[0])

# Define the coordinates of the region you want to zoom in
x_start1, x_end1, y_start1, y_end1 = 1055, 1105, 638, 688
x_start2, x_end2, y_start2, y_end2 = 1206, 1256, 698, 748
x_start3, x_end3, y_start3, y_end3 = 1513, 1563, 1005, 1055



# Extract the zoomed-in region
zoomed_data1 = data[y_start1:y_end1, x_start1:x_end1]
zoomed_data2 = data[y_start2:y_end2, x_start2:x_end2]
zoomed_data3 = data[y_start3:y_end3, x_start3:x_end3]

center_x1, center_y1 = (x_end1 - x_start1) // 2, (y_end1 - y_start1) // 2
center_position1 = (center_x1, center_y1)

# Generate apertures of radii 0.5 to 10 in steps of 0.5 and calculate mean flux
radii = np.arange(0.5, 10.5, 0.5)
mean_fluxes1 = []
for r in radii:
    aperture1 = CircularAperture(center_position1, r=r)
    photometry1 = aperture_photometry(zoomed_data1, aperture1)
    area1 = aperture1.area  # Area of the aperture
    mean_flux1 = photometry1['aperture_sum'][0] / area1 # Calculate the mean flux
    mean_fluxes1.append(mean_flux1)  # Append the mean flux to the list

# Measure the Light Profile
reduced_mean_flux1 = mean_fluxes1-min(mean_fluxes1)
peak_flux1 = np.max(reduced_mean_flux1)
normalization_factor1 = factor / peak_flux1
normalized_flux1 = reduced_mean_flux1 * normalization_factor1
x_coords1 = np.arange(0, reduced_mean_flux1.shape[0])

center_x2, center_y2 = (x_end2 - x_start2) // 2, (y_end2 - y_start2) // 2
center_position2 = (center_x2, center_y2)

# Generate apertures of radii 0.5 to 10 in steps of 0.5 and calculate mean flux
radii = np.arange(0.5, 10.5, 0.5)
mean_fluxes2 = []
for r in radii:
    aperture2 = CircularAperture(center_position2, r=r)
    photometry2 = aperture_photometry(zoomed_data2, aperture2)
    area2 = aperture2.area  # Area of the aperture
    mean_flux2 = photometry2['aperture_sum'][0] / area2  # Calculate the mean flux
    mean_fluxes2.append(mean_flux2)  # Append the mean flux to the list

# Measure the Light Profile
reduced_mean_flux2 = mean_fluxes2-min(mean_fluxes2)
peak_flux2 = np.max(reduced_mean_flux2)
normalization_factor2 = factor / peak_flux2
normalized_flux2 = reduced_mean_flux2 * normalization_factor2
x_coords2 = np.arange(0, reduced_mean_flux2.shape[0])

center_x3, center_y3 = (x_end3 - x_start3) // 2, (y_end3 - y_start3) // 2
center_position3 = (center_x3, center_y3)

# Generate apertures of radii 0.5 to 10 in steps of 0.5 and calculate mean flux
radii = np.arange(0.5, 10.5, 0.5)
mean_fluxes3 = []
for r in radii:
    aperture3 = CircularAperture(center_position3, r=r)
    photometry3 = aperture_photometry(zoomed_data3, aperture3)
    area3 = aperture3.area  # Area of the aperture
    mean_flux3 = photometry3['aperture_sum'][0] / area3  # Calculate the mean flux
    mean_fluxes3.append(mean_flux3)  # Append the mean flux to the list

# Measure the Light Profile
reduced_mean_flux3 = mean_fluxes3-min(mean_fluxes3)
peak_flux3 = np.max(reduced_mean_flux3)
normalization_factor3 = factor / peak_flux3
normalized_flux3 = reduced_mean_flux3 * normalization_factor3
x_coords3 = np.arange(0, reduced_mean_flux3.shape[0])

# Now create a plot to compare all four light profiles
plt.figure(figsize=(10, 5))
plt.plot(x_coords1, normalized_flux1, 'o-', color='blue', label='Companion 1')
plt.plot(x_coords2, normalized_flux2, 's-', color='red', label='Companion 2')
plt.plot(x_coords3, normalized_flux3, '^-', color='green', label='Companion 3')
plt.plot(x_coords4, reduced_mean_flux4, 'd-', color='purple', label='Object')
plt.xlabel('Pixel Position along x-axis')
plt.ylabel('Summed Flux along y-axis')
plt.title('Comparative Light Profiles along x-axis')
plt.legend()
plt.grid(True)
plt.show()
