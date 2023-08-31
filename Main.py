# For loading different pages 
import importlib

# Tkinter itself
import tkinter as tk
import customtkinter as ctk 

# Import our models
from classes.models import *

# Import sqlalchemy to do our operations
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# For creating a dynamic footer 
import datetime



ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"

# Header class that has a navbar
class Header(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		self.master = master
		
		# Create the navbar
		navbar = ctk.CTkFrame(self, fg_color="transparent")
		navbar.pack(expand=True)

		# Create header message 
		welcomeLabel = ctk.CTkLabel(navbar, text="Welcome to BookSmart.AI!", text_color="black", font=("Helvetica", 32))
		
		# Create frame for nav buttons
		navBtnFrame = ctk.CTkFrame(navbar, fg_color="transparent")
		self.navBtns = [] # List for all nav buttons
		self.navBtnMap = { # Create nav buttons with iteration
			"Home": "homePage",
			"AI Settings": "aiSettingsPage",
			"Library": "storyLibraryPage",
			"My Account": "userAccountPage",
		}
		colCount = 0
		for key in self.navBtnMap:
			navBtn = ctk.CTkButton(navBtnFrame, corner_radius=0, text=f"{key}", command=lambda k=key:self.master.openPage(self.navBtnMap[k])) #type: ignore
			navBtn.grid(row=0, column=colCount, padx=10)
			colCount += 1
			self.navBtns.append(navBtn)

		# Structure remaining elements
		welcomeLabel.grid(row=0, column=0)
		navBtnFrame.grid(row=1, column=0, pady=20)

		# Adjust nav button links depending on user login state
		self.updateNavButtons()

	'''
	- Update the nav buttons based on the login state of the user
	1. If user is logged in, nav buttons lead to their respective places
	2. Else: Make all nav buttons lead to login page, ensuring that the user must log in before accessing the application
	'''
	def updateNavButtons(self):
		i = 0
		for key in self.navBtnMap:
			if (self.master.loggedInUser): #type: ignore
				self.navBtns[i].configure(command=lambda:self.master.openPage(self.navBtnMap[key])) #type: ignore
			else:
				self.navBtns[i].configure(command=lambda:self.master.openPage("userLoginPage")) #type: ignore
			i += 1
			
# Footer frame
class Footer(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		currentYear = datetime.datetime.now().year
		footerLabel = ctk.CTkLabel(self, text=f"BookSmart {currentYear}", text_color="black",	font=("Helvetica", 16))
		footerLabel.pack()

# Main application
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("BookSmart.Ai")
		self.width = self.winfo_screenwidth()
		self.height = self.winfo_screenheight()
		self.geometry(f"{self.width}x{self.height}")

		# Attribute to keep track of the current page
		self.currentPage = None
		self.loggedInUser = None		

		# Engine and session constructor that we're going to use 
		self.engine = create_engine("sqlite:///assets/PyProject.db", echo=True)
		self.Session = sessionmaker(bind=self.engine)



		# Call function to create navbar
		self.header = Header(self)
		self.header.pack(side="top", fill="x")

		footer = Footer(self)
		footer.pack(fill="x", side="bottom")

		# Open the page you want, probably the home page, which would be the ai story, which is a good 
		# candidate for being the homePage
		self.openPage("userRegisterPage")


	def loadPage(self, pageName):
		try:
			module = importlib.import_module(f"pages.{pageName}")
			pageClass = getattr(module, pageName)
			return pageClass		
		except (ImportError, AttributeError):
			print(f"Error: Page {pageName} wasn't found.")
			return None
		
	def openPage(self, pageName, *args):
		pageClass = self.loadPage(pageName)
		if pageClass is None:
			return
		if self.currentPage:
			self.currentPage.destroy()
		self.currentPage = pageClass(self, *args)
		self.currentPage.pack(fill="both", expand=True)

if __name__ == "__main__":
	app = App()
	app.mainloop()