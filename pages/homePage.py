import customtkinter as ctk
from PIL import Image # Import python image library for the button images
import os
'''
+ homePage: Frame that represents the home page of the application. Here the user can choose to start a new story/chat, 
	or continue the story that they were most recently on.

Attributes/Variables:
- master (App): 'App' class instance from 'Main.py'
- innerPageFrame (CTkFrame): Frame that centers page and contains all of its widgets 
- pageHeader (CTkFrame): Header of the page
- pageHeading (CTkLabel): Heading label that displays message of the page
- pageBtnsSection (CTkFrame): Container that contains all of the home page's buttons 
- newStoryBtn (CTkButton): Button that starts a new story and redirects the user to the AIChatPage
- continuePrevStoryBtn (CTkButton): Button that continues the story that the user was most recently on
	and redirects them to the AIChatPage

Methods: 
- startNewStory: Redirects user to the AIChatPage, wipes out previous story information such as unsaved messages,
	and as a result let's them start a new story.
'''
class homePage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		
		innerPageFrame = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])

		pageHeader = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		pageHeading = ctk.CTkLabel(pageHeader, text="Home", text_color=self.master.theme["label_clr"], font=("Helvetica", 32))

		pageBtnsSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		newStoryBtn_img = ctk.CTkImage(Image.open(os.path.join(self.master.image_path, "glass_addStoryBtn.png")),size=(150, 150))
		newStoryBtn = ctk.CTkButton(pageBtnsSection, image=newStoryBtn_img, text=" ", height=40, width=40, fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.startNewStory)
		newStoryBtn_lbl = ctk.CTkLabel(pageBtnsSection, font=("Helvetica", 24), text="New Story", text_color=self.master.theme["btn_text_clr"])
		continuePrevStoryBtn_img = ctk.CTkImage(Image.open(os.path.join(self.master.image_path, "glass_prevStoryBtn.png")),size=(150, 150))
		continuePrevStoryBtn = ctk.CTkButton(pageBtnsSection, image=continuePrevStoryBtn_img, text=" ", height=40, width=40, fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("AIChatPage")) #type: ignore
		continuePrevStoryBtn_lbl = ctk.CTkLabel(pageBtnsSection, font=("Helvetica", 24), text="Continue Story", text_color=self.master.theme["btn_text_clr"])
		innerPageFrame.pack(expand=True)
		pageHeader.grid(row=0, column=0, pady=10)
		pageHeading.grid(row=0, column=0)

		pageBtnsSection.grid(row=1, column=0)
		newStoryBtn.grid(row=1, column=0, padx=10, pady=10)
		newStoryBtn_lbl.grid(row=2, column=0, padx=20, pady=20)
		continuePrevStoryBtn.grid(row=1, column=1, padx=10, pady=10)
		continuePrevStoryBtn_lbl.grid(row=2, column=1, padx=20, pady=20)


	# Starts a new chat, so that user can write a new story
	def startNewStory(self):
		# Clear previous chat messages and wipe story data since the user is starting a brand new slate
		self.master.unsavedStoryMessages = [] #type: ignore
		self.master.currentStory = None #type: ignore
		self.master.isSavedStory = False #type: ignore
		self.master.isRemixedStory = False #type: ignore
		self.master.storyGenObj = None #type: ignore

		# Wipe the AI's knowledge of any previous story messages and stories.
		self.master.storyGPT.clear() #type: ignore

		# Redirect the user to the ai chat page
		self.master.openPage("AIChatPage") #type: ignore