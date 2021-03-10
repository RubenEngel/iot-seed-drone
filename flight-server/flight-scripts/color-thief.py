from colorthief import ColorThief
# from picamera import PiCamera

# camera = PiCamera()

# camera.resolution = (500, 500)

# camera.capture('/current_location.jpg')

color_thief = ColorThief('/current_location.jpg')

# get the dominant color
'''
The number determines how many pixels are skipped before the next one is sampled. 
We rarely need to sample every single pixel in the image to get good results. 
The bigger the number, the faster a value will be returned.
'''
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=3)

print(dominant_color)