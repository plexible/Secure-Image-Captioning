from create_key import embedding_key
from embedding import embedding
from extracting import extracting
import cv2
#String
# Birleştirilmiş binary dizisi
birlesik_binary = ["0111110101000010", "0100001101000100", "0100000101000010", "0100000101000010",
                   "0100000101000010", "0100000101000010", "0100000101000010", "0100000101000010"]
#Key
key = b"asd"
generated_embedding_key = embedding_key(key)

#Embedding Part
image_path = "image.jpg"
output_path = "embedded_img.png"
embedded_image = embedding(image_path, birlesik_binary, generated_embedding_key)   

#Extractin Part
output_path = "embedded_img.png"
cv2.imwrite(output_path, embedded_image)
    

val = extracting(output_path, generated_embedding_key)
print(val)