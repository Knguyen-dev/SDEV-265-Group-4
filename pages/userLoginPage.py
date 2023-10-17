import customtkinter as ctk
import hashlib
import sys
sys.path.append("..")
from classes.utilities import clearEntryWidgets, isEmptyEntryWidgets, toggleHidden
from classes.models import User

'''
+ userLoginPage: Tkinter frame that represents the login page of the application. This is where users would 
	log into the accounts that they've created/registered.

Constructor:
- master: 'App' class instance from 'Main.py'

Attributes/Variables:
- master (App): App class from 'Main.py'
- form (CTkFrame): Tkinter frame that contains all of the widgets for the form
- formHeader (CTkFrame): Header of the form 
- formheading (CTkLabel): Heading message for the form
- formErrorMesage (CTkLabel): Label that indicates various errors that happened while submitting the form
- formFieldsSection (CTkFrame): Section that contains labels and their corresponding entry widgets
- formFields (Array): Array of objects that's used to create the label and entry widgets
- formEntryList (Array): List of entry widgets for the registration form
- formBtnsSection (CTkFrame): Container for the buttons of the form
- clearFormBtn (CTkButton): Clear the form of any pre-existing input
- confirmLoginBtn (CTkButton): Button that attempts to log the user in
- openRegisterAccountBtn (CTkButton): Redirects the user to the userRegisterPage

Methods: 
- loginUser(self): Attempts to log the user in. If their credentials are valid, the user is directed to 
	the userAccountPage. Else, the form will pop up with a message telling the user that their input is incorrect.
'''
class userLoginPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="#EBEBEB")
		self.master = master
		# Create login form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Login", text_color="#0F3325", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)
		formFields = [
			{
				"text": "Username"
			},
			{
				"text": "Password",
				"toggleHidden": True,
			}
		]
		# Iteratively create the labels, entry widgets, and checboxes.
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x].get("text"), text_color="#0F3325")
			entry = ctk.CTkEntry(formFieldsSection)
			label.grid(row=x, column=0, pady=10, ipadx=10)
			entry.grid(row=x, column=1, pady=10, ipadx=10)
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", text_color="#0F3325", onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)
			self.formEntryList.append(entry)

		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", fg_color="#0E4732", hover_color="#3A6152", command=lambda: clearEntryWidgets(self.formEntryList))
		confirmLoginBtn = ctk.CTkButton(formBtnsSection, text="Confirm Login", fg_color="#0E4732", hover_color="#3A6152", command=self.loginUser)
		openRegisterAccountBtn = ctk.CTkButton(formBtnsSection, text="Register New Account", fg_color="#0E4732", hover_color="#3A6152", command=lambda: self.master.openPage("userRegisterPage")) #type: ignore
		
		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		openRegisterAccountBtn.grid(row=0, column=1, padx=10, pady=10)
		confirmLoginBtn.grid(row=0, column=2, padx=10, pady=10)
		
	
	def loginUser(self):
		'''
		- Attempts to log in a user
		1. username (string): Inputted username
		2. password (string): Inputted password
		3. passwordHash (string): Password hash created from the user's inputted password
		4. retrievedUser (User): If retrievedUser exists, then there is a User with the same username and 
			password hash that was entered in onto the form. That means the inputted credentials were correct, so 
			that's a successful login. Else, the username or the password was incorrect. 
		'''
		# Check if input fields are empty
		if (isEmptyEntryWidgets(self.formEntryList)):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get input values from the form
		username = self.formEntryList[0].get()
		password = self.formEntryList[1].get()
		passwordHash = hashlib.md5(password.encode("utf-8")).hexdigest()

		# Now check if the inputted username and password hash matches a record from the User table 
		retrievedUser = self.master.session.query(User).filter_by(username=username, passwordHash=passwordHash).first() #type: ignore
		if not retrievedUser:
			self.formErrorMessage.configure(text="Username or password is incorrect!")
			return
		
		# Assign the new logged in user
		self.master.loggedInUser = retrievedUser #type: ignore

		# Update the nav buttons now that the user is logged in
		# so that they actually work and aren't disabled
		self.master.header.updateNavButtons() #type: ignore

		# Redirect the user to the 'My Account' or the 'user account page'
		self.master.openPage("userAccountPage") #type: ignore