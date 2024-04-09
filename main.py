from create_key import generate_key, embedding_key, create_binary_secret_key_list, convert_binary_secret_key_list_byte
from embedding import embedding
from extracting import extracting
import cv2

#String
secret_key = generate_key()
print(secret_key)
combined_binary = create_binary_secret_key_list(secret_key)

#Key
key = b"a man"
generated_embedding_key = embedding_key(key)

#Embedding Part
image_path = "manzara-fotografi-cekmek-724x394.webp"
output_path = "embedded_img.png"
embedded_image = embedding(image_path, combined_binary, generated_embedding_key)   

#Extractin Part
output_path = "embedded_img.png"
cv2.imwrite(output_path, embedded_image)
    
generated_embedding_key = embedding_key(key)

val = extracting(output_path, generated_embedding_key)
print(val)


byte_dizi = convert_binary_secret_key_list_byte(val)

print(byte_dizi)