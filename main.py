from create_key import embedding_key
from embedding import embedding
from extracting import extracting
import cv2
#String
# Birleştirilmiş binary dizisi
birlesik_binary = ['0100000101000010', '0100001101000100', '0100010101000110', '0100011101001000', 
                   '0100101001001010', '0100101101001100', '0100110101001110', '0100111101010000', '0101000101010001']

#Key
key = b"a man"
generated_embedding_key = embedding_key(key)

#Embedding Part
image_path = "manzara-fotografi-cekmek-724x394.webp"
output_path = "embedded_img.png"
embedded_image = embedding(image_path, birlesik_binary, generated_embedding_key)   

#Extractin Part
output_path = "embedded_img.png"
cv2.imwrite(output_path, embedded_image)
    
generated_embedding_key = embedding_key(key)

val = extracting(output_path, generated_embedding_key)
print(val)
