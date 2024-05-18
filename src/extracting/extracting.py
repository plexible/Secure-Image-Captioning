import cv2
from embedding.embedding import find_quarters, select_numbers_from_list, unique_list
import math
def find_index_value(index):
    binary_index = format(index, '08b')
    binary_index_len = len(binary_index)
    if binary_index_len > 0:
        son_bit = int(binary_index[-1])
        return str(son_bit)

def extract_key_from_image(newKey, quarters, selected_quarters):
    new_string = []
    for i,x in zip(selected_quarters, range(0,10)):
        str = ""
        if(x == len(newKey)):
            break
        for k in newKey[x]:
            str += find_index_value(quarters[i][k])
        new_string.append(str)
    return new_string

def extracting(image_path, key):
    key_len = len(key[0])*8
    img = cv2.imread(image_path)
    height, width, z = img.shape
    max_size = int(height * width / key_len)*0.8
    selected_quarters = select_numbers_from_list(key[0], max_size)
    selected_quarters = unique_list(selected_quarters)
    quarters = find_quarters(img, key_len, height, width)
    return extract_key_from_image(key, quarters, selected_quarters)