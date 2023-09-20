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
- sliderVarList (Array): List of tk.DoubleVar objects, which are later used to obtain the values of the form.
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
		self.sliderVarList = []
		formFields = [ 
			{
				"text": 'Temperature',
				"lower": 0,
				"upper": 2,
				"value": self.master.storyGPT.temperature,
			},
			{
				"text": 'Top P',
				"lower": 0,
				"upper": 1,
				"value": self.master.storyGPT.top_p,
			},
			{
				"text": 'Presence Penalty',
				"lower": -2,
				"upper": 2,
				"value": self.master.storyGPT.presence_penalty,
			},
			{
				"text": 'Frequency Penalty',
				"lower": -2,
				"upper": 2,
				"value": self.master.storyGPT.frequency_penalty,
			},
			{
				"text": 'Response Length (in words)',
				"lower": 25,
				"upper": 150,
				"value": self.master.storyGPT.response_length,
				"step": 1,
			},
		]

		# Create form sliders and labels iteratively
		for x in range(len(formFields)):
			sliderVar = tk.DoubleVar(value=formFields[x]["value"])
			sliderLabel = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"]) # label defining what a slider is for
			
			# If the data type for the slider var is defined, then chnage it
			if formFields[x]['text'] == "Response Length":
				sliderVar = tk.IntVar(value=formFields[x]["value"])

			# Slider object itself
			slider = tk.Scale(formFieldsSection, from_=formFields[x]["lower"], to=formFields[x]["upper"], resolution=0.01, orient="horizontal", bg="#D3D3D3", length=200, variable=sliderVar)
			
			# If the 'step' key is defined, then change the resolution or step of the slider
			if "step" in formFields[x]:
				slider.configure(resolution=formFields[x]["step"])
			
			sliderLabel.grid(row=x, column=0, padx=10, pady=10)
			slider.grid(row=x, column=1, padx=10, pady=10)
			self.sliderVarList.append(sliderVar)

		# Response style entry and label
		responseStyleLabel = ctk.CTkLabel(formFieldsSection, text="Response Style")
		self.responseStyleBox = ctk.CTkTextbox(formFieldsSection, height=50)
		responseStyleLabel.grid(row=len(formFields), column=0)
		self.responseStyleBox.grid(row=len(formFields), column=1)

		# Insert/render the AI's current response/writing style 
		self.responseStyleBox.insert("1.0", self.master.storyGPT.response_style)	

		# Is stream checkbox
		self.streamCheckVar = ctk.BooleanVar()
		self.streamCheckVar.set(self.master.storyGPT.is_stream)
		streamLabel = ctk.CTkLabel(formFieldsSection, text="Stream")
		streamCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=self.streamCheckVar, onvalue=True, offvalue=False, text="")
		streamLabel.grid(row=len(formFields) + 1, column=0, pady=10)
		streamCheckBox.grid(row=len(formFields) + 1, column=1, pady=10)

		# Create the form buttons
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		restoreSettingsBtn = ctk.CTkButton(formBtnsSection, text="Restore Settings", command=self.restoreSettingsWidgets)
		changeSettingsBtn = ctk.CTkButton(formBtnsSection, text="Confirm Changes", command=self.changeAISettings)

		# Structure the widgets on the page
		form.pack(expand=True)		
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, padx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		restoreSettingsBtn.grid(row=0, column=0, padx=10)
		changeSettingsBtn.grid(row=0, column=1, padx=10)
	

	# Restores the value of the sliders and checkboxes to represent what the AI chat bot is currently using.
	def restoreSettingsWidgets(self):
		# Set the variables of the sliders to the ai's current parameter values
		self.sliderVarList[0].set(self.master.storyGPT.temperature)
		self.sliderVarList[1].set(self.master.storyGPT.top_p)
		self.sliderVarList[2].set(self.master.storyGPT.presence_penalty)
		self.sliderVarList[3].set(self.master.storyGPT.frequency_penalty)
		self.sliderVarList[4].set(self.master.storyGPT.response_length)
				
		# First clear the respnoseStyleBox, and then insert in the ai's current response style
		self.responseStyleBox.delete("1.0", "end-1c")		
		self.responseStyleBox.insert("1.0", self.master.storyGPT.response_style)	

		# Set the value of the stream check variable to the AI's stream value 
		self.streamCheckVar.set(self.master.storyGPT.is_stream)


	# Changes the settings of the AI chat bot
	def changeAISettings(self):
		# Change attributes of storyGPT using corresponding tkinter-related variables
		self.master.storyGPT.temperature = self.sliderVarList[0].get()
		self.master.storyGPT.top_p = self.sliderVarList[1].get()
		self.master.storyGPT.presence_penalty = self.sliderVarList[2].get()
		self.master.storyGPT.frequency_penalty = self.sliderVarList[3].get()
		self.master.storyGPT.response_length = self.sliderVarList[4].get()
		self.master.storyGPT.response_style = self.responseStyleBox.get("1.0", "end-1c")
		self.master.storyGPT.is_stream = self.streamCheckVar.get()

		