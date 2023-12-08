import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk

'''
+ userAccountPage: Frame that represents the user's profile or account page. A page where the user can see all of 
	their public account information such as their username, profile picture, etc.

Constructor:
- master: 'App' class instance from 'Main.py'

Attributes/Variables:
- master: 'App' class instance from 'Main.py'
- innerPageFrame (CTkFrame): Container for all of the page's widgets
- userImageSection (CTkFrame): Section that contains the user's image
- avatarSourcePath (string): Path to the image folder from script's directory.
- image: PIL image object
- imageWidget (ImageTk): Tkinter widget that holds the image
- ImageLabel (tk.Label): Label that displays the widget
- userBtnsSection (CTkFrame): Container that holds all of the buttons for the page
- openEditAvatarBtn (CTkButton): Button that redirects the user to the editAvatarPage
- openEditAccountBtn (CTkButton): Button that redirects the user to the editAccountPage
- confirmLogOutBtn (CTkButton): Button that logs out the user
- userInfoSection (CTkFrame): Section that contains the labels that show the user's public information.
- userInfoFields (array): Array that's used to create the labels that show the user's information.
'''
class userAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		# This extra frame just allows stuff to be centered onto the userAccountPage frame
		innerPageFrame = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		innerPageFrame.pack(expand=True)
		# Create section to store the user's profile picture
		userImageSection = tk.Canvas(innerPageFrame)
		
		avatarSourcePath = f"./assets/images/profile_pics/{self.master.loggedInUser.avatar}"
		image = Image.open(avatarSourcePath).resize((300, 300))
		imageWidget = ImageTk.PhotoImage(image=image)
		imageLabel = tk.Label(userImageSection, image=imageWidget)
		imageLabel.image = imageWidget #type: ignore
		imageLabel.grid(row=0, column=0)

		# Create section to store buttons on the user page
		userBtnsSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		openEditAvatarBtn = ctk.CTkButton(userBtnsSection,  text="Edit Avatar", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("editAvatarPage")) #type: ignore
		openEditAccountBtn = ctk.CTkButton(userBtnsSection,  text="Edit Account", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("editAccountPage")) #type: ignore
		confirmLogOutBtn = ctk.CTkButton(userBtnsSection,  text="Log Out", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.master.confirmLogout)
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
			label = ctk.CTkLabel(userInfoSection, text_color=self.master.theme["label_clr"], text=f"{userInfoFields[x].get('text')}: {userInfoFields[x].get('value')}", font=("Helvetica", 24))
			label.grid(row=x, column=0, sticky="W", pady=10)

		# Structure the 3 main sections of the user account page
		userImageSection.grid(row=0, column=0, padx=30, pady=10)
		userBtnsSection.grid(row=1, padx=30, column=0)
		userInfoSection.grid(row=0, column=1, padx=30)