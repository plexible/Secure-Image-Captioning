import cv2
from embedding.embedding import find_quarters

def find_index_value(index):
    binary_index = format(index, '08b')
    binary_index_len = len(binary_index)
    if binary_index_len > 0:
        son_bit = int(binary_index[-1])
        return str(son_bit)

def extract_key_from_image(newKey, quarters):
    new_string = []
    for i in range(0,10):
        str = ""
        if(i == len(newKey)):
            break
        for k in newKey[i]:
            str += find_index_value(quarters[i][k])
        new_string.append(str)
    return new_string

def extracting(image_path, key):
    img = cv2.imread(image_path)
    height, width, z = img.shape
    quarters = find_quarters(img, height, width)
    return extract_key_from_image(key, quarters)