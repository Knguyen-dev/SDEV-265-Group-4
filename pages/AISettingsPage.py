import customtkinter as ctk
import tkinter as tk

'''
+ AISettingsPage: Page where hte user can configure the settings of the AI

Attributes/Variables:
- master (App): App class from 'Main.py'
- form (CTkFrame): Frame that contains all widgets for the form/page
- formHeader (CTkFrame): Header of the form
- formHeading (CTkLabel): Heading label of the form
- formFieldsSection (CTkFrame): Frame that contains all of the labels and entry widgets for the form
- formSlidersList (Array): List of CTkSlider objects, which are later used to obtain the values of the form.
- formFields (Array): Array of objects that help create the labels and sliders on the form
- sliderVar (tk.IntVar): Variable that stores the numerical value of the slider.
- sliderLabel(CTkLabel): Label corresponding to 'slider'.
- slider (CTkSlider): A tkinter slider object that is displayed on screen.
- formBtnsSection (CTkFrame): Frame that contains all of the buttons on the form.
- restoreSettingsBtn (CTkButton): Button that restores the settings sliders on the form to reflect the AI's current settings.
- changeSettingsBtn (CTkButton): Applies changes to the AI's settings configurations.

Methods:
- restoreAISettings(self): Restores sliders for the AI settings page to the values that are 
	currently set on the AI.

- changeAISettings(self): Applies changes to the AI class instance in the 'App' class
'''
# Ai settings page frame
class AISettingsPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		form = ctk.CTkFrame(self)

		# Form header
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Configure AI Settings!", font=("Helvetica", 32))
		
		# Section for form sliders 
		formFieldsSection = ctk.CTkFrame(form)
		self.formSlidersList = [] #list of sliders
		'''
		NOTE: The "value" attribute in the formFields objects/maps should be obtained from the 
			ai chat bot that we instantiate.
		''' 
		formFields = [ # array of objects for the creation of the form sliders
			{
				"text": 'Temperature',
				"lower": 0,
				"upper": 2,
				"value": 0,
			},
			{
				"text": 'Top P',
				"lower": 0,
				"upper": 1,
				"value": 0,
			},
			{
				"text": 'Presence Penalty',
				"lower": -2,
				"upper": 2,
				"value": 0,
			},
			{
				"text": 'Frequency Penalty',
				"lower": -2,
				"upper": 2,
				"value": 0,
			},
		]

		# Create form sliders and labels iteratively
		for x in range(len(formFields)):
			sliderLabel = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"]) # label defining what a slider is for
			slider = tk.Scale(formFieldsSection, from_=formFields[x]["lower"], to=formFields[x]["upper"], resolution=0.01, orient="horizontal", bg="#D3D3D3", length=200)
			sliderLabel.grid(row=x, column=0, padx=10, pady=10)
			slider.grid(row=x, column=1, padx=10, pady=10)
			self.formSlidersList.append(slider)

		isStream = False
		checkVar = ctk.BooleanVar()
		checkVar.set(isStream)
		streamLabel = ctk.CTkLabel(formFieldsSection, text="Stream")
		self.streamCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, onvalue=True, offvalue=False, text="")
		streamLabel.grid(row=len(formFields), column=0)
		self.streamCheckBox.grid(row=len(formFields), column=1)

		# Create the form buttons
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		restoreSettingsBtn = ctk.CTkButton(formBtnsSection, text="Restore Settings")
		changeSettingsBtn = ctk.CTkButton(formBtnsSection, text="Confirm Changes", command=self.changeAISettings)

		# Structure the widgets on the page
		form.pack(expand=True)		
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, padx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		restoreSettingsBtn.grid(row=0, column=0, padx=10)
		changeSettingsBtn.grid(row=0, column=1, padx=10)
	

	# Restores the value of the sliders to represent what the AI chat bot 
	# is currently using.
	def restoreAISettings(self):
		pass


	# Changes the settings of the AI chat bot
	def changeAISettings(self):
		temperature = self.formSlidersList[0].get()
		top_p = self.formSlidersList[1].get()
		presence_penalty = self.formSlidersList[2].get()
		frequency_penalty = self.formSlidersList[3].get()
		is_stream = self.streamCheckBox.get()

		# Then call the completion function on the ai chat bot

		