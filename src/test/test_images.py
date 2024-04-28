import cv2
import numpy as np
from scipy.stats import ttest_ind
from skimage.metrics import structural_similarity as ssim

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
    
def calculate_psnr(image1, image2):
    psnr = cv2.PSNR(image1, image2)
    return psnr

# İki resmin Mean Squared Error'ını hesaplar
def calculate_mse(image1, image2):
    mse = np.mean((image1 - image2) ** 2)
    return mse

# İki resmin Mean Absolute Error'ını hesaplar
def calculate_mae(image1, image2):
    mae = np.mean(np.abs(image1 - image2))
    return mae

# İki resmin benzerliğini ölçmek için Structural Similarity Index'i hesaplar
def calculate_ssim(image1, image2):
    ssim_score, _ = ssim(image1, image2, full=True, channel_axis=2)
    return ssim_score
