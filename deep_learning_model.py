from transformers import GPT2TokenizerFast, ViTImageProcessor, VisionEncoderDecoderModel
from torch.utils.data import Dataset
from torchtext.data import get_tokenizer
from PIL import Image

import warnings
warnings.filterwarnings('ignore')

model_raw = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer       = GPT2TokenizerFast.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

def show_n_generate(url, greedy = True, model = model_raw):
    image = Image.open(url)
    pixel_values   = image_processor(image, return_tensors ="pt").pixel_values

    if greedy:
        generated_ids  = model.generate(pixel_values, max_new_tokens = 50)
    else:
        generated_ids  = model.generate(
            pixel_values,
            do_sample=True,
            max_new_tokens = 50,
            top_k=5)
    generated_text = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_text)

url1 = "manzara-fotografi-cekmek-724x394.webp"
url2 = "embedded_img.png"
show_n_generate(url1, greedy = True)
show_n_generate(url2, greedy = True)