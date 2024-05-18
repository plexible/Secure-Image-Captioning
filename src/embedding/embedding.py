from key.create_key import generate_new_key, key_expansion
import cv2
import math

def unique_list(lst):
    seen = set()
    for i, item in enumerate(lst):
        while item in seen:
            item += 1
        lst[i] = item
        seen.add(item)
        
    return lst

def scale_number_to_range(number, min_value, max_value, target_min, target_max):
    # Oranla ölçekleme yap ve tam sayıya dönüştür
    scaled_number = int(((number - min_value) / (max_value - min_value)) * (target_max - target_min) + target_min)
    return scaled_number

def select_numbers_from_list(number_list, max_val):
    min_value = min(number_list)
    max_value = max(number_list)
    target_min = 0
    target_max = max_val
    
    selected_numbers = []
    for number in number_list:
        selected_number = scale_number_to_range(number, min_value, max_value, target_min, target_max)
        selected_numbers.append(selected_number)
    return selected_numbers

def find_quarters(img, keyLen, height, width):
    quarterSize = int(math.sqrt(height * width / keyLen))
    quarters = []
    rng1 = quarterSize
    rng2 = quarterSize
    for i in range(rng1):
        for j in range(rng2):
            quarter = img[i * height // rng1:(i + 1) * height // rng1, j * width // rng2:(j + 1) * width // rng2].flatten()
            quarters.append(quarter)
    return quarters


def find_new_index_value(binary, index):
    binary_index = format(index, '08b')
    binary_index_len = len(binary_index)
    if binary_index_len > 0:
        last_bit = int(binary_index[-1])
        if last_bit == int(binary):
            changed_pixel =0
            return changed_pixel, index
        changed_pixel = 1
        new_binary = binary_index[:-1] + binary
        new_binary = int(new_binary, 2)
        return changed_pixel, new_binary
    
    
def create_new_quarters(newKey, quarters, birlesik_binary, selected_quarters):
    changed_pixel = 0
    for i, x in zip(selected_quarters, range(0,10)):
        if(x == len(newKey)):
            break
        for binary ,k in zip(birlesik_binary[x], newKey[x]):
            changed, quarters[i][k] = find_new_index_value(binary,  quarters[i][k])
            changed_pixel += changed
    return changed_pixel, quarters

def create_new_image(img, height, width, keyLen, quarters):
    quarterSize = int(math.sqrt(height * width / keyLen))
    rng1 = quarterSize
    rng2 = quarterSize
    for i in range(rng1):
        for j in range(rng2):
            quarter_height = (i + 1) * height // rng1 - i * height // rng1
            quarter_width = (j + 1) * width // rng2 - j * width // rng2
            img[i * height // rng1:(i + 1) * height // rng1, j * width // rng2:(j + 1) * width // rng2] = \
            quarters[i * rng2 + j].reshape((quarter_height, quarter_width, 3))
    return img    


def embedding(image_path, birlesik_binary, key):
    key_len = len(key[0])*8
    img = cv2.imread(image_path)
    height, width, z = img.shape
    max_size = int(height * width / key_len)*0.8
    selected_quarters = select_numbers_from_list(key[0], max_size)
    selected_quarters = unique_list(selected_quarters)
    quarters = find_quarters(img, key_len, height, width)
    changed_pixel, new_quarters = create_new_quarters(key, quarters, birlesik_binary, selected_quarters)
    new_image = create_new_image(img, height, width, key_len, new_quarters)
    return changed_pixel, new_image

