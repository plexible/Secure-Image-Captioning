from collections import Counter
from cryptography.fernet import Fernet
import numpy as np

s_box = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

Rcon = [
    [0x01, 0x00, 0x00, 0x00], [0x02, 0x00, 0x00, 0x00], 
    [0x04, 0x00, 0x00, 0x00], [0x08, 0x00, 0x00, 0x00],
    [0x10, 0x00, 0x00, 0x00], [0x20, 0x00, 0x00, 0x00], 
    [0x40, 0x00, 0x00, 0x00], [0x80, 0x00, 0x00, 0x00],
    [0x1B, 0x00, 0x00, 0x00], [0x36, 0x00, 0x00, 0x00]
]

def rot_word(temp):
    return temp[1:] + [temp[0]] 

def sub_word(word):
    return [s_box[i] for i in word]  

def is_duplicate(lst):
    # Listenin içindeki değerlerin sayılarını hesapla
    counts = Counter(lst)
    
    # Tekrar eden değerler varsa True, yoksa False döndür
    for count in counts.values():
        if count > 1:
            return True
    return False

def unique_list(lst):
    seen = set()
    for i, item in enumerate(lst):
        while item in seen:
            item += 1
        lst[i] = item
        seen.add(item)
        
    return lst

def generate_key():
    fernet_key = Fernet.generate_key()
    aes_key_256_bits = fernet_key[:16]
    return aes_key_256_bits    

def generate_new_key(generated_key):
    key = list(generated_key)
    newKey = [key]
    key = rot_word(key)
    while len(newKey) < 16:
        key = sub_word(key)
        newKey.append(key)
    newKey = newKey[:16]
    newKey = [item for sublist in newKey for item in sublist][:16]
    newKey = unique_list(newKey)
    return newKey        

def key_expansion(key):
    newList = []
    key_schedule = [key[i:i+4] for i in range(0, len(key), 4)]
    Nk = len(key) // 4
    Nb = 4
    Nr = 7 
    for i in range(Nk, Nb * (Nr + 1)):
        temp = key_schedule[i-1]
        if i % Nk == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp = [temp[j] ^ Rcon[(i//Nk)-1][j] for j in range(4)]
        key_schedule.append([key_schedule[i-Nk][j] ^ temp[j] for j in range(4)])
    key_schedule = [item for sublist in key_schedule for item in sublist]
    for i in range(0,len(key_schedule), 16):
        new = key_schedule[i:i+16]
        newList.append(unique_list(new))
    return newList

def numbers_different_from_each_other(sum):
    while not (len(set(str(sum))) == len(str(sum))): #For the numbers to be different from each other.
        sum += 1
    return sum

def embedding_key(key_value):
    newKey = generate_new_key(key_value)
    newKey = key_expansion(newKey)
    return newKey

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
    
def find_index_value(index):
    binary_index = bin(index)
    binary_index_len = len(binary_index)
    if binary_index_len > 0:
        son_bit = int(binary_index[-1])
        return str(son_bit)
    
def create_new_quarters(newKey, quarters, birlesik_binary):
    for i in range(0,10):
        if(i == len(newKey)):
            break
        for binary ,k in zip(birlesik_binary[i], newKey[i]):
            quarters[i][k] = find_new_index_value(binary,  quarters[i][k])
    return quarters

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
            
def create_new_image(img, height, width, quarters):
    for i in range(3):
        for j in range(3):
            quarter_height = (i + 1) * height // 3 - i * height // 3
            quarter_width = (j + 1) * width // 3 - j * width // 3
            img[i * height // 3:(i + 1) * height // 3, j * width // 3:(j + 1) * width // 3] = \
            quarters[i * 3 + j].reshape((quarter_height, quarter_width, 3))
    return img    
  
def embedding_key(key_value):
    newKey = generate_new_key(key_value)
    newKey = key_expansion(newKey)
    return newKey
        