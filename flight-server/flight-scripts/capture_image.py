from picamera import PiCamera

camera = PiCamera()

camera.resolution = (500, 500)

camera.capture('/current_location.jpg')