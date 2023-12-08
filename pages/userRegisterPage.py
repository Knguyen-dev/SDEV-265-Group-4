import customtkinter as ctk
import hashlib
import sys
sys.path.append("..")
from classes.utilities import *
from classes.models import User


'''
+ userRegisterPage: Frame that represents the registration page that the user is directed to in order to create a new 
	account.

Constructor:
- master: 'App' class instance from 'Main.py'

Attributes/Variables:
- master (App): App class from 'Main.py'
- form (CTkFrame): Tkinter frame that contains all of the widgets for the form
- formHeader (CTkFrame): Header of the form 
- formHeading (CTkLabel): Heading message for the form
- formErrorMesage (CTkLabel): Label that indicates various errors that happened while submitting the form
- formFieldsSection (CTkFrame): Section that contains labels and their corresponding entry widgets
- formFields (Array): Array of objects that's used to create the label and entry widgets
- formEntryList (Array): List of entry widgets for the registration form
- formBtnsSection (CTkFrame): Container for the buttons of the form
- openLoginBtn (CTkButton): Button that redirects the user to the login apge
- confirmRegisterBtn (CTkButton): Button that submits the form and attempts to register the user.
- clearFormBtn (CTkButton): Clears the entry widgets on the form

Methods: 
- registerUser(self): Registers a new user into the database if the form is valid. Then after a successful 
	submission, the user is redirected to the login page
'''
class userRegisterPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		# Create registration form frame
		form = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		form.pack(expand=True)

		# Create form header and text elements for header
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Register", text_color=self.master.theme["label_clr"], font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text_color=self.master.theme["label_clr"], text="")

		# Create input section with form fields
		formFieldsSection = ctk.CTkFrame(form, fg_color="transparent")
		formFields = [
			{
				"text": "Email",
			},
			{
				"text": "Username",
			},
			{
				"text": "First Name",
			},
			{
				"text": "Last Name",
			},
			{
				"text": "Password",
				"toggleHidden": True	
			},
			{
				"text": "Confirm Password",
				"toggleHidden": True
			},
		]		
		self.formEntryList = []

		# Iterate through object to create fields
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"], text_color=self.master.theme["label_clr"])
			entry = ctk.CTkEntry(formFieldsSection, fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"])
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, padx=10, pady=10)
			entry.grid(row=x, column=1, padx=10, pady=10)
			# If there's a 'toggleHidden' attribute, add a checkbox
			# so that we can toggle visibility on the field
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", text_color=self.master.theme["label_clr"], onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)
			
		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		openLoginBtn = ctk.CTkButton(formBtnsSection, text_color=self.master.theme["btn_text_clr"],  text="Log into an existing account", fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("userLoginPage")) #type: ignore
		confirmRegisterBtn = ctk.CTkButton(formBtnsSection, text_color=self.master.theme["btn_text_clr"],  text="Confirm Registration", fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.registerUser)
		clearFormBtn = ctk.CTkButton(formBtnsSection, text_color=self.master.theme["btn_text_clr"],  text="Clear", fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: clearEntryWidgets(self.formEntryList))

		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		openLoginBtn.grid(row=0, column=1, padx=10, pady=10)
		confirmRegisterBtn.grid(row=0, column=2, padx=10, pady=10)

	
	def registerUser(self):
		'''
		- Registers a user in the database. If the form is valid, the user is added and redirected to the login page. Else 
			the form will show an error message telling the user which part of their form is wrong.
		1. email (string): Value representing the email that the user entered.
		2. username (string): The value the user representing the username field.
		3. firstName (string): The value the user representing the first mame field.
		4. lastName (string): The value the user representing the last name field.
		5. password (string): The value the user representing the password field.
		6. confirmPassword (string): The value the user entered for the confirm password field.
		7. retrievedUser (User): If retrievedUser exists, the username that was entered into the form is already owned
			by a user in the database. 
		8. newUser (User): User object with attribute values from the form that is going to be added into the database
		'''
		# Check if any fields are empty before moving on
		if isEmptyEntryWidgets(self.formEntryList):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return

		# Get input field values
		email = self.formEntryList[0].get()
		username = self.formEntryList[1].get()
		firstName = self.formEntryList[2].get()
		lastName = self.formEntryList[3].get()
		password = self.formEntryList[4].get()
		confirmPassword = self.formEntryList[5].get()

		# Check if it's a valid email form
		if not isValidEmail(email):
			self.formErrorMessage.configure(text="Email isn't in valid form!")
			return
		
		# Check if username is valid
		if not isValidUsername(username):
			self.formErrorMessage.configure(text="Username length is 6-20 characters, and can only have numbers, letters, and underscores!")
			return
		
		# Check if password is valid
		if not isValidPassword(password):
			self.formErrorMessage.configure(text="Password can only be 6-20 characters with only numbers, letters, and symbols: !@#$%^&*(){}[]<>,+~-._")
			return
		
		# Check if password and the retryped password match
		if password != confirmPassword:
			self.formErrorMessage.configure(text="Passwords must match!")
			return
		
		# Check if there are any users with the inputted username
		retrievedUser = self.master.session.query(User).filter_by(username=username).first() #type: ignore
		if retrievedUser:
			self.formErrorMessage.configure(text="Usename already taken!")
			return
		
		# Create a new user based on the form information
		newUser = User(
			email=email,
			username=username,
			firstName=firstName,
			lastName=lastName,
			passwordHash=hashlib.md5(password.encode("utf-8")).hexdigest(),
			avatar="default_user.jpg"
		)

		# Add new user to the database
		self.master.session.add(newUser) #type: ignore
		self.master.session.commit() #type: ignore
		self.master.session.close() #type: ignore

		# Redirect user to login screen after they've successfully registered
		self.master.openPage("userLoginPage") #type: ignore