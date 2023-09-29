import customtkinter as ctk # custom tkinter gui library  
import importlib # For importing pages 
import datetime # For creating a dynamic footer 
# Import sqlalchemy to do our operations
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# Import the AI model
from ai import StoryGPT 

# importing user so we don't have to log in everytime for testing
from classes.models import User


ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"

'''
+ Header: Tkinter frame that represents the header of the application 

Constructor:
- master (App): 'App' Class instance

Attributes/Variables:
- master (App): 'App' class instance
- navbar (CTkFrame): Inner frame that that contains the label and the contains the container for the nav buttons
- navLabel (CTkLabel): Label that shows the text of the navbar 
- navBtnFrame (CTkFrame): Tkinter frame/container that has the buttons in the nav
- navBtns (Array): List that contains all of the tkinter buttons that are contained in the nav bar
- navBtnMap (Object/Map): Object/map that contains the text of the buttons (keys) and the name of the class/page that 
	the button is linked to. This allows buttons to link open certain pages when clicked

Methods:
- updateNavBtns(self): Adjusts the accessibility of the nav buttons based on their login state. 
- disableNavBtns(self): Disables the nav buttons from being used
'''
class Header(ctk.CTkFrame):
	def __init__(self, master):
		# Put Header in the master frame
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		self.master = master
		navbar = ctk.CTkFrame(self, fg_color="transparent")
		navLabel = ctk.CTkLabel(navbar, text="Welcome to BookSmart.AI!", text_color="black", font=("Helvetica", 32))
		navBtnFrame = ctk.CTkFrame(navbar, fg_color="transparent")
		self.navBtns = [] 
		self.navBtnMap = { 
			"Home": "homePage",
			"AI Settings": "AISettingsPage",
			"Library": "storyLibraryPage",
			"My Account": "userAccountPage",
		}

		# Create nav buttons with iteration and use colCount to put them all in a row
		colCount = 0
		for key in self.navBtnMap:
			navBtn = ctk.CTkButton(navBtnFrame, corner_radius=0, text=f"{key}", command=lambda k=key:self.master.openPage(self.navBtnMap[k])) #type: ignore
			navBtn.grid(row=0, column=colCount, padx=10)
			colCount += 1
			self.navBtns.append(navBtn)

		# Structure remaining elements
		navbar.pack(expand=True)
		navLabel.grid(row=0, column=0)
		navBtnFrame.grid(row=1, column=0, pady=20)

		# Adjust nav buttons based on user's state. On load, the user isn't logged in, so calling this would 
		# correctly disable the nav buttons until the user logged in.
		self.updateNavButtons()
	
	'''
	- Update the navigation buttons based on the user's login state.
	If the user is logged in:
	1. Enable all navigation buttons.
	2. Allow users to click on the buttons to navigate to their respective places.

	If the user is not logged in:
	1. Disable all navigation buttons.
	2. Prevent users from clicking on the buttons, ensuring they cannot navigate to other pages until they log in.
	'''
	def updateNavButtons(self):
		for button in self.navBtns:
			if (self.master.loggedInUser): #type: ignore
				button.configure(state="standard")
			else:
				button.configure(state="disabled")
		
	# Disables nav all nav buttons
	def disableNavButtons(self):
		for button in self.navBtns:
			button.configure(state="disabled")



'''
+ Footer: Tkinter frame that represents the footer of the application

Constructor:
- master (App): 'App' Class instance

Attributes/Variables:
- currentYear (int): Integer that represents the current year 
- footerLabel (CTkLabel): Label that contains the text for the footer
'''
class Footer(ctk.CTkFrame):
	def __init__(self, master):
		# Put header in master frame
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		currentYear = datetime.datetime.now().year
		footerLabel = ctk.CTkLabel(self, text=f"BookSmart {currentYear}", text_color="black",	font=("Helvetica", 16))
		footerLabel.pack()



'''
+ App: Root window of the tkinter or GUI application. It's our Main application window and it contains 
	data that we want to persist through different pages of the application.

Attributes/Variables:
- width (int): The viewport width of the client.
- height (int): The viewport height of the client. 
- currentPage (CTkFrame): The page that the application is currently rendering 
- loggedInUser (User): Represents the user that is currently logged into the application. If no user is logged in then
	this value is None.
- currentStory (Story): Can represent the saved story object that the user is continuing to write, or it represents the story
	that the user is using to remix off of. 
- isSavedStory (Bool): If true, currentStory is the story the user is continuing. Else, this means isRemixed story is True or False
- isRemixedStory (Bool): If true, currentStory is the story the user is using to remix off of. Note as a result their remixed story 
	isn't saved in the database yet. Else, this means isSavedStory is true or false.

NOTE: If both isSavedStory and isRemixedStory are false, then the user is not remixing a story and they aren't continuing a saved story.
	Basically it means the user is writing a brand new story that hasn't been saved into the database yet.

- unsavedStoryMessages (Array): Array of 'Message' objects that the user and AI have generated for a story, but they haven't been
	saved and linked to a story object in the database yet. These would represent the messages in their most recent chat session.
- engine (SqlAlchemy Engine): Sqlalchemy engine object that helps us connect to the database
- Session (SqlAlchemy Session Maker): Customized constructor that makes session objects for our database 
- session (SqlAlchemy Session): Session class instance that's used to interact with the database 
- header (CTkFrame): Header of the application
- footer (CTkFrame): Footer of the application

Methods:
- getPage(self, pageName): Searches for and returns a class/module with name pageName. This class is a tkinter frame and 
	is an individual page in our GUI application. 
- openPage(self, pageName, *args): Opens and loads a page in our tkinter application that has the name pageName.
	It passes, the 'App' class and then any potential arguments that the pageName class may take as parameters
- logoutUser(self): Logs out the currently logged in user from our application.
'''
class App(ctk.CTk):
	def __init__(self):
		# Initialize window and resize it based on the user's viewport width and height
		super().__init__()
		self.title("BookSmart.Ai")
		self.width = self.winfo_screenwidth()
		self.height = self.winfo_screenheight()
		self.geometry(f"{self.width}x{self.height}")

		# AI model class instance that's going to be used throughout the application
		self.storyGPT = StoryGPT()

		# Attribute to keep track of the current page
		self.currentPage = None
		self.loggedInUser = None 
		self.currentStory = None
		self.isSavedStory = False
		self.isRemixedStory = False
		self.unsavedStoryMessages = []
		self.storyGenObj = None

		# Engine and session constructor that we're going to use 
		self.engine = create_engine("sqlite:///assets/PyProject.db")
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

		# Log in a knguyen44 for developing purposes, no need to login everytime
		self.loggedInUser = self.session.query(User).filter_by(username="knguyen44").first()


		# Call function to create navbar
		self.header = Header(self)
		self.header.pack(side="top", fill="x")
		footer = Footer(self)
		footer.pack(fill="x", side="bottom")

		# On load in, direct to AIChatPage for development puropsees with the prompt engineering
		self.openPage("AIChatPage")

	'''
	- Returns a class of a page (a tkinter frame) for the application 
	1. module: Python module/file as an object.
	2. pageClass: A class for a tkinter frame
	'''
	def getPage(self, pageName):
		try:
			# import the module using the path.
			module = importlib.import_module(f"pages.{pageName}")
			# get the page class from the module
			pageClass = getattr(module, pageName)
			return pageClass
		except (ImportError, AttributeError):
			print(f"Error: Page {pageName} does not exist.")
			return None

	
	'''
	- Loads and opens a page with pageName in the tkinter application
	1. pageClass: A class for a tkinter frame
	'''
	def openPage(self, pageName, *args):
		pageClass = self.getPage(pageName)
		# If pageClass doesn't exist, then stop execution
		if not pageClass:
			return
		
		# If there is a currentPage already, destroy it, then reassign it to the new page class
		# We pageClass to create the tkinter frame, and pass in self (App class), and any potential arguments
		if self.currentPage:
			self.currentPage.destroy()
		self.currentPage = pageClass(self, *args)

		# Pack the new page on the screen
		self.currentPage.pack(fill="both", expand=True)
		

	'''
	- Log the current user out of the application.
	'''
	def logoutUser(self):
		# loggedInUser is none because we are logging out the user
		self.loggedInUser = None 
		
		# Wipe currentStory and reset booleans for the new user. This is so the new user starts on a blank slate
		self.unsavedStoryMessages = [] 
		self.currentStory = None
		self.isSavedStory = False
		self.isRemixedStory = False

		# Clear AI knowledge of any stories the user is currently writing, if any, which prevents the user from logging back in and getting unexpected output
		# NOTE: More specifically when they login and 'continue' an unsaved story, it prevents AI from having knowledge of an interaction from another user or session.
		self.storyGPT.clear()

		# Redirect the user to the login page
		self.openPage("userLoginPage")

		# Update nav buttons so that user can't access the pages associated with them
		self.header.updateNavButtons()


# Make it so application can only be run from this file; 'python Main.py'
if __name__ == "__main__":
	app = App()
	app.mainloop()