import tkinter as tk
import customtkinter as ctk

# For images
from PIL import Image, ImageTk
from urllib.request import urlopen
import io


# Section that contains the user's profile picture 
class userImageFrame(tk.Canvas):
	def __init__(self, master):
		super().__init__(master, highlightbackground="#eee", highlightthickness=1)
		self.master = master

		userImageSource = "https://st3.depositphotos.com/1767687/16607/v/600/depositphotos_166074422-stock-illustration-default-avatar-profile-icon-grey.jpg"

		# Open url, do an http request, to the website that hosts the image
		response = urlopen(userImageSource)
		# Read image data, which gets us a binary object (blob), that represents image
		imageData = response.read()
		# Create PIL image object from binary image data
		image = Image.open(io.BytesIO(imageData)).resize((325, 325))
		
		# Turn PIL image into Tkinter image object
		image = ImageTk.PhotoImage(image=image)

		# Put tkinter image object in a label to display image; need image attribute twice to keep it displayed
		imageLabel = tk.Label(self, image=image)
		imageLabel.image = image #type: ignore
		imageLabel.grid(row=0, column=0)

# Section that contains buttons for interacting with a user's account, editing account, logging out, etc.
class userAccountPanel(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="transparent")
		self.master = master

		self.openEditAccountBtn = ctk.CTkButton(self, text="Edit Account", command=lambda: self.master.openPage("userEditPage")) #type: ignore
		self.confirmLogOutBtn = ctk.CTkButton(self, text="Log Out")
		self.openDeleteAccountBtn = ctk.CTkButton(self, text="Delete Account", command=lambda: self.master.openPage("userDeletePage")) #type: ignore

		self.openEditAccountBtn.grid(row=0, column=0, pady=5)
		self.confirmLogOutBtn.grid(row=1, column=0, pady=5)
		self.openDeleteAccountBtn.grid(row=2, column=0, pady=5)

# A section that contains public user information such as username, email, first/last name, etc.
class userInfoPanel(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="transparent")
		self.master = master
		userInfoFields = [
			{
				"text": "Username",
				"value": "SomeUserName"
			},
			{
				"text": "Email",
				"value": "SomeUserName@gmail.com"
			},
			{
				"text": "Name",
				"value": "SomeFirstName SomeLastName"
			}
		]
		for x in range(len(userInfoFields)):
			label = ctk.CTkLabel(self, text=f"{userInfoFields[x].get('text')}: {userInfoFields[x].get('value')}", font=("Helvetica", 24))
			label.grid(row=x, column=0, sticky="W", pady=10)
			
		
class userAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# This extra frame just allows stuff to be centered onto the userAccountPage frame
		innerPageFrame = ctk.CTkFrame(self, fg_color="transparent")
		innerPageFrame.pack(expand=True)

		userImageSection = userImageFrame(innerPageFrame)
		userBtnSection = userAccountPanel(innerPageFrame)
		userInfoSection = userInfoPanel(innerPageFrame)

		userImageSection.grid(row=0, column=0, padx=30, pady=10)
		userBtnSection.grid(row=1, padx=30, column=0)
		userInfoSection.grid(row=0, column=1, padx=30)
		


