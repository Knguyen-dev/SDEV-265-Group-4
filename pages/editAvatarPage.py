import customtkinter as ctk
import tkinter as tk
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
		
		self.imageFolderPath = "./assets/images/" # Path to image folder relative to our script file
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
		prevImageBtn = ctk.CTkButton(imageBtnsSections, text="Previous", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.loadPreviousImage)
		nextImageBtn = ctk.CTkButton(imageBtnsSections, text="Next", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.loadNextImage)
		selectImageBtn = ctk.CTkButton(imageBtnsSections, text="Select", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.changeAvatar)

		# Structure the widgets 
		innerPageFrame.pack(expand=True)
		header.grid(row=0, column=0, pady=10)
		heading.grid(row=0, column=0)

		self.imageLabel.grid(row=1, column=0, pady=10)

		imageBtnsSections.grid(row=2, column=0, pady=10)
		prevImageBtn.grid(row=0, column=0, padx=10)
		nextImageBtn.grid(row=0, column=1, padx=10)
		selectImageBtn.grid(row=0, column=2, padx=10)

		# Load the current image onto the screen
		self.loadCurrentImage()

	# Returns the paths of all of the image files in a list
	def getImageFileNames(self):
		fileNames = os.listdir(self.imageFolderPath) 
		return [fileName for fileName in fileNames]
		
	# Loads the current image onto the screen
	def loadCurrentImage(self):
		# Put new image on the label to display it
		newImage = ImageTk.PhotoImage(Image.open(f"{self.imageFolderPath}{self.imageList[self.imageIndex]}").resize((300, 300))) 
		self.imageLabel.configure(image=newImage)
		self.imageLabel.image = newImage #type: ignore

		# Update the file name of the current image
		self.currentImageFileName = self.imageList[self.imageIndex]

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


	# Changes the avatar of the currently logged in user
	def changeAvatar(self):
		# Update the avatar attribute with the image's file name, and persist that change to the database
		self.master.loggedInUser.avatar = self.currentImageFileName #type: ignore
		self.master.session.commit() # type: ignore

		# Redirect the user to the account page to make sure they see their changess
		self.master.openPage("userAccountPage") #type: ignore