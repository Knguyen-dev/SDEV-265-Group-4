import customtkinter as ctk # custom tkinter gui library  
import importlib # For importing pages 
import datetime # For creating a dynamic footer 
# Import sqlalchemy to do our operations
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# Import the AI model
from ai import StoryGPT 

# importing user so we don't have to log in everytime for testing
# from classes.models import User

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
		self.master = master
		super().__init__(self.master, fg_color=self.master.subFGCLR, corner_radius=0)
		navbar = ctk.CTkFrame(self, fg_color="transparent")
		navLabel = ctk.CTkLabel(navbar, text="Welcome to BookSmart.AI!", text_color=self.master.textCLR, font=("Helvetica", 32))
		navBtnFrame = ctk.CTkFrame(navbar, fg_color="transparent")

		# List of all buttons in the navbar
		self.navBtns = [] 



		# Map specifically used for creating buttons that redirect the user to other pages
		self.navBtnMap = { 
			"Home": "homePage",
			"AI Settings": "AISettingsPage",
			"Library": "storyLibraryPage",
			"My Account": "userAccountPage",
		}
		colCount = 0
		for key in self.navBtnMap:
			navBtn = ctk.CTkButton(navBtnFrame, corner_radius=0, fg_color=self.master.btnFGCLR, hover_color=self.master.btnHoverCLR, text=f"{key}", text_color=self.master.textCLR, command=lambda k=key:self.master.openPage(self.navBtnMap[k])) #type: ignore
			navBtn.grid(row=0, column=colCount, padx=10)
			colCount += 1
			self.navBtns.append(navBtn)

		# Create nav button that toggles the theme
		toggleThemeBtn = ctk.CTkButton(navBtnFrame, corner_radius=0, fg_color=self.master.btnFGCLR, hover_color=self.master.btnHoverCLR, text="Toggle Theme", text_color=self.master.textCLR, command=self.master.toggleTheme)
		toggleThemeBtn.grid(row=0, column=colCount+1, padx=10)
		self.navBtns.append(toggleThemeBtn)


		# Structure remaining elements
		navbar.pack(expand=True)
		navLabel.grid(row=0, column=0,)
		navBtnFrame.grid(row=1, column=0, pady=20, sticky='ns')

		# Adjust nav buttons based on user's state. On load, the user isn't logged in, so calling this would 
		# correctly disable the nav buttons until the user logged in.
		self.updateNavButtons()
	

	def updateNavButtons(self):
		'''
		- Update the navigation buttons based on the user's login state.
		If the user is logged in:
		1. Enable all navigation buttons.
		2. Allow users to click on the buttons to navigate to their respective places.

		Else the user is not logged in:
		1. Disable all navigation buttons that aren't the toggle theme button.
		2. Prevent users from clicking on those buttons, ensuring they cannot navigate to other pages until they log in.

		NOTE: 
		- The toggleThemeBtn is special as, it shouldn't be disabled even when the user 
			is logged out. So we make sure that we exclude it from being disabled. However we 
			will leave it so that this function can enable this button again in case it 
			was disabled by disableNavButtons.

		- The reason toggleThemeBtn is also going to be disabled by disableNavButtons is 
			because toggling the theme re-renders the page. Having a re-render happen when 
			the ai api is generating a message could break application.
		'''
		for button in self.navBtns:
			if (self.master.loggedInUser): #type: ignore
				button.configure(state="standard")
			elif button.cget("text") != "Toggle Theme":
				button.configure(state="disabled")
		
	
	def disableNavButtons(self):
		'''Disables all nav buttons'''
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
		self.master = master
		# Put header in master frame
		super().__init__(self.master, fg_color=self.master.subFGCLR, corner_radius=0)
		currentYear = datetime.datetime.now().year
		footerLabel = ctk.CTkLabel(self, text=f"BookSmart {currentYear}", text_color=self.master.textCLR, font=("Helvetica", 16))
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

		'''
		- currentPage: Tkinter frame class representing the current page the user is on
		- loggedInUser: User object that represents the user that's currently logged into the application
		- currentStory: Current story object that the user has selected and is editing with. 
			Useful for rendering the saved messages for a selected story.
		- isSavedStory: Boolean indicating whether the story the user is on is already saved into the database or not
		- isRemixedStory: Boolean indicating whether the stor ythe user is writing is a remix
		- unsavedStoryMessages: Array of message objects that represent the messages that the 
			user and ai have written that haven't been saved into a story yet
		- storyGenObj: Generator object that will yield the AI's response message to the user's query
		
		- remixStoryObj: Story object that the user is planning to make a remix on.
			It's useful to store this in Main, as the user may want to toggle the theme, which'll reload 
			the page. So we need that same story they wanted to remix when reloading
		'''
		self.currentPage = None
		self.loggedInUser = None 
		self.currentStory = None
		self.isSavedStory = False
		self.isRemixedStory = False
		self.unsavedStoryMessages = []
		self.storyGenObj = None
		self.remixStoryObj = None


		self.isDarkTheme = True
		self.appColors = {
			"dark_slate": "#0f172a",
			"dark_gray": "#030712",
			"medium_gray": "#374151",
			"light_gray": "#9ca3af",
			"white": "#FFFFFF",
			"black": "#000000",
			"light_emerald": "#34d399",
			"light_blue": "#4267B2",
		}

		# Color of backround
		self.mainFGCLR = ""
		# Color of page content container
		self.subFGCLR = ""
		# Color of text
		self.textCLR = ""
		# Color of the entry widgets 
		self.entryFGCLR = ""
		# Color of text in entry widgets
		self.entryTextCLR = ""

		# Color of buttons
		self.btnFGCLR = ""
		self.btnHoverCLR = ""

		# Engine and session constructor that we're going to use 
		self.engine = create_engine("sqlite:///assets/PyProject.db")
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

		# Log in a knguyen44 for developing purposes, no need to login everytime
		# self.loggedInUser = self.session.query(User).filter_by(username="knguyen44").first()

		# Apply theme of application now
		self.applyTheme()

		# Call function to create navbar
		self.header = Header(self)
		self.header.pack(side="top", fill="x")
		self.footer = Footer(self)
		self.footer.pack(fill="x", side="bottom")

		# On load in, direct to AIChatPage for development puropsees with the prompt engineering
		self.openPage("userLoginPage")

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
	1. pageName: The name of the class for the page that's being opened
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

		
	def reloadCurrentPage(self):
		'''Re opens the current page; best used in conjunction with render and toggle theme functions'''
		# Replace old header and footer with new header and footer because 
		self.header.pack_forget()
		self.footer.pack_forget()
		self.header = Header(self)
		self.header.pack(side="top", fill="x")
		self.footer = Footer(self)
		self.footer.pack(fill="x", side="bottom")

		# Re-opens the current page
		pageName = self.currentPage.__class__.__name__
		self.openPage(pageName)


	def applyTheme(self):
		'''Applies color changes to the application'''
		if (self.isDarkTheme):
			self.mainFGCLR = self.appColors["dark_gray"]
			self.subFGCLR = self.appColors["dark_slate"]
			self.textCLR = self.appColors["white"]
			self.entryFGCLR = self.appColors["medium_gray"]
			self.entryTextCLR = self.appColors["white"]
			self.btnFGCLR = self.appColors["light_gray"]
			self.btnHoverCLR = self.appColors["light_blue"]
			ctk.set_appearance_mode("Dark")
		else:
			self.mainFGCLR = self.appColors["white"]
			self.subFGCLR = self.appColors["light_gray"]
			self.textCLR = self.appColors["white"]
			self.entryFGCLR = self.appColors["white"]
			self.entryTextCLR = self.appColors["black"]
			self.btnFGCLR = self.appColors["light_blue"]
			self.btnHoverCLR = self.appColors["light_emerald"]
			ctk.set_appearance_mode("Light")

	def toggleTheme(self):
		'''Toggles theme of the application and reloads the page to show the changes '''
		self.isDarkTheme = not (self.isDarkTheme)
		self.applyTheme()
		self.reloadCurrentPage()
		
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