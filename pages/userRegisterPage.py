import tkinter as tk
import customtkinter as ctk

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
				"labelText": "Email",
			},
			{
				"labelText": "Username",
			},
			{
				"labelText": "First Name",
			},
			{
				"labelText": "Last Name",
			},
			{
				"labelText": "Password",
				"isHidden": True	
			},
			{
				"labelText": "Confirm Password",
				"isHidden": True
			},
		]		
		# Create list of form entries to get input later
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["labelText"])
			entry = ctk.CTkEntry(formFieldsSection)
			# If it's the password field, hide the input
			if (formFields[x].get("isHidden")):
				entry.configure(show="*")
			label.grid(row=x, column=0, pady=10, ipadx=10)
			entry.grid(row=x, column=1, pady=10, ipadx=10)
			self.formEntryList.append(entry)
			
		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		openLoginBtn = ctk.CTkButton(formBtnsSection, text="Log into an existing account", command=lambda: self.master.openPage("userLoginPage")) #type: ignore
		confirmRegisterBtn = ctk.CTkButton(formBtnsSection, text="Confirm Registration")

		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)

		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)

		formBtnsSection.grid(row=2, column=0, pady=10)
		openLoginBtn.grid(row=0, column=0, padx=10, pady=10)
		confirmRegisterBtn.grid(row=0, column=1, padx=10, pady=10)




		




