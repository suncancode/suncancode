"""
Task 4 - Unstructured data: an image
CSCI446/946 Big Data Analytics - Lab 1
"""

import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# ---- Đường dẫn tới thư mục chứa dataset ----
DATA_DIR = r"D:\sun\WOLLONGONG\S226\CSCI946 - Big Data Analytics\Lab\W2\Lab1-Released\CSCI446_946_Week2_Lab_SP_2026_Datasets"

# 4.1 Load, display and inspect the image
image = mpimg.imread(os.path.join(DATA_DIR, "campus.png"))

plt.imshow(image)
plt.title("Campus Image")
plt.axis("off")
plt.show()

print("Shape:", image.shape)
print("Data type:", image.dtype)
print("Top-left pixel:", image[0, 0])

# 4.2 Crop the image and inspect one colour channel
# Crop a region: rows 160-320 and columns 300-570
crop = image[160:320, 300:570]
plt.imshow(crop)
plt.title("Cropped Image")
plt.axis("off")
plt.show()

print("Cropped shape:", crop.shape)

# Display the red channel
red_channel = image[:, :, 0]
plt.imshow(red_channel, cmap="gray")
plt.title("Red Channel")
plt.colorbar(label="Intensity")
plt.axis("off")
plt.show()

print("Mean red value:", red_channel.mean())

"""
Questions to answer:
1. What do the three values in image.shape represent?
2. What information is stored in one pixel of this colour image?
3. How does the cropped image differ from the original image?
4. Why can an image be called unstructured data even though Python
   stores it as an array?
"""
