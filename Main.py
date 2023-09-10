import customtkinter as ctk # custom tkinter gui librar  
import importlib # For importing pages 
import datetime # For creating a dynamic footer 

# Import the user model for development purposes
from classes.models import User
# Import sqlalchemy to do our operations
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"

##### Application Header that has navbar #####
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
			"AI Settings": "AISettingsPage",
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
	2. Else: All nav buttons are disabled, preventing user from traversing to other pages until they log in
	'''
	def updateNavButtons(self):
		for button in self.navBtns:
			if (self.master.loggedInUser): #type: ignore
				button.configure(state="standard")
			else:
				button.configure(state="disabled")

###### Application Footer #####
class Footer(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		currentYear = datetime.datetime.now().year
		footerLabel = ctk.CTkLabel(self, text=f"BookSmart {currentYear}", text_color="black",	font=("Helvetica", 16))
		footerLabel.pack()



##### Main application #####
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("BookSmart.Ai")
		self.width = self.winfo_screenwidth()
		self.height = self.winfo_screenheight()
		self.geometry(f"{self.width}x{self.height}")

		# Attribute to keep track of the current page
		self.currentPage = None

		# If user is logged in, this will be a User class instance, representing 
		# the User that is currently logged into the application
		self.loggedInUser = None 

		# Story object that could be the saved story the user is continuing, or the story that 
		# they're basing a remix off of.
		self.currentStory = None

		# If true, the user is continuing a saved story
		self.isSavedStory = False

		# If true, the user is currently writing a new story, but it's a remix from an existing saved story 
		self.isRemixedStory = False

		# Array that keeps track of the messages in the most recent story or session
		# NOTE: unsavedStoryMessages will continue saving messages even if those messages aren't associated with a story in the database.
		self.unsavedStoryMessages = []

		# Engine and session constructor that we're going to use 
		self.engine = create_engine("sqlite:///assets/PyProject.db", echo=True)
		self.Session = sessionmaker(bind=self.engine)

		# The master session object we'll use throughout the application to interact with the database
		self.session = self.Session()

		# Log into a user for dev purposes
		self.loggedInUser = self.session.query(User).filter_by(username="knguyen44").first()

		# Call function to create navbar
		self.header = Header(self)
		self.header.pack(side="top", fill="x")
		footer = Footer(self)
		footer.pack(fill="x", side="bottom")

		self.openPage("storyLibraryPage")


	# Gets a page or tkinter frame for the application 
	def getPage(self, pageName):
		try:
			# import the module using the full path
			module = importlib.import_module(f"pages.{pageName}")
			# get the page class from the module
			page_class = getattr(module, pageName)
			return page_class
		except (ImportError, AttributeError):
			print(f"Error: Page {pageName} does not exist.")
			return None

	# Loads and opens a page
	def openPage(self, pageName, *args):
		pageClass = self.getPage(pageName)
		if not pageClass:
			return
		if self.currentPage:
			self.currentPage.destroy()
		self.currentPage = pageClass(self, *args)
		self.currentPage.pack(fill="both", expand=True)
		


	# Log the current user out of the application
	def logoutUser(self):
		self.loggedInUser = None # loggedInUser is none because the user is logging out 
		self.currentSavedStory = None # Wipe the saved story that we're currently continuing
		self.unsavedStoryMessages = [] # Reset the messages of the current story
		self.currentRemixedStory = None # Reset remixed story 

		# Just testing this out
		self.currentStory = None
		self.isSavedStory = False
		self.isRemixedStory = False

		# Redirect the user to the login page
		self.openPage("userLoginPage") #type: ignore
		# Update nav buttons so that user can't access the pages associated with them
		self.header.updateNavButtons() #type: ignore



if __name__ == "__main__":
	app = App()
	app.mainloop()