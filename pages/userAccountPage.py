import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

##### The user account or profile page#####
class userAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		# This extra frame just allows stuff to be centered onto the userAccountPage frame
		innerPageFrame = ctk.CTkFrame(self, fg_color="transparent")
		innerPageFrame.pack(expand=True)
		# Create section to store the user's profile picture
		userImageSection = tk.Canvas(innerPageFrame, highlightbackground="#eee", highlightthickness=1)
		
		avatarSourcePath = f"./assets/images/{self.master.loggedInUser.avatar}"
		image = Image.open(avatarSourcePath).resize((300, 300))
		imageWidget = ImageTk.PhotoImage(image=image)
		imageLabel = tk.Label(userImageSection, image=imageWidget)
		imageLabel.image = imageWidget #type: ignore
		imageLabel.grid(row=0, column=0)

		# Create section to store buttons on the user page
		userBtnsSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		openEditAvatarBtn = ctk.CTkButton(userBtnsSection, text="Edit Avatar", command=lambda: self.master.openPage("editAvatarPage")) #type: ignore
		openEditAccountBtn = ctk.CTkButton(userBtnsSection, text="Edit Account", command=lambda: self.master.openPage("editAccountPage")) #type: ignore
		confirmLogOutBtn = ctk.CTkButton(userBtnsSection, text="Log Out", command=self.master.logoutUser)
		openEditAvatarBtn.grid(row=0, column=0, pady=5)
		openEditAccountBtn.grid(row=1, column=0, pady=5)
		confirmLogOutBtn.grid(row=2, column=0, pady=5)

		# Create section to display user information
		# Get user information, and iteratively create labels to show that user information
		userInfoSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		userInfoFields = [
			{
				"text": "Username",
				"value": self.master.loggedInUser.username
			},
			{
				"text": "Email",
				"value": self.master.loggedInUser.email
			},
			{
				"text": "Name",
				"value": f"{self.master.loggedInUser.firstName} {self.master.loggedInUser.lastName}"
			}
		]
		for x in range(len(userInfoFields)):
			label = ctk.CTkLabel(userInfoSection, text=f"{userInfoFields[x].get('text')}: {userInfoFields[x].get('value')}", font=("Helvetica", 24))
			label.grid(row=x, column=0, sticky="W", pady=10)

		# Structure the 3 main sections of the user account page
		userImageSection.grid(row=0, column=0, padx=30, pady=10)
		userBtnsSection.grid(row=1, padx=30, column=0)
		userInfoSection.grid(row=0, column=1, padx=30)