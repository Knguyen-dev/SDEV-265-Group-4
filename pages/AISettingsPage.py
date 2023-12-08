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
        
        self.currentMode = ''
        self.aiSettings = ''
        super().__init__(self.master,fg_color=self.master.theme["main_clr"], corner_radius=0)
        form = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
        # Form header
        formHeader = ctk.CTkFrame(form, fg_color="transparent")
        formHeading = ctk.CTkLabel(formHeader, text="Set AI Settings", font=(
            "Helvetica", 32), text_color=self.master.theme["label_clr"])
        
        # Structure the widgets on the page
        form.pack(expand=True)
        formHeader.grid(row=0, column=0, pady=10)
        formHeading.grid(row=0, column=0)

        innerAISettingsFrame = ctk.CTkFrame(form, fg_color="transparent")
        innerAISettingsFrame.grid(row=1, column=0)
        innerAISettingsFrame.grid_rowconfigure(4, weight=1)

        self.aiModeSliderLabel = ctk.CTkLabel(innerAISettingsFrame, text=f'Conversation Style: ', text_color=self.master.theme["label_clr"], font=("Helvetica", 16))
        self.aiModeSliderLabel.grid(row=0, column=0, padx=(10, 10), pady=(10, 10))
        aiModeSlider = ctk.CTkSlider(innerAISettingsFrame, from_=0, to=2, number_of_steps=2)
        aiModeSlider.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))
        aiModeSlider.configure(command=self.sliderCallback)

        # Response style entry and label
        responseStyleLabel = ctk.CTkLabel(innerAISettingsFrame, text="Response Style", text_color=self.master.theme["label_clr"])
        self.responseStyleBox = ctk.CTkTextbox(
            innerAISettingsFrame, height=25, fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"])
        responseStyleLabel.grid(row=3, column=0)
        self.responseStyleBox.grid(row=4, column=0)

        # Insert/render the AI's current response/writing style
        self.responseStyleBox.insert("1.0", self.master.storyGPT.response_style)

        # Create the form buttons
        formBtnsSection = ctk.CTkFrame(innerAISettingsFrame, fg_color="transparent")
        resetSettingsBtn = ctk.CTkButton(formBtnsSection, text="Restore Settings",  text_color=self.master.theme[
                                           "btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.resetMode)
        changeSettingsBtn = ctk.CTkButton(formBtnsSection, text="Confirm Changes",  text_color=self.master.theme[
                                          "btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.applyAISettings(self.aiSettings))

        formBtnsSection.grid(row=5, column=0, pady=10)
        resetSettingsBtn.grid(row=0, column=1, padx=10)
        changeSettingsBtn.grid(row=0, column=2, padx=10)

        self.aiModeMap = {
        0: "Creative",
        1: "Balanced",
        2: "Focused"}

        self.aiSettingsMap = {
            "Creative": {
                "temp": (1),
                "top_p": (1),
                "presence_penalty": (0),
                "frequency_penalty": (0),
            },
            "Balanced": {
                "temp": (0.8),
                "top_p": (1),
                "presence_penalty": (0),
                "frequency_penalty": (0),
            },
            "Focused": {
                "temp": (0.5),
                "top_p": (1),
                "presence_penalty": (0),
                "frequency_penalty": (0),
            },
        }

    def sliderCallback(self, value):
        key = int(value)
        print('key=', key)
        self.currentMode = self.aiModeMap[key]
        print('current mode=', self.currentMode)
        self.aiSettings = self.aiSettingsMap[self.currentMode]
        print('settings=', self.aiSettings)
        self.aiModeSliderLabel.configure(text=f'Conversation Style: \n {self.currentMode}')

    def applyAISettings(self, settingsObj):
    # Access the settings object's values and set them to the AI's attributes
        self.master.storyGPT.temperature = settingsObj["temp"]
        self.master.storyGPT.top_p = settingsObj["top_p"]
        self.master.storyGPT.presence_penalty = settingsObj["presence_penalty"]
        self.master.storyGPT.frequency_penalty = settingsObj["frequency_penalty"]
        self.master.storyGPT.response_style = self.responseStyleBox.get(
            "1.0", "end-1c")  # type: ignore

    def resetMode(self):
        self.currentMode = self.currentMode
        
