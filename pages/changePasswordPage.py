import customtkinter as ctk
import hashlib
import sys
sys.path.append("..")
from classes.utilities import clearEntryWidgets, isEmptyEntryWidgets, isValidPassword, toggleHidden


##### Page for changing passwords #####
class changePasswordPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# Create edit form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Change Password", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)

		formFields = [
			"Old Password",
			"New Password",
			"Retype New Password",
		]
		# Create list of form entries to get input later
		# Then create and position label and entry widgets for form
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x])
			entry = ctk.CTkEntry(formFieldsSection)
			checkVar = ctk.StringVar(value="off")
			visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", onvalue="on", offvalue="off")
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, pady=10, padx=10)
			entry.grid(row=x, column=1, pady=10, padx=10)
			visibilityCheckBox.grid(row=x, column=2, pady=10, padx=4)

		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))		
		changePasswordBtn = ctk.CTkButton(formBtnsSection, text="Confirm Change", command=self.changePassword)

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
		
		# User can only delete the account they're currently signed in to.
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
