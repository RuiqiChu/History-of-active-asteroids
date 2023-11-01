# Aim of these codes in step2:
# From the initial matching from step1 which gives the plates with objects on them, 
# get the precise location of the object on those plates

# To run:

# First use HORIZON system to generated the ephemeris for each interested objects on the precise time when they were taken on one plate, save the position files to this folder, name consistent with the file_names in the code

python matching_again

# This will generate a matching_info.xlsx which has the precise location of objects on each interested plate.
