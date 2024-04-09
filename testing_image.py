import cv2
import numpy as np
from scipy.stats import ttest_ind

def calculate_histogram(image):
    # Check if the image is loaded successfully
    if image is None:
        raise ValueError("Image not loaded properly.")
    # Calculate histogram
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    return histogram

def perform_statistical_test(histogram1, histogram2):
    # Check if both histograms have the same shape
    if histogram1.shape != histogram2.shape:
        raise ValueError("Histograms have different shapes.")
    # Perform t-test
    t_statistic, p_value = ttest_ind(histogram1, histogram2)
    return t_statistic, p_value

# Paths to the original image and the distorted (hidden message) image
original_image_path = "manzara-fotografi-cekmek-724x394.webp"
distorted_image_path = "embedded_img.png"

# Load images
original_image = cv2.imread(original_image_path, 0)
distorted_image = cv2.imread(distorted_image_path, 0)

# Calculate histograms
original_histogram = calculate_histogram(original_image)
distorted_histogram = calculate_histogram(distorted_image)

# Perform histogram analysis
# Histogram comparison process is performed here.

# Statistical test
try:
    t_statistic, p_value = perform_statistical_test(original_histogram, distorted_histogram)
    print("T statistic:", t_statistic)
    print("P value:", p_value)
except ValueError as e:
    print("Error:", e)
    
    
    
import cv2

# İki resmin Peak Signal-to-Noise Ratio'sunu hesaplar
def calculate_psnr(image1, image2):
    psnr = cv2.PSNR(image1, image2)
    return psnr

# İki resmi yükle
image1 = cv2.imread("manzara-fotografi-cekmek-724x394.webp", cv2.IMREAD_COLOR)
image2 = cv2.imread("embedded_img.png", cv2.IMREAD_COLOR)


# PSNR'yi hesapla
psnr_value = calculate_psnr(image1, image2)
print("PSNR Value:", psnr_value)

 
import cv2
import numpy as np

# İki resmin Mean Squared Error'ını hesaplar
def calculate_mse(image1, image2):
    mse = np.mean((image1 - image2) ** 2)
    return mse

# İki resmi yükle
image1 = cv2.imread("manzara-fotografi-cekmek-724x394.webp", cv2.IMREAD_COLOR)
image2 = cv2.imread("embedded_img.png", cv2.IMREAD_COLOR)

# MSE'yi hesapla
mse_value = calculate_mse(image1, image2)
print("MSE Value:", mse_value)


import cv2
import numpy as np

# İki resmin Mean Absolute Error'ını hesaplar
def calculate_mae(image1, image2):
    mae = np.mean(np.abs(image1 - image2))
    return mae

# İki resmi yükle
image1 = cv2.imread("manzara-fotografi-cekmek-724x394.webp", cv2.IMREAD_COLOR)
image2 = cv2.imread("embedded_img.png", cv2.IMREAD_COLOR)

# MAE'yi hesapla
mae_value = calculate_mae(image1, image2)
print("MAE Value:", mae_value)


from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
# İki resmin benzerliğini ölçmek için Structural Similarity Index'i hesaplar
def calculate_ssim(image1, image2):
    ssim_score, _ = ssim(image1, image2, full=True, channel_axis=2)
    return ssim_score

# İki resmi yükle
image1 = cv2.imread("manzara-fotografi-cekmek-724x394.webp", cv2.IMREAD_COLOR)
image2 = cv2.imread("embedded_img.png", cv2.IMREAD_COLOR)

# SSI'yi hesapla
ssim_score = calculate_ssim(image1, image2)
print("SSI Score:", ssim_score)