from colorthief import ColorThief

color_thief = ColorThief('/Users/rubenengel/GitHub/iot-seed-drone/flight-server/flight-scripts/Screen-Shot-2021-01-28-at-19.06.21.png')
# get the dominant color
'''
The number determines how many pixels are skipped before the next one is sampled. 
We rarely need to sample every single pixel in the image to get good results. 
The bigger the number, the faster a value will be returned.
'''
dominant_color = color_thief.get_color(quality=5)
# build a color palette
palette = color_thief.get_palette(color_count=6)



print(dominant_color)