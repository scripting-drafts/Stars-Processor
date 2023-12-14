import pandas as pd
import math
from stars_processor import stars_processor

col_def = pd.read_fwf('../data/bsc_label.txt', header=None, colspecs=(
    (0,4),
    (5,9),
    (9,17),
    (17,23),
    (23,34)
))

# print(col_def)
star_col_def = []
column_names = []

for _, (n1, n2, _, _, name) in col_def.iterrows():
    if not pd.isna(n1):
        star_col_def.append((int(n1)-1, int(n2)))
    else:
        star_col_def.append((int(n2)-1, int(n2)))
    column_names.append(name)

star_def = pd.read_fwf('../data/bsc5.dat', header=None, colspecs=star_col_def)
star_def.columns = column_names

col_def = pd.read_fwf('../data/bsc_label.txt', header=None, colspecs=(
    (0,4),
    (5,9),
    (9,17),
    (17,23),
    (23,34)
))

star_def = pd.read_fwf('../data/bsc5.dat', header=None, colspecs=star_col_def)
star_def.columns = column_names

print(star_def.head())

class Star():
    """
    A class representing a star, with name, magnitude, right ascension (ra),
    declination (dec) and projected co-ordinates x,y calculated by a class
    method.
    """

    def __init__(self, hr_name, name, dm_name, hd_name, sao_name, spectral_type, mag, ra, dec, rot_vel):
        """
        Initializes the star object with its name and magnitude, and position
        as right ascension (ra) and declination (dec), both in radians.
        """
        sp = stars_processor()

        self.hr_name = hr_name
        self.name = name
        self.dm_name = dm_name
        self.hd_name = hd_name
        self.sao_name = sao_name

        self.spectral_type = spectral_type
        self.mag = mag
        self.ra = ra
        self.dec = dec
        self.const = ""
        self.rot_vel = rot_vel
        self.temp = sp.get_temperature(spectral_type)
        self.lum = sp.get_luminosity(spectral_type)

        if not pd.isna(name):
            self.name = name
            if len(name) >= 3:
                self.const = name[-3:]
                self.name = name[:-3]
        else:
            self.name = ""
        self.name = self.name.strip()
        self.project_orthographic(0, 0)
                
    def project_orthographic(self, ra0, dec0):
        """
        Calculates, stores and returns the projected co-ordinates (x, y) of
        this star's position using an orthographic projection about the
        angular position (ra0, dec0).

        """

        delta_ra = self.ra - ra0
        self.x = math.cos(self.dec) * math.sin(delta_ra)
        self.y = math.sin(self.dec) * math.cos(dec0)\
             - math.cos(self.dec) * math.cos(delta_ra) * math.sin(dec0)
        return self.x, self.y
    
    def __repr__(self):
        return f"Name:{self.name},Const:{self.const},Mag:{self.mag},RA:{self.ra},DEC:{self.dec}"


stars = []

for _, line in star_def.iterrows():
    if pd.isna(line['Vmag']):
        continue
    hr_name = line['HR']
    name = line['Name']
    dm_name = line['DM']
    hd_name = line['HD']
    sao_name = line['SAO']
    
    spectral_type = line['SpType']
    mag = float(line['Vmag'])
    rot_vel = float(line['RotVel'])

    # Right ascension (hrs, mins, secs), equinox J2000, epoch 2000.0
    ra_hrs, ra_min, ra_sec = [float(x) for x in (line['RAh'],
                                                 line['RAm'], line['RAs'])]
    # Declination (hrs, mins, secs), equinox J2000, epoch 2000.0
    dec_deg, dec_min, dec_sec = [float(x) for x in (str(line['DE-'])+str(line['DEd']),
                                                 line['DEm'], line['DEs'])]
    # Convert both RA and declination to radians
    ra = math.radians((ra_hrs + ra_min/60 + ra_sec/3600) * 15.)
    # NB in the Southern Hemisphere be careful to subtract the minutes and
    # seconds from the (negative) degrees.
    sgn = math.copysign(1, dec_deg)
    dec = math.radians(dec_deg + sgn * dec_min/60 + sgn * dec_sec/3600)

    # Create a new Star object and add it to the list of stars
    stars.append(Star(hr_name, name, dm_name, hd_name, sao_name, spectral_type, mag, ra, dec, rot_vel))

tau = []

for s in stars:
    if s.const =='Tau':
        tau.append([s.hr_name, s.const, s.name, s.spectral_type, [s.x, s.y], s.mag, s.rot_vel, s.temp, s.lum])
        # print(s.hr_name, s.const, s.name, spectral_type, [s.x, s.y], s.mag, s.rot_vel)

for each in tau:
    print(each)

# DEBUG print(len(tau))
print(star_def.columns)

# [(s.x, s.y, s.mag) for s in stars if s.const=='Cas'][:5]

# import cv2
# import numpy as np

# # Define the image size
# image_width = 800
# image_height = 600
# color = (0,255,255)  # BGR color (red in this case)

# def paint_stars(data):

#     image = 255 * np.zeros((image_height, image_width, 3), dtype=np.uint8)
    
#     max_x = max(item[0] for item in data)
#     max_y = max(item[1] for item in data)
#     min_x = min(item[0] for item in data)
#     min_y = min(item[1] for item in data)
    
#     mag_data = [item[2] for item in data]
#     min_mag = np.percentile(data, 25)
#     max_mag = np.percentile(data, 95)

#     for x, y, mag in data:
#         # Scale the (x, y) coordinates
#         scaled_x = int((x-min_x)/(max_x-min_x) * image_width)
#         scaled_y = int((y-min_y)/(max_y-min_y) * image_height)

#         # Scale the magnitude to determine the radius
#         mag = min(max(mag, min_mag), max_mag)
#         scaled_mag = int((mag-min_mag)/(max_mag-min_mag)) * 4

#         # Draw a filled circle on the image

#         cv2.circle(image, (scaled_x, scaled_y), scaled_mag, 
#                    color, -1)  # -1 for filled circle

#     # Save or display the resulting image
#     cv2.imshow("Result Image", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# paint_stars([(s.x, s.y, s.mag) for s in stars if s.const=='Ori'])

# print(list(set(s.const for s in stars)))

