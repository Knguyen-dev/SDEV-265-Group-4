from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog  # Import filedialog
from PIL import Image, ImageTk
import os		

# Now when pathing, we are in a directory above. This lets us more easily 
# access the "images" folder
import sys
sys.path.append("..")

# Page for editing the user's avatar
class editAvatarPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		innerPageFrame = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		
		self.imageFolderPath = "./assets/images/profile_pics/" # Path to image folder relative to our script file
		self.imageIndex = 0 # Index of the current image
		self.imageList = self.getImageFileNames() # list of image file names that we'll use to load images 
		self.currentImageFileName = "" # the file name of the current image file the image slider is on

		# Heading of the page
		header = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		heading = ctk.CTkLabel(header, text="Choose your avatar or pfp", font=("Helvetica", 32), text_color=self.master.theme["label_clr"])

		# Create image label where we'll display the image
		self.imageLabel = tk.Label(innerPageFrame)

		# Create container and buttons for the image slider
		imageBtnsSections = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		prevImageBtn = ctk.CTkButton(imageBtnsSections,  text="Previous", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.loadPreviousImage)
		nextImageBtn = ctk.CTkButton(imageBtnsSections,  text="Next", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.loadNextImage)
		selectImageBtn = ctk.CTkButton(imageBtnsSections,  text="Select", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.changeAvatar)
		chooseFromFileBtn = ctk.CTkButton(imageBtnsSections, text="Choose from File", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.chooseImageFromFileSystem)

		# Structure the widgets 
		innerPageFrame.pack(expand=True)
		header.grid(row=0, column=0, pady=10)
		heading.grid(row=0, column=0)

		self.imageLabel.grid(row=1, column=0, pady=10)

		imageBtnsSections.grid(row=2, column=0, pady=10)
		prevImageBtn.grid(row=0, column=0, padx=10)
		selectImageBtn.grid(row=0, column=1, padx=10)
		nextImageBtn.grid(row=0, column=2, padx=10)
		chooseFromFileBtn.grid(row=0, column=3, padx=10)

		# Load the current image onto the screen
		self.loadCurrentImage()

	# Returns the paths of all of the image files in a list
	def getImageFileNames(self):
		fileNames = os.listdir(self.imageFolderPath) 
		return [fileName for fileName in fileNames]
		
	# Loads the current image onto the screen  
	def loadCurrentImage(self):
		try:
			imagePath = f"{self.imageFolderPath}{self.imageList[self.imageIndex]}"
			newImage = ImageTk.PhotoImage(Image.open(imagePath).resize((300, 300)))
			self.imageLabel.configure(image=newImage)
			self.imageLabel.image = newImage
   
			# Update the file name of the current image
			self.currentImageFileName = self.imageList[self.imageIndex]
		except FileNotFoundError:
			messagebox.showerror("Error", "The image file could not be found.")
			# Handle the error, e.g., by loading a default image or removing the invalid entry

	# Loads the next image
	def loadNextImage(self):
		self.imageIndex += 1
		if (self.imageIndex > len(self.imageList) - 1):
			self.imageIndex = 0
		self.loadCurrentImage()

	# Loads the previous image
	def loadPreviousImage(self):
		self.imageIndex -= 1
		if (self.imageIndex < 0):
			self.imageIndex = len(self.imageList) - 1
		self.loadCurrentImage()

	def chooseImageFromFileSystem(self):
		file_path = filedialog.askopenfilename(title="Select an Image",
											   filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
		if file_path:
			self.currentImageFileName = file_path
			self.loadImageFromFile(file_path)

	def loadImageFromFile(self, file_path):
		newImage = ImageTk.PhotoImage(Image.open(file_path).resize((300, 300)))
		self.imageLabel.configure(image=newImage)
		self.imageLabel.image = newImage

		self.changeAvatar()

	# Changes the avatar of the currently logged in user
	def changeAvatar(self):
		# Update the avatar attribute with the image's file name, and persist that change to the database
		self.master.loggedInUser.avatar = self.currentImageFileName 
		self.master.session.commit() # type: ignore

		# Redirect the user to the account page to make sure they see their changess
		self.master.openPage("userAccountPage") 