from customtkinter import *
from PIL import Image, ImageTk
import os, asyncio, requests,re
from tkinter import filedialog
from get_board import run

 
class myBoard:
    def __init__(self):
        self.start_arg = ''
        self.app = CTk()
        self.main_widgets = {}
        self.__layout()
        self.status = ''
        self.app.mainloop()
    
   

    def open_filesystem(self):
        # open and collect desired directory
        self.main_widgets["directory"] = filedialog.askdirectory(title="Select a Folder")
        
    def reach_pinterest(self):
        
        url = self.main_widgets["link_entry"].get()

        # Verify url
        url_regex = re.compile(r'^(https?://)'
                               r'(www\.)?'
                               r'pinterest\.com/'
                               r'[^/]+/'
                               r'[^/]+/$',
                               re.IGNORECASE)
        if not bool(url_regex.match(url)):
            print("Invalid url!")
            return 
        
        url_list = asyncio.run(run(url))
        
        # Download Images
        for i, url in enumerate(url_list):
            self.download_img(url, i)

    def download_img(self, url, i):
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            new_path = f'{self.main_widgets["directory"]}/{self.main_widgets["name_img_entry"].get()}_{i}.jpg'
            with open(new_path, "wb") as img_file:
                img_file.write(response.content)
                self.main_widgets["scrollable_images"].add_images(new_path)

        except FileNotFoundError:
            print(f"Invalid folder path: {self.folder_path}")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

    def __layout(self):
        # Create app
        app = self.app
        app.grid_rowconfigure(0, weight=1)
        app.grid_rowconfigure(1, weight=1)
        app.grid_rowconfigure(2, weight=1)
        app.grid_rowconfigure(3, weight=1)
        app.grid_rowconfigure(4, weight=1)

        app.grid_columnconfigure(0, weight=0)
        app.grid_columnconfigure(1, weight=1)
        app.grid_columnconfigure(2, weight=1)
        app.grid_columnconfigure(3, weight=1)

        # resizing
        app.geometry("750x500")
        app.title("Image Collector")
        set_appearance_mode("light")

        # Entry for link
        link_entry = CTkEntry(master=self.app, placeholder_text="Pinterest board link", width=350, corner_radius=20)
        link_entry.grid(row=0,column=1, pady=0, padx=25 ,sticky="swe", columnspan=2)
        self.main_widgets["link_entry"] = link_entry
        
        
        # Search button
        search_btn = CTkButton(self.app, fg_color="#D71449",hover_color="#C01745" ,border_color="black", text="Collect", 
                                text_color="white", command=self.reach_pinterest, height=20, width=100 ,corner_radius=30,)
        search_btn.grid(row=0, column=3, sticky="sw")

        # Button to select folder
        select_foleder_btn = CTkButton(self.app, fg_color="#D71449", text="open folder", corner_radius=7, height=8, command=self.open_filesystem)
        select_foleder_btn.grid(row=1, column=1, ipadx=10,pady=5, padx=35, sticky="ew")
        name_img_entry = CTkEntry(self.app, placeholder_text="names", corner_radius=30, height=8,fg_color="#f0f0f0",  # Background color
            text_color="#333333")
        name_img_entry.grid(row=1, column=2, pady=5, sticky="w")
        self.main_widgets["name_img_entry"] = name_img_entry

        # Status label (Not in Use)
        status_label = CTkLabel(app,text='')
        status_label.grid(row=2, column=3, sticky ="sw",padx=10)
        self.main_widgets["status_label"] = status_label

        scrollable_frame = ImageScrollableFrame(self.app)
        self.main_widgets["scrollable_images"] = scrollable_frame

        # Logo
        img = Image.open("pinterest.png")
        img = img.resize((500,400))
        pinterest_img =CTkImage(img)

        #Enable column and row Growth
        img_label = CTkLabel(self.app, image=pinterest_img,text="", height=15)
        img_label.grid(row=0,column=0,sticky="n", padx=10,pady=10)
        
 
        
class ImageScrollableFrame:
    def __init__(self,app):
        self.app = app
        self.scrollable_frame = CTkScrollableFrame(app,width=400,height=200)
        self.scrollable_frame.grid(row=3,column=1, columnspan=3, sticky="nsew", padx=40)
        self.img_list = []
        # Set 
        for i in range(4):   
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
            self.scrollable_frame.grid_rowconfigure(i, weight=1)

    def add_images(self, img_path):
        
        # Get image number from path

        img_ = os.path.splitext(img_path)[0]
        img_ = img_.strip('.jpg')
        match = re.search(r'_(\d+)$', img_)

        if match:
            number = int(match.group(1))
        else:
            number = int(img_[-1])

        # Add image to Frame
        img = Image.open(img_path) 
        img_ctk  = ImageTk.PhotoImage(img)
        img_label = CTkLabel(self.scrollable_frame, image=img_ctk, text="", corner_radius=55)
        img_label.image = img_ctk
        img_label.grid(row=(number // 4) ,column=(number % 4),padx=12,pady=12, sticky="nsew")
        self.img_list.append(img_ctk)
        
if __name__ == "__main__":
    myBoard()