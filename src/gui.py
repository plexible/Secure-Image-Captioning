from customtkinter import *
from cv2 import COLOR_BGR2RGB, imwrite, cvtColor
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk
import string
import warnings
import easygui

from key.create_key import generate_key, embedding_key
from key.create_secret_key import create_binary_secret_key_list, convert_binary_secret_key_list_byte
from embedding.embedding import embedding
from extracting.extracting import extracting
from deep_learning.deep_learning_model import show_n_generate
warnings.simplefilter("ignore")

class MyApp(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("dark")
        self.title("Embedding-Extracting")
        self.secret_key = ""
        self.generated_secret_key = ""
        self.embedding_caption = ""
        self.caption = ""
        self.image_path = None
        self.extraction_file_path = None
        self.tabview = CTkTabview(master=self)
        self.tabview.pack(padx=20, pady=20)

        self.embedding_tab = self.tabview.add("Embedding")
        self.extracting_tab = self.tabview.add("Extracting")

        self.create_embedding_tab()
        self.create_extracting_tab()
    
    def create_embedding_tab(self):
        self.secret_key_frme = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        self.information_frame = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        self.image_frame = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)

        self.secret_key_frme.grid(row=0, column=0, padx=20, pady=20)
        self.information_frame.grid(row=1, column=0, padx=20, pady=20)
        self.image_frame.grid(row=0, column=1, padx=20, pady=(0,200))
        
        self.create_secret_key_widgets()

        self.create_caption_widgets()

        refresh_button = CTkButton(master=self.embedding_tab, text="Refresh", command=self.perform_embedding_refresh)
        refresh_button.grid(row=1, column=0, padx=20, pady=(320,0))

        browse_button = CTkButton(self.image_frame, text="Choose Image", command=self.browse_image)
        browse_button.grid(row=0, column=0, pady=10)

    def create_caption_widgets(self):
        self.label = CTkLabel(master=self.information_frame, text="Embedding")
        self.show_embedding_caption = CTkLabel(master=self.information_frame, text="Caption:  " + self.embedding_caption)
        self.ebmedding_btn = CTkButton(master=self.information_frame, text="Embedding", command=self.perform_embedding)

        self.label.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_embedding_caption.pack(anchor="n", expand=True, padx=30, pady=10)
        self.ebmedding_btn.pack(anchor="n", expand=True, padx=30, pady=20)

    def create_secret_key_widgets(self):
        self.label_secret_key = CTkLabel(master=self.secret_key_frme, text="Generate Secret Key")
        self.show_embedding_secret_key = CTkLabel(master=self.secret_key_frme, text="Secret Key:  " + self.generated_secret_key)
        self.generate_key_btn = CTkButton(master=self.secret_key_frme, text="Generate Key", command=self.create_secret_key)
        
        self.label_secret_key.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_embedding_secret_key.pack(anchor="n", expand=True, padx=30, pady=10)
        self.generate_key_btn.pack(anchor="n", expand=True, padx=30, pady=20)
        
    def create_secret_key(self):
        self.generated_secret_key = generate_key().decode('utf-8')
        self.label_secret_key.destroy()
        self.show_embedding_secret_key.destroy()
        self.generate_key_btn.destroy()    
        self.create_secret_key_widgets()

    def create_extracted_information_widgets(self):
        self.show_caption = CTkLabel(master=self.extracted_information_frame, text="Caption:  " + self.caption)
        self.show_secret_key = CTkLabel(master=self.extracted_information_frame, text="Secret Key:  " + self.secret_key)
        self.submit_btn = CTkButton(master=self.extracted_information_frame, text="Extracting", command=self.perform_extracting)

        self.show_caption.pack(anchor="s", expand=True, padx=30, pady=10)
        self.show_secret_key.pack(anchor="s", expand=True, padx=30, pady=10)
        self.submit_btn.pack(anchor="n", expand=True, padx=30, pady=20)

    def create_extracting_tab(self):
        self.extracted_information_frame = CTkFrame(master=self.extracting_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        self.extracting_image_frame = CTkFrame(master=self.extracting_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
        
        self.extracted_information_frame.grid(row=0, column=1, padx=20, pady=20)
        self.extracting_image_frame.grid(row=0, column=0, padx=20, pady=(0,200))

        label = CTkLabel(master=self.extracted_information_frame, text="Extracted Information  ")
        label.pack(anchor="s", expand=True, padx=30, pady=10)
        
        self.create_extracted_information_widgets()

        refresh_button = CTkButton(master=self.extracting_tab, text="Refresh", command=self.perform_extracting_refresh)
        refresh_button.grid(row=0, column=1, padx=20, pady=(320,0))

        browse_button = CTkButton(self.extracting_image_frame, text="Choose Image", command=self.browse_extracting_image)
        browse_button.grid(row=0, column=0, pady=10)


    def perform_extracting_refresh(self):
        self.secret_key = ""
        self.caption = ""
        self.extracting_image_frame.destroy()
        self.extracted_information_frame.destroy()
        self.extraction_file_path = ""
        self.create_extracting_tab()

    def perform_embedding_refresh(self):
        self.generated_secret_key = ""
        self.embedding_caption = ""
        self.secret_key_frme.destroy()
        self.image_frame.destroy()
        self.information_frame.destroy()
        if hasattr(self, "new_image_frame"):
            getattr(self, "new_image_frame").destroy()
        self.image_path = ""
        self.create_embedding_tab()

    def browse_image(self):  
        try:
            file_path = easygui.fileopenbox(default="*.png;*.jpg;*.jpeg", filetypes=["*.png", "*.jpg", "*.jpeg"])
            if file_path:
                self.image_path = file_path
            else:
                print("The file was not selected or the operation was cancelled.")
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_frame.grid(row=0, column=1, padx=20, pady=10)
            self.display_image(photo, self.image_frame, "embedding_label")
        except Exception as e:
            messagebox.showerror("Error", "The file was not selected or the operation was cancelled.")


    def browse_extracting_image(self):
        try:
            file_path = easygui.fileopenbox(default="*.png;*.jpg;*.jpeg", filetypes=["*.png", "*.jpg", "*.jpeg"])
            if file_path:
                self.extraction_file_path = file_path
            else:
                self.error = f"The file was not selected or the operation was cancelled."
                print(self.error)
            image = Image.open(file_path)
            image.thumbnail((400, 400)) 
            photo = ImageTk.PhotoImage(image)
            self.extracting_image_frame.grid(row=0, column=0, padx=20, pady=10)
            self.display_image(photo, self.extracting_image_frame, "extracting_label")
        except Exception as e:
            messagebox.showerror("Error", self.error)
        
    def perform_embedding(self):
        try:
            if(self.generated_secret_key == ""):
                self.error = f"Generate a secret key!"
                raise ValueError("Generate a secret key!")
            self.error = f"Embedding operation is failed"
            #Key
            key = show_n_generate(self.image_path, greedy = True).encode("utf-8")
            self.embedding_caption = key.decode('utf-8')
            self.label.destroy()
            self.show_embedding_caption.destroy()
            self.ebmedding_btn.destroy() 
            self.create_caption_widgets()   
            generated_embedding_key = embedding_key(key)
            combined_binary = create_binary_secret_key_list(self.generated_secret_key.encode("utf-8"))    
            #Embedding Part
            new_img = embedding(self.image_path, combined_binary, generated_embedding_key)   
            
            self.new_image_frame = CTkFrame(master=self.embedding_tab, fg_color="#8D6F3A", border_color="#FFCC70", border_width=2)
            self.new_image_frame.grid(row=0, column=2, padx=20)
            new_image_label = CTkLabel(master=self.new_image_frame, text="Embedded Image")
            new_image_label.grid(row=0, column=0, pady=10, padx=10)
            img = cvtColor(new_img, COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)
            self.display_image(photo, self.new_image_frame, "embedded_label")

            messagebox.showinfo("Embedding", "The operation has been completed successfully.")

            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                imwrite(file_path, new_img)
                messagebox.showinfo("Embedding", "The operation has been completed successfully.")
        except Exception as e:
            self.perform_embedding_refresh()
            messagebox.showerror("Error", self.error)

    def perform_extracting(self):
        if not self.extraction_file_path:
            messagebox.showerror("Error", "Choose an image.")
        else:
            try:
                key = show_n_generate(self.extraction_file_path, greedy = True).encode("utf-8")    
                self.caption = key.decode('utf-8')
                generated_embedding_key = embedding_key(key)
                extracted_array = extracting(self.extraction_file_path, generated_embedding_key)
                print(extracted_array)

                extracted_secret_key = convert_binary_secret_key_list_byte(extracted_array)
                self.secret_key = extracted_secret_key.decode('utf-8')
                
                for widget in [self.show_secret_key, self.show_caption, self.submit_btn]:
                    widget.destroy()
                    
                self.create_extracted_information_widgets()

                messagebox.showinfo("Extracting", "The operation has been completed successfully.")
            except Exception as e:
                print(e)
                self.perform_extracting_refresh()
                messagebox.showerror("Error", f"Information could not be extracted from the image")

    def display_image(self, photo, frame, label_name):
        if hasattr(self, label_name):
            getattr(self, label_name).destroy()
        new_label = CTkLabel(frame, image=photo, text="")
        warnings.resetwarnings()
        new_label.image = photo
        new_label.grid(row=1, column=0, pady=10, padx=10)

        setattr(self, label_name, new_label)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()    