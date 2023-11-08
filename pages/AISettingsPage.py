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
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		form = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])

		# Form header
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Configure AI Settings!", font=("Helvetica", 32), text_color=self.master.theme["label_clr"])
		
		# Section for form sliders 
		formFieldsSection = ctk.CTkFrame(form, fg_color="transparent")
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
		]

		# Create form sliders and labels iteratively
		for x in range(len(formFields)):
			sliderVar = ctk.DoubleVar(value=formFields[x]["value"])
			sliderLabel = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"], text_color=self.master.theme["label_clr"]) # label defining what a slider is for
			valueLabel = ctk.CTkLabel(formFieldsSection, text_color=self.master.theme["label_clr"], textvariable=sliderVar)

			# Multiplied by 100 so each step is changes value by 0.01
			numberSteps = (formFields[x]["upper"] - formFields[x]["lower"]) * 100 

			# Slider object itself
			slider = ctk.CTkSlider(formFieldsSection, from_=formFields[x]["lower"], to=formFields[x]["upper"], number_of_steps=numberSteps, orientation="horizontal", variable=sliderVar)
			
			sliderLabel.grid(row=x, column=0, padx=10, pady=10)
			valueLabel.grid(row=x, column=1, padx=10, pady=10)
			slider.grid(row=x, column=2, padx=10, pady=10)
			self.sliderVarList.append(sliderVar)

		# Response style entry and label
		responseStyleLabel = ctk.CTkLabel(formFieldsSection, text="Response Style", text_color=self.master.theme["label_clr"])
		self.responseStyleBox = ctk.CTkTextbox(formFieldsSection, height=50, fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"])
		responseStyleLabel.grid(row=len(formFields), column=0)
		self.responseStyleBox.grid(row=len(formFields), column=1)

		# Insert/render the AI's current response/writing style 
		self.responseStyleBox.insert("1.0", self.master.storyGPT.response_style)	

		# Create the form buttons
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		restoreSettingsBtn = ctk.CTkButton(formBtnsSection, text="Restore Settings", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.restoreSettingsWidgets)
		changeSettingsBtn = ctk.CTkButton(formBtnsSection, text="Confirm Changes", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.changeAISettings)

		# Structure the widgets on the page
		form.pack(expand=True)		
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, padx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		restoreSettingsBtn.grid(row=0, column=0, padx=10)
		changeSettingsBtn.grid(row=0, column=1, padx=10)


	def formatSliderVars(self):
		'''Rounds all slider variable values to the hundredth's place'''
		for sliderVar in self.sliderVarList:
			roundedValue = round(sliderVar.get(), 2)
			sliderVar.set(roundedValue)


	
	def restoreSettingsWidgets(self):
		''' Restores the value of the sliders and checkboxes to represent what the AI chat bot is currently using.'''
		# Set the variables of the sliders to the ai's current parameter values
		self.sliderVarList[0].set(self.master.storyGPT.temperature) #type: ignore
		self.sliderVarList[1].set(self.master.storyGPT.top_p) #type: ignore
		self.sliderVarList[2].set(self.master.storyGPT.presence_penalty) #type: ignore
		self.sliderVarList[3].set(self.master.storyGPT.frequency_penalty) #type: ignore
		# First clear the responseStyleBox, and then insert in the ai's current response style
		self.responseStyleBox.delete("1.0", "end-1c")		
		self.responseStyleBox.insert("1.0", self.master.storyGPT.response_style) #type: ignore


	
	def changeAISettings(self):
		'''Changes the settings of the Story Writer AI'''
		# Round all slider values to the hundredth's place to ensure no values that are smaller than that.
		self.formatSliderVars()

		# Change attributes of storyGPT using corresponding tkinter-related variables
		self.master.storyGPT.temperature = self.sliderVarList[0].get() #type: ignore
		self.master.storyGPT.top_p = self.sliderVarList[1].get() #type: ignore
		self.master.storyGPT.presence_penalty = self.sliderVarList[2].get() #type: ignore
		self.master.storyGPT.frequency_penalty = self.sliderVarList[3].get() #type: ignore
		self.master.storyGPT.response_style = self.responseStyleBox.get("1.0", "end-1c") #type: ignore

		print(self.master.storyGPT.temperature)
		print(self.master.storyGPT.top_p)
		print(self.master.storyGPT.presence_penalty)
		print(self.master.storyGPT.frequency_penalty)
		print(self.master.storyGPT.response_style)




		