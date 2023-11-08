import customtkinter as ctk
import hashlib
import sys
sys.path.append("..")
from classes.utilities import clearEntryWidgets, isEmptyEntryWidgets, isValidPassword, toggleHidden

'''
+ changePasswordPage: Page where the user can change the password of their account

Attributes/Variables:
- master (App): 'App' class instance from 'Main.py'  
- form (CTkFrame): Frame that contains all form widgets
- formHeader (CTkFrame): Header of the form
- formHeading (CTkLabel): Heading label of the form
- formErrorMessage (CTkLabel): Label that shows any errors that occurred with form submission
- formFieldsSection (CTkFrame): Section that contains all form labels, entry widgets, etc.
- formFields (Array): Array that helps create the labels, entry widgets, and check boxes in the form
- formEntryList (Array): List of entry widgets that'll be used to obtain information from the form
- label (CTkLabel): Label for the entry widget
- entry (CTkEntry): Entry widget where user enters infomration
- checkVar (StringVar): Variable that keeps track of the check box's state
- visibilityCheckBox (CTkCheckBox): Check box that toggles the visibility of the entry widget
- formBtnsSection (CTkFrame): Frame that contains all buttons for the form
- clearFormBtn (CTkButton): Button that clears all input from the form
- changePasswordBtn (CTkButton): Button that attempts to change the password of the user's account.
	On success, it logs out the user.

Methods

'''

##### Page for changing passwords #####
class changePasswordPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		# Create edit form frame
		form = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Change Password", font=("Helvetica", 32), text_color=self.master.theme["label_clr"])
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="", text_color=self.master.theme["label_clr"])
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form, fg_color="transparent")
		formFields = [
			"Old Password",
			"New Password",
			"Retype New Password",
		]
		
		# Then create and position label and entry widgets for form
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x], text_color=self.master.theme["label_clr"])
			entry = ctk.CTkEntry(formFieldsSection, fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"])
			checkVar = ctk.StringVar(value="off")
			visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", text_color=self.master.theme["label_clr"], onvalue="on", offvalue="off")
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, pady=10, padx=10)
			entry.grid(row=x, column=1, pady=10, padx=10)
			visibilityCheckBox.grid(row=x, column=2, pady=10, padx=4)

		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: clearEntryWidgets(self.formEntryList))		
		changePasswordBtn = ctk.CTkButton(formBtnsSection, text="Confirm Change", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.changePassword)

		# Structure the remaining elements of the page
		# padx=90; adds enough gray padding so that form looks uniform
		formHeader.grid(row=0, column=0, pady=10, padx=90)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		changePasswordBtn.grid(row=0, column=1, padx=10, pady=10)


	
	def changePassword(self):
		'''
		- Changes the currently logged in user's password on their account. On success, it logs them out and redirects 
			them to the userLoginPage to login again, now with their new password.
		1. oldPassword (string): Form input representing the user's current password
		2. oldPasswordHash (string): Password hash based on oldPassword
		3. newPassword (string): Form input representing the user's new password, or the password they 
			want to change to.
		4. confirmNewPassword (string): Form input that should be the same as newPassword, as this is 
			here to tell the user to retype newPassword to confirm that it is the password they want to change to.
		5. retrievedUser (User): If this exists, there exists an account in the database where 
			the username of the currently logged in user and the password that they entered match.
		'''
		# Check if fields are empty
		if (isEmptyEntryWidgets(self.formEntryList)):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return

		oldPassword = self.formEntryList[0].get()
		oldPasswordHash = hashlib.md5(oldPassword.encode("utf-8")).hexdigest()
		newPassword = self.formEntryList[1].get()
		confirmNewPassword = self.formEntryList[2].get()

		# Check if the new password is valid
		if not isValidPassword(newPassword):
			self.formErrorMessage.configure(text="Password can only be 6-20 characters with only numbers, letters, and symbols: !@#$%^&*(){}[]<>,+~-._")
			return
		
		# Check if passwords match
		if newPassword != confirmNewPassword:
			self.formErrorMessage.configure(text="Passwords must match!")
			return
		
		# User can only change the password of the account that they're currently logged into.
		# So query in the user's table for a matching username, and a matching password hash
		retrievedUser = self.master.session.query(User).filter_by(username=self.master.loggedInUser.username, passwordHash=oldPasswordHash).first() #type: ignore
		
		# If we didn't find a user with the current usernmae and password hash to current password, then they had to have gotten the password input wrong
		if not retrievedUser:
			self.formErrorMessage.configure(text="Old password entered is incorrect!")
			return
		
		# Save new password to user and commit it to the database
		retrievedUser.passwordHash = hashlib.md5(newPassword.encode("utf-8")).hexdigest()
		self.master.session.commit() #type: ignore
		self.master.session.close() #type: ignore

		# After a password is changed we log out our user
		self.master.logoutUser() #type: ignore
