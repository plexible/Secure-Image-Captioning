from key.create_key import generate_key, embedding_key
from key.create_secret_key import create_binary_secret_key_list, convert_binary_secret_key_list_byte
from embedding.embedding import embedding
from extracting.extracting import extracting
from deep_learning.deep_learning_model import show_n_generate
import cv2

from test.test_images import calculate_histogram, calculate_mae, calculate_mse, calculate_psnr, calculate_ssim, perform_statistical_test
from tabulate import tabulate

results = []

for i in range(1, 11):
    image_path = f'assets/embedding_images/img{i}.jpg'
    output_path = f'assets/embedded_images/embedded_img{i}.png'
    
    result = {'Index': i}
    print(f"************************     {i}       ******************************")
    
    secret_key = generate_key()
    result['Secret Key'] = secret_key
    print(f"Secret Key: {secret_key}")
    
    combined_binary = create_binary_secret_key_list(secret_key)
    
    # Key
    key = show_n_generate(image_path, greedy=True)
    print(key)
    result['Caption Before Embedding'] = key
    key = key.encode("utf-8")
    generated_embedding_key = embedding_key(key)
    
    # Embedding Part
    changed_pixel, embedded_image = embedding(image_path, combined_binary, generated_embedding_key)
    result['Changed Pixel'] = changed_pixel
    print(f'Changed Pixel: {changed_pixel}')
    
    # Save the embedded image
    cv2.imwrite(output_path, embedded_image)
    
    # Test
    # Load images
    original_image = cv2.imread(image_path, 0)
    distorted_image = cv2.imread(output_path, 0)
    
    # Calculate histograms
    original_histogram = calculate_histogram(original_image)
    distorted_histogram = calculate_histogram(distorted_image)
    
    # Statistical test
    t_statistic, p_value = perform_statistical_test(original_histogram, distorted_histogram)
    result['T statistic'] = t_statistic
    result['P value'] = p_value
    print("T statistic:", t_statistic)
    print("P value:", p_value)
    
    # İki resmi yükle
    original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    distorted_image = cv2.imread(output_path, cv2.IMREAD_COLOR)
    
    # PSNR'yi hesapla
    psnr_value = calculate_psnr(original_image, distorted_image)
    result['PSNR Value'] = psnr_value
    print("PSNR Value:", psnr_value)
    
    # MSE'yi hesapla
    mse_value = calculate_mse(original_image, distorted_image)
    result['MSE Value'] = mse_value
    print("MSE Value:", mse_value)
    
    # MAE'yi hesapla
    mae_value = calculate_mae(original_image, distorted_image)
    result['MAE Value'] = mae_value
    print("MAE Value:", mae_value)
    
    # SSI'yi hesapla
    ssim_score = calculate_ssim(original_image, distorted_image)
    result['SSI Score'] = ssim_score
    print("SSI Score:", ssim_score)
    # Deep Learning Model
    key = show_n_generate(output_path, greedy=True)
    result['Caption After Embedding'] = key
    print(key)
    key = key.encode("utf-8")
    generated_embedding_key = embedding_key(key)
    
    extracted_array = extracting(output_path, generated_embedding_key)
    extracted_secret_key = convert_binary_secret_key_list_byte(extracted_array)
    result['Extracted Secret Key'] = extracted_secret_key
    print(extracted_secret_key)
    
    results.append(result)

# Print results in tabular format
headers = [
    "Index", "Secret Key", "Caption Before Embedding", "Changed Pixel", "T statistic", "P value", 
    "PSNR Value", "MSE Value", "MAE Value", "SSI Score", "Caption After Embedding", "Extracted Secret Key"
]
table = [[result[header] for header in headers] for result in results]
print(tabulate(table, headers=headers, tablefmt="grid"))