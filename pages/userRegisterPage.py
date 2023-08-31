import customtkinter as ctk # Custom tkinter
import hashlib # Hashing passwords
import sys # Makes it easier to access appropriate files and modules
sys.path.append("..")
from classes.utilities import * # Input validation functions and form clearing
from classes.models import User



class userRegisterPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		
		# Create registration form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create form header and text elements for header
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Register", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")

		# Create input section with form fields
		formFieldsSection = ctk.CTkFrame(form)
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
		# Create list of form entries to get input later
		self.formEntryList = []

		# Iterate through object to create fields
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"])
			entry = ctk.CTkEntry(formFieldsSection)
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, padx=10, pady=10)
			entry.grid(row=x, column=1, padx=10, pady=10)
			# If there's a 'toggleHidden' attribute, add a checkbox
			# so that we can toggle visibility on the field
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)
			
		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		openLoginBtn = ctk.CTkButton(formBtnsSection, text="Log into an existing account", command=lambda: self.master.openPage("userLoginPage")) #type: ignore
		confirmRegisterBtn = ctk.CTkButton(formBtnsSection, text="Confirm Registration", command=self.registerUser)
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))

		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)

		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)

		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		openLoginBtn.grid(row=0, column=1, padx=10, pady=10)
		confirmRegisterBtn.grid(row=0, column=2, padx=10, pady=10)


	def isExistingUser(self, username):
		retrievedUser = self.master.session.query(User).filter_by(username=username).first() #type: ignore
		return retrievedUser is not None


	# Registers a user in the database
	def registerUser(self):
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
		
		# Create a session that we can use
		session = self.master.Session() #type: ignore

		# Check if there are any users with the inputted username
		retrievedUser = session.query(User).filter_by(username=username).first()
		if retrievedUser:
			self.formErrorMessage.configure(text="Usename already taken!")
			return
		
		# Create a new user based on the form information
		newUser = User(
			email=email,
			username=username,
			firstName=firstName,
			lastName=lastName,
			# For right now do a simple md5 hash, but later
			# we should use that api idea
			passwordHash=hashlib.md5(password.encode("utf-8")).hexdigest(),
			avatar="default_user.jpg"
		)

		# Add new user to the database
		session.add(newUser)
		session.commit()
		session.close()