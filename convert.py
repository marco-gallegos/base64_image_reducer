"""@Author: Marco A. Gallegos <ma_galeza@hotmail.com>
@Date:   2022-05-20
@Version: 1.0
@Description: This is a way to convert a base 64 image into a lightweight version of itself
only using pillow and without touching hard disk, so this is fast and simple.

on testing this script was able to reduce a 12000x9000 30MB jpeg image into a 1920x1080 300KB image.
"""
import base64
from image import base64_image
from  io import BytesIO
from PIL import Image
import sys
import time

# Decode back to the original bytes
new_img_str = base64.b64decode(base64_image)

# Use StringIO to provide an in-memory buffer that we can use
# to pass the image string to PIL.
bio = BytesIO(new_img_str)

# Load this file in memory using pil (we can use another library like cv2 or use imagemagick)
img = Image.open(bio)

print("doing some operations on the image")
processing_init = time.time()

current_width, current_height = img.size

img_weight = sys.getsizeof(img.tobytes()) / (1024**2)
# we use LANCZOS to get better quality, if is not needed you can delete it and get
# a lighter image and a faster processing.
# learn about LANCZOS resampling https://en.wikipedia.org/wiki/Lanczos_resampling
resized_img = img.resize((1920, 1080), resample=Image.Resampling.LANCZOS) # full hd is good for now
resized_img_bytes = resized_img.tobytes()
resized_bio = BytesIO()
resized_img.save(resized_bio, format="JPEG")
resized_base64_image = base64.b64encode(resized_bio.getvalue()).decode("utf-8")
resized_img_weight = sys.getsizeof(resized_img_bytes) / (1024**2)

processing_finish = time.time()


print(f"current width: {current_width} and current height: {current_height}") 
# the numbers are not in MB but is only to see the change in size
print(f"img variable size in memory in MB : {img_weight}")
print(f"resized image variable size in memory in MB : {resized_img_weight}")

# save the results into files
# with open("resized_base64_image.txt", "w") as f:
#    f.write(resized_base64_image)

#resized_img.save("resized_image.jpeg")

print(f"all operation finished in {processing_finish - processing_init} seconds")
# Display the images
# resized_img.show()
# img.show()