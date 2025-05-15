import os
import yt_dlp as youtube_dl
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Audio Downloader")
        self.geometry("500x400")
        
        # Initialize variables
        self.download_path = tk.StringVar()
        self.download_path.set(os.path.expanduser("~"))  # Default path
        
        # Set up background image label (this will be behind all widgets)
        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Hardcoded background image path
        self.background_image_path = "/home/oem/YTDLaudioOnly/chibiaudioonlyytdl.png"  # Replace with your image path
        self.load_background_image()  # Load the background image on startup
        
        # Create UI components directly on the main window
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Enter YouTube URL:", bg="lightgrey").pack(pady=5)
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.pack(pady=5)

        tk.Label(self, text="Download Path:", bg="lightgrey").pack(pady=5)
        tk.Entry(self, textvariable=self.download_path, width=50).pack(pady=5)
        path_button = tk.Button(self, text="Choose Folder", command=self.choose_path, bg="lightgrey")
        path_button.pack(pady=5)

        download_button = tk.Button(self, text="Download Audio", command=self.download_audio, bg="lightgrey")
        download_button.pack(pady=20)

        self.status_label = tk.Label(self, text="", wraplength=400, bg="lightgrey")
        self.status_label.pack(pady=10)

    def load_background_image(self):
        """Load the background image from the hardcoded path."""
        try:
            img = Image.open(self.background_image_path)
            bg_img = ImageTk.PhotoImage(img.resize((500, 400), Image.LANCZOS))
            self.background_label.config(image=bg_img)
            self.background_label.image = bg_img  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

    def choose_skin(self):
        # Open file dialog to select an image
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.background_image_path = image_path  # Update the path
            self.load_background_image()  # Load the new background image

    def choose_path(self):
        # Open folder dialog to set download path
        path = filedialog.askdirectory()
        if path:
            self.download_path.set(path)

    def download_audio(self):
        # Get URL and download path
        url = self.url_entry.get()
        path = self.download_path.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return

        self.status_label.config(text="Downloading audio...")  # Update status
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        # Download audio
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Audio downloaded successfully!")
            messagebox.showinfo("Success", "Audio downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download audio: {e}")
            self.status_label.config(text="")

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
