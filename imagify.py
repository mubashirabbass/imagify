import requests
import os
import uuid
import concurrent.futures
from threading import Thread
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import io
from datetime import datetime

class ImagifyDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Imagify - Image Downloader")
        self.geometry("800x650")
        self.minsize(700, 600)
        
        # Appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.search_term = ctk.StringVar()
        self.image_count = ctk.StringVar(value="10")
        self.save_location = ctk.StringVar()
        self.downloading = False
        self.downloaded_count = 0
        self.current_image_preview = None
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(5, weight=1)
        
        # Header Frame with Logo
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(10,0))
        
        # Logo and Welcome Message
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="🖼️ Imagify",
            font=ctk.CTkFont(size=28, weight="bold"),
            compound="left"
        )
        self.logo_label.pack(pady=(10,5))
        
        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text="Download high-quality images with ease",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray40")
        )
        self.welcome_label.pack(pady=(0,15))
        
        # Search Term
        self.search_label = ctk.CTkLabel(self, text="Search for images:", anchor="w")
        self.search_label.grid(row=1, column=0, padx=20, pady=(10,5), sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_term,
            placeholder_text="e.g. 'nature', 'animals', 'technology'",
            height=40,
            border_width=2,
            corner_radius=10
        )
        self.search_entry.grid(row=1, column=1, padx=20, pady=(10,5), sticky="ew")
        
        # Image Count Entry
        self.count_label = ctk.CTkLabel(self, text="Number of images (1-1000):", anchor="w")
        self.count_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.count_entry = ctk.CTkEntry(
            self,
            textvariable=self.image_count,
            placeholder_text="Enter number (1-1000)",
            height=40,
            width=100,
            corner_radius=10
        )
        self.count_entry.grid(row=2, column=1, padx=20, pady=5, sticky="w")
        
        # Save Location
        self.location_label = ctk.CTkLabel(self, text="Save location:", anchor="w")
        self.location_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.location_entry = ctk.CTkEntry(
            self,
            textvariable=self.save_location,
            state="readonly",
            height=40,
            corner_radius=10
        )
        self.location_entry.grid(row=3, column=1, padx=(20,5), pady=5, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(
            self,
            text="Browse",
            width=80,
            height=40,
            command=self.browse_location
        )
        self.browse_btn.grid(row=3, column=1, padx=(5,20), sticky="e")
        
        # Image Preview Frame
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Image preview will appear here",
            font=ctk.CTkFont(size=12),
            fg_color=("gray90", "gray20"),
            corner_radius=8
        )
        self.preview_label.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Progress Frame
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=(0,10), sticky="nsew")
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.progress_label.pack(pady=(10,5), padx=20, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=12, corner_radius=6)
        self.progress_bar.pack(pady=5, padx=20, fill="x")
        self.progress_bar.set(0)
        
        self.progress_percent = ctk.CTkLabel(
            self.progress_frame,
            text="0% (0/0)",
            font=ctk.CTkFont(size=12),
        )
        self.progress_percent.pack(pady=(5,10))
        
        # Download Button with counter
        self.download_btn = ctk.CTkButton(
            self,
            text="Download Images (0/0)",
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.start_download
        )
        self.download_btn.grid(row=6, column=0, columnspan=2, padx=20, pady=(5,10), sticky="ew")
        
        # Footer with copyright
        self.footer_label = ctk.CTkLabel(
            self,
            text=f"© {datetime.now().year} Developed By: Mubashir Abbas - All rights reserved",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray40")
        )
        self.footer_label.grid(row=7, column=0, columnspan=2, pady=(0,10))
        
        # Appearance mode menu
        self.appearance_menu = ctk.CTkOptionMenu(
            self,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode,
            width=100
        )
        self.appearance_menu.grid(row=7, column=1, padx=20, pady=(0,10), sticky="e")
        
    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)
        
    def browse_location(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.save_location.set(folder_selected)
    
    def start_download(self):
        if not self.search_term.get():
            messagebox.showerror("Error", "Please enter a search term")
            return
            
        if not self.save_location.get():
            messagebox.showerror("Error", "Please select a save location")
            return
            
        try:
            self.target_count = int(self.image_count.get())
            if self.target_count < 1 or self.target_count > 1000:
                messagebox.showerror("Error", "Please enter a number between 1 and 1000")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
            
        if self.downloading:
            return
            
        self.downloading = True
        self.downloaded_count = 0
        self.download_btn.configure(state="disabled", text=f"Downloading (0/{self.target_count})")
        self.progress_bar.set(0)
        self.progress_percent.configure(text=f"0% (0/{self.target_count})")
        self.progress_label.configure(text="Starting download...")
        self.preview_label.configure(image=None, text="Downloading images...")
        
        # Start download in a separate thread
        Thread(target=self.download_images, daemon=True).start()
    
    def download_images(self):
        try:
            subscription_key = "Your api key "
            search_url = "https://api.bing.microsoft.com/v7.0/images/search"
            headers = {"Ocp-Apim-Subscription-Key": subscription_key}
            params = {
                "q": self.search_term.get(),
                "count": self.target_count,
                "offset": 0,
                "mkt": "en-US",
                "safesearch": "Moderate"
            }
            
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()
            
            image_urls = [img["contentUrl"] for img in search_results["value"]]
            total_images = len(image_urls)
            
            # Download images with thread pool
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for i, url in enumerate(image_urls):
                    futures.append(executor.submit(self.save_image, url, i+1, total_images))
                    
                for future in concurrent.futures.as_completed(futures):
                    try:
                        img_data, img_path = future.result()
                        if img_data:
                            # Convert to CTkImage
                            img = Image.open(io.BytesIO(img_data))
                            img.thumbnail((300, 300))
                            ctk_img = ctk.CTkImage(light_image=img, size=(300, 300))
                            
                            self.downloaded_count += 1
                            progress = self.downloaded_count / total_images
                            self.update_progress(
                                progress,
                                f"Downloaded {self.downloaded_count} of {total_images}",
                                ctk_img
                            )
                    except Exception as e:
                        print(f"Error downloading image: {e}")
            
            self.update_progress(
                1, 
                f"Successfully downloaded {self.downloaded_count} images", 
                None
            )
            messagebox.showinfo(
                "Success", 
                f"Download completed!\n{self.downloaded_count} images saved to:\n{self.save_location.get()}"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.update_progress(0, "Download failed", None)
        finally:
            self.downloading = False
            self.download_btn.configure(state="normal", text=f"Download Images (0/{self.target_count})")
    
    def save_image(self, url, image_num, total_images):
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Read image data
            img_data = response.content
            
            # Generate filename
            img_name = f"image_{image_num}.jpg"
            save_path = os.path.join(self.save_location.get(), img_name)
            
            with open(save_path, 'wb') as img_file:
                img_file.write(img_data)
                
            return (img_data, save_path)
            
        except Exception as e:
            print(f'Error downloading {url}: {e}')
            return (None, None)
    
    def update_progress(self, progress, text, ctk_img):
        downloaded = self.downloaded_count
        self.progress_bar.set(progress)
        self.progress_percent.configure(text=f"{int(progress*100)}% ({downloaded}/{self.target_count})")
        self.progress_label.configure(text=text)
        self.download_btn.configure(text=f"Downloading ({downloaded}/{self.target_count})")
        
        if ctk_img:
            try:
                self.preview_label.configure(
                    image=ctk_img, 
                    text="",
                    compound="center"
                )
                self.preview_label.image = ctk_img
            except Exception as e:
                print(f"Error updating preview: {e}")

if __name__ == "__main__":
    app = ImagifyDownloader()
    app.mainloop()