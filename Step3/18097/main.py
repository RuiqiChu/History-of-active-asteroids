from astropy.io import fits  
import matplotlib.pyplot as plt  
from matplotlib.patches import Circle  
import numpy as np
from astropy.visualization import simple_norm
from photutils.aperture import CircularAperture, aperture_photometry

class DataHandler:  
  
    def __init__(self, file_path, zoomed_position):  
        self.file_path = file_path  
        self.x_start = zoomed_position[0]  
        self.x_end = zoomed_position[1]  
        self.y_start = zoomed_position[2]    
        self.y_end = zoomed_position[3]    
        self.index = str(self.file_path).split("_")[0]  
        # Open the FITS file and extract the data  
        try:  
            with fits.open(self.file_path) as hdul:  
                self.data = hdul[0].data  
        except FileNotFoundError:  
            print(f"File {self.file_path} not found.")  
            self.data = None  
        except Exception as e:  
            print(f"Error reading FITS file: {e}")  
            self.data = None  
    def lin_interp(self,x, y, i, half):
        return x[i] + (x[i+1] - x[i]) * ((half - y[i]) / (y[i+1] - y[i]))

    def half_max_x(self,x, y):
        half = max(y)/2.0
        signs = np.sign(np.add(y, -half))
        zero_crossings = (signs[0:-2] != signs[1:-1])
        zero_crossings_i = np.where(zero_crossings)[0]
        return [self.lin_interp(x, y, zero_crossings_i[0], half),
                self.lin_interp(x, y, zero_crossings_i[1], half)]
    
    def overview(self,object_positions):  
        if self.data is None:  
            print("No data available to display.")  
            return  
        self.object_x = object_positions[0]
        self.object_y = object_positions[1]
        self.com1_x = object_positions[2]
        self.com1_y = object_positions[3]
        self.com2_x = object_positions[4]
        self.com2_y = object_positions[5]
        self.com3_x = object_positions[6]
        self.com3_y = object_positions[7]
        # Extract the zoomed-in region  
        zoomed_data = self.data[self.y_start:self.y_end, self.x_start:self.x_end]  
  
        # Display the zoomed-in region  
        plt.figure(figsize=(7, 7))  
        plt.imshow(zoomed_data, cmap='viridis')  
  
        # Draw the red circle for Object
        object_circle1 = Circle((self.object_x, self.object_y), 20, color='red', fill=False)
        plt.gca().add_patch(object_circle1)
        # Label Companion 1
        plt.text(self.object_x, self.object_y + 30, 'Object', color='red', ha='center')

        # Draw the red circle for Companion 1
        companion_circle1 = Circle((self.com1_x, self.com1_y), 10, color='red', fill=False)
        plt.gca().add_patch(companion_circle1)
        # Label Companion 1
        plt.text(self.com1_x, self.com1_y + 15, 'Companion 1', color='red', ha='center')

        # Draw the red circle for Companion 2
        companion_circle2 = Circle((self.com2_x, self.com2_y), 10, color='red', fill=False)
        plt.gca().add_patch(companion_circle2)
        # Label Companion 2
        plt.text(self.com2_x, self.com2_y + 15, 'Companion 2', color='red', ha='center') 
        
        # Draw the red circle for Companion 3
        companion_circle3 = Circle((self.com3_x, self.com3_y), 10, color='red', fill=False)
        plt.gca().add_patch(companion_circle3)
        # Label Companion 3
        plt.text(self.com3_x, self.com3_y + 15, 'Companion 3', color='red', ha='center')
        plt.colorbar()
        plt.title("Original Zoomed data") 
        plt.tight_layout() 
        plt.savefig('overview_'+ self.index) 
        plt.show()  
        
    def analysis(self,name,object_position):

        self.x_start = object_position[0]  
        self.x_end = object_position[1]
        self.y_start = object_position[2]  
        self.y_end = object_position[3]  

        # Extract the zoomed-in region
        zoomed_data = self.data[self.y_start:self.y_end, self.x_start:self.x_end]

        # Define the center of the bright spot
        center_x, center_y = (self.x_end - self.x_start) // 2, (self.y_end - self.y_start) // 2
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

        # Measure the Light Profile
        light_profile_x = np.sum(zoomed_data, axis=0)
        normalised_light_profile = light_profile_x-min(light_profile_x)

        # Determine the x-coordinates for the profile
        x_coords = np.arange(0, light_profile_x.shape[0])

        hmx = self.half_max_x(x_coords,normalised_light_profile)
        # print the answer
        fwhm = hmx[1] - hmx[0]
        print("FWHM:{:.3f}".format(fwhm))
        # Display the original zoomed-in region
        plt.figure(figsize=(20, 5))
        plt.subplot(1, 4, 1)
        plt.imshow(zoomed_data, cmap='viridis', origin='lower')
        plt.colorbar()
        plt.title("Original Zoomed data")

        # Plot apertures on the second subplot
        plt.subplot(1, 4, 2)
        norm = simple_norm(zoomed_data, 'sqrt', percent=99)
        plt.imshow(zoomed_data, cmap='viridis', norm=norm, origin='lower')
        plt.colorbar()
        plt.title("Apertures on Zoomed data")

        # Plot each aperture on the image
        for r in radii:
            aperture = CircularAperture(center_position, r=r)
            aperture.plot(color='white', lw=1.5)

        # Adjust plot limits
        plt.xlim(0, zoomed_data.shape[1])
        plt.ylim(0, zoomed_data.shape[0])

        # Plot the mean radial light profile on the third subplot
        plt.subplot(1, 4, 3)
        plt.plot(radii, mean_fluxes, 'o-', color='black')
        plt.xlabel('Aperture Radius (pixels)')
        plt.ylabel('Mean Flux (arbitrary units)')
        plt.title('Mean Radial Light Profile')
        half = max(normalised_light_profile)/2.0
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
        plt.savefig(str(name) + "_" + self.index) 
        plt.show()

    def compare(self,asteroid_pos,com1_pos,com2_pos,com3_pos):
        # Extract the zoomed-in region for the fourth set of coordinates
        x_start4, x_end4, y_start4, y_end4 = asteroid_pos
        zoomed_data4 = self.data[y_start4:y_end4, x_start4:x_end4]

        # Calculate the normalized light profile for the fourth region
        light_profile_x4 = np.sum(zoomed_data4, axis=0)
        reduced_light_x4 = light_profile_x4-min(light_profile_x4)
        factor = np.max(reduced_light_x4)
        x_coords4 = np.arange(0, light_profile_x4.shape[0])

        # Define the coordinates of the region you want to zoom in
        x_start1, x_end1, y_start1, y_end1 = com1_pos
        x_start2, x_end2, y_start2, y_end2 = com2_pos
        x_start3, x_end3, y_start3, y_end3 = com3_pos



        # Extract the zoomed-in region
        zoomed_data1 = self.data[y_start1:y_end1, x_start1:x_end1]
        zoomed_data2 = self.data[y_start2:y_end2, x_start2:x_end2]
        zoomed_data3 = self.data[y_start3:y_end3, x_start3:x_end3]


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
        plt.savefig('compare_' + self.index)
        plt.show()

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
handler.overview(object_positions)
handler.analysis('object',asteroid_position)
handler.analysis('companion1',companion1_position)
handler.analysis('companion2',companion2_position)
handler.analysis('companion3',companion3_position)
handler.compare(asteroid_position,companion1_position,companion2_position,companion3_position)
