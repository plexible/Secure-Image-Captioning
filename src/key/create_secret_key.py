def create_binary_secret_key_list(secret_key):
    pieces = [secret_key[i:i+2] for i in range(0, len(secret_key), 2)]
    combined_binary = [''.join(format(byte, '08b') for byte in parca) for parca in pieces]
    return combined_binary

def convert_binary_secret_key_list_byte(combined_binary):
    secret_key = ""
    secret_key = ''.join([chr(int(i[0:len(i)//2], 2)) + chr(int(i[len(i)//2:], 2)) for i in combined_binary])
    return secret_key.encode("utf-8")