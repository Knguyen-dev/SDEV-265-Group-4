import customtkinter as ctk
import hashlib
import sys
sys.path.append("..")
from classes.utilities import clearEntryWidgets, isEmptyEntryWidgets, toggleHidden



# Page for user to delete their account
class deleteAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.mainFGCLR, corner_radius=0)
		
		# Create edit form frame
		form = ctk.CTkFrame(self, fg_color=self.master.subFGCLR)
		form.pack(expand=True)
		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Delete Account", font=("Helvetica", 32), text_color=self.master.textCLR)
		subHeading = ctk.CTkLabel(formHeader, text=f"Are you sure you want to delete '{self.master.loggedInUser.username}'?", text_color=self.master.textCLR)
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="", text_color=self.master.textCLR)
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form, fg_color=self.master.subFGCLR)
		formFields = [
			{
				"text": "Username"
			},
			{
				"text": "Password", 
				"toggleHidden": True
			}
		]
		# Create list of form entries to get input later
		# Then create and position label and entry widgets for form
		self.formEntryList = []

		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x].get("text"), text_color=self.master.textCLR)
			entry = ctk.CTkEntry(formFieldsSection, fg_color=self.master.entryFGCLR, text_color=self.master.entryTextCLR)
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, padx=10, pady=10)
			entry.grid(row=x, column=1, padx=10, pady=10)
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", text_color=self.master.textCLR, onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)

		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", text_color=self.master.textCLR, fg_color=self.master.btnFGCLR, hover_color=self.master.btnHoverCLR, command=lambda: clearEntryWidgets(self.formEntryList))
		deleteAccountBtn = ctk.CTkButton(formBtnsSection, text="Delete Account", text_color=self.master.textCLR, fg_color=self.master.btnFGCLR, hover_color=self.master.btnHoverCLR, command=self.deleteAccount)
		
		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, padx=40, pady=10)
		formHeading.grid(row=0, column=0)
		subHeading.grid(row=1, column=0)
		self.formErrorMessage.grid(row=2, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0,column=0, padx=10, pady=10)
		deleteAccountBtn.grid(row=0,column=1, padx=10, pady=10)


	# Deletes the account/record of the currently logged in user from the database
	def deleteAccount(self):
		# Check if fields are empty
		if isEmptyEntryWidgets(self.formEntryList):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get input fields from forms
		username = self.formEntryList[0].get()
		password = self.formEntryList[1].get()
		passwordHash = hashlib.md5(password.encode("utf-8")).hexdigest()

		'''
		- Since user is deleting their own account, the username they enter should be the username of the currently logged in user.
		- As a result, for the form to be valid, the username and password must belong to the currently logged in user.		
		'''
		if self.master.loggedInUser.username == username and self.master.loggedInUser.passwordHash == passwordHash: #type: ignore
			# Delete the logged in user from the database and save those changes
			self.master.session.delete(self.master.loggedInUser) #type: ignore
			self.master.session.commit() #type: ignore
			# We can safely do the logout process on the user now, since their account does not exist anymore
			self.master.logoutUser() #type: ignore
		else:
			# Else, their username or password is wrong
			self.formErrorMessage.configure(text="Username or password is incorrect!")
