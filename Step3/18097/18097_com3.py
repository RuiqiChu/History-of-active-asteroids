from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from astropy.visualization import simple_norm
from photutils.aperture import CircularAperture, aperture_photometry
from matplotlib.patches import Circle

def lin_interp(x, y, i, half):
    return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))

def half_max_x(x, y):
    half = max(y)/2.0
    signs = np.sign(np.add(y, -half))
    zero_crossings = (signs[0:-2] != signs[1:-1])
    zero_crossings_i = np.where(zero_crossings)[0]
    return [lin_interp(x, y, zero_crossings_i[0], half),
            lin_interp(x, y, zero_crossings_i[1], half)]
# Open the FITS file
fits_file_path = "18097_02_intensity.fits"
hdul = fits.open(fits_file_path)

# Extract the data
data = hdul[0].data

# Close the FITS file
hdul.close()

# Define the coordinates of the region you want to zoom in
x_start, x_end, y_start, y_end = 1513, 1563, 1005, 1055

# Extract the zoomed-in region
zoomed_data = data[y_start:y_end, x_start:x_end]
zoomed_data_log = zoomed_data

# Define the center of the bright spot
center_x, center_y = (x_end - x_start) // 2, (y_end - y_start) // 2
center_position = (center_x, center_y)

# Generate apertures of radii 0.5 to 10 in steps of 0.5 and calculate mean flux
radii = np.arange(0.5, 10.5, 0.5)
mean_fluxes = []
for r in radii:
    aperture = CircularAperture(center_position, r=r)
    photometry = aperture_photometry(zoomed_data, aperture)
    area = aperture.area  # Area of the aperture
    mean_flux = photometry['aperture_sum'][0] / area  # Calculate the mean flux
    mean_fluxes.append(mean_flux)  # Append the mean flux to the list

# Sum the pixel values along the y-axis for each x-coordinate
light_profile_x = np.sum(zoomed_data, axis=0)
normalised_light_profile = light_profile_x-min(light_profile_x)

# Determine the x-coordinates for the profile
x_coords = np.arange(0, light_profile_x.shape[0])

hmx = half_max_x(x_coords,normalised_light_profile)
# print the answer
fwhm = hmx[1] - hmx[0]
print("FWHM:{:.3f}".format(fwhm))
# Display the original zoomed-in region
plt.figure(figsize=(20, 5))
plt.subplot(1, 4, 1)
plt.imshow(zoomed_data_log, cmap='viridis', origin='lower')
plt.colorbar()
plt.title("Original Zoomed data")

half = max(normalised_light_profile)/2.0
# Plot apertures on the second subplot
plt.subplot(1, 4, 2)
norm = simple_norm(zoomed_data_log, 'sqrt', percent=99)
plt.imshow(zoomed_data_log, cmap='viridis', norm=norm, origin='lower')
plt.colorbar()
plt.title("Apertures on Zoomed data")

# Plot each aperture on the image
for r in radii:
    aperture = CircularAperture(center_position, r=r)
    aperture.plot(color='white', lw=1.5)

# Adjust plot limits
plt.xlim(0, zoomed_data_log.shape[1])
plt.ylim(0, zoomed_data_log.shape[0])

# Plot the mean radial light profile on the third subplot
plt.subplot(1, 4, 3)
plt.plot(radii, mean_fluxes, 'o-', color='black')
plt.xlabel('Aperture Radius (pixels)')
plt.ylabel('Mean Flux (arbitrary units)')
plt.title('Mean Radial Light Profile')

# Plot the light profile along the x-axis on the fourth subplot
plt.subplot(1, 4, 4)
plt.plot(x_coords, normalised_light_profile, 'o-', color='blue')
plt.plot(hmx,[half,half])
plt.xlabel('Pixel Position along x-axis')
plt.ylabel('Summed Flux along y-axis')
plt.title('Light Profile along x-axis')
plt.grid(True)

# Show all the plots
plt.tight_layout()
plt.show()
