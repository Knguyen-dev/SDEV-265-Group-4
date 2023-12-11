import customtkinter as ctk
import sys
sys.path.append("..")
from classes.utilities import *
from classes.models import User


###### The page for editting accounts #####
class editAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		# Create edit form frame
		form = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Edit Account", font=("Helvetica", 32), text_color=self.master.theme["label_clr"])
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="", text_color=self.master.theme["label_clr"])
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form, fg_color="transparent")
		formFields = [
			{
				"text": "Username",
				"value": self.master.loggedInUser.username,
			},
			{
				"text": "Email",
				"value": self.master.loggedInUser.email,
			},
			{
				"text": "First Name",
				"value": self.master.loggedInUser.firstName,
			},
			{
				"text": "Last Name",
				"value": self.master.loggedInUser.lastName,
			},
		]

		# Create list of form entries to get input later
		# Then create and position label and entry widgets for form
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"], text_color=self.master.theme["label_clr"])
			entry = ctk.CTkEntry(formFieldsSection, fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"])
			
			# Insert the current value of a user's attribute into the entry widget to show the user 
			# their current account information
			entry.insert(0, formFields[x]["value"]) 

			# Structure the label and entry widget
			label.grid(row=x, column=0, pady=10, ipadx=10)
			entry.grid(row=x, column=1, pady=10, ipadx=10)
			self.formEntryList.append(entry)

		# Clear form button and then a confirm changes button
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection,  text="Clear", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: clearEntryWidgets(self.formEntryList))
		confirmEditsBtn = ctk.CTkButton(formBtnsSection,  text="Confirm Edits", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.editAccount)
		openChangePasswordBtn = ctk.CTkButton(formBtnsSection,  text="Change Password", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("changePasswordPage")) 
		openDeleteAccountBtn = ctk.CTkButton(formBtnsSection,  text="Account Deletion", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("deleteAccountPage")) 

		# Structure the remaining page elements accordingly
		formHeader.grid(row=0, column=0, padx=70, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		confirmEditsBtn.grid(row=0, column=0, padx=10, pady=10)
		clearFormBtn.grid(row=1, column=0, padx=10, pady=10)
		openChangePasswordBtn.grid(row=2, column=0, padx=10, pady=10)
		openDeleteAccountBtn.grid(row=3, column=0, padx=10, pady=10)

	# Validates and edits the attributes (username, email, first name, and last name) of the currently logged in user
	def editAccount(self):
		# Check if fields are empty
		if (isEmptyEntryWidgets(self.formEntryList)):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get inputted values of the form
		username = self.formEntryList[0].get()
		email = self.formEntryList[1].get()
		firstName = self.formEntryList[2].get()
		lastName = self.formEntryList[3].get()

		# Validate the username
		if not isValidUsername(username):
			self.formErrorMessage.configure(text="Username is invalid!")
			return

		# Validate the email
		if not isValidEmail(email):
			self.formErrorMessage.configure(text="Email is invalid!")
			return
		
		'''
		- Check if email is already taken: Query for a user with the inputted username 
		- If the user exists, a user in the database was found with the inputted username
			Case 1: This could mean, a different user from the logged in user has the username
			Case 2: The currently logged in user kept their current username in the username entry field.
			So the retrievedUser is just a record of the currently logged in user. In this case, we want 
			to let the form go through. By putting "and self.master.loggedInUser != retrievedUser", we're making 
			sure that a different user from the currently logged in user already has the username that they entered.
			As a result, the user is able to submit the form when they don't change their username, and the system
			correctly detects when a separate user has their inputted username
		'''
		retrievedUser = self.master.session.query(User).filter_by(username=username).first() 
		if retrievedUser and (self.master.loggedInUser != retrievedUser): 
			self.formErrorMessage.configure(text="Username is already taken!")
			return
		
		# All form checks passed, so apply changes
		self.master.loggedInUser.username = username 
		self.master.loggedInUser.email = email 
		self.master.loggedInUser.firstName = firstName 
		self.master.loggedInUser.lastName = lastName 
		self.master.session.commit() 

		# Then redirect user to the account page, so that they can see their changes
		self.master.openPage("userAccountPage") 