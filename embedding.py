from create_key import generate_new_key, key_expansion
import cv2

def find_quarters(img, height, width):
    quarters = []
    rng1 = 3
    rng2 = 3
    for i in range(rng1):
        for j in range(rng2):
            quarter = img[i * height // rng1:(i + 1) * height // rng1, j * width // rng2:(j + 1) * width // rng2].flatten()
            quarters.append(quarter)
    return quarters


def find_new_index_value(binary, index):
    binary_index = bin(index)
    binary_index_len = len(binary_index)
    if binary_index_len > 0:
        son_bit = int(binary_index[-1])
        if son_bit == binary:
            print(binary_index)
            return index
        new_binary = binary_index[:-1] + binary
        new_binary = int(new_binary, 2)
        return new_binary
    
    
def create_new_quarters(newKey, quarters, birlesik_binary):
    for i in range(0,10):
        if(i == len(newKey)):
            break
        for binary ,k in zip(birlesik_binary[i], newKey[i]):
            quarters[i][k] = find_new_index_value(binary,  quarters[i][k])
    return quarters

def create_new_image(img, height, width, quarters):
    rng1 = 3
    rng2 = 3
    for i in range(rng1):
        for j in range(rng2):
            quarter_height = (i + 1) * height // rng1 - i * height // rng1
            quarter_width = (j + 1) * width // rng2 - j * width // rng2
            img[i * height // rng1:(i + 1) * height // rng1, j * width // rng2:(j + 1) * width // rng2] = \
            quarters[i * rng2 + j].reshape((quarter_height, quarter_width, 3))
    return img    


def embedding(image_path, birlesik_binary, key):
    img = cv2.imread(image_path)
    height, width, z = img.shape
    quarters = find_quarters(img, height, width)
    new_quarters = create_new_quarters(key, quarters, birlesik_binary)
    new_image = create_new_image(img, height, width, new_quarters)
    return new_image