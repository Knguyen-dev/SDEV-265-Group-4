import customtkinter as ctk

class homePage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		innerPageFrame = ctk.CTkFrame(self, fg_color="transparent")

		pageHeader = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		pageHeading = ctk.CTkLabel(pageHeader, text="Home", font=("Helvetica", 32))

		pageBtnsSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		newStoryBtn = ctk.CTkButton(pageBtnsSection, text="Start A New Story!", command=self.startNewStory)		
		continuePrevStoryBtn = ctk.CTkButton(pageBtnsSection, text="Continue Previous Story!", command=lambda: self.master.openPage("AIChatPage")) #type: ignore

		innerPageFrame.pack(expand=True)
		pageHeader.grid(row=0, column=0, pady=10)
		pageHeading.grid(row=0, column=0)

		pageBtnsSection.grid(row=1, column=0)
		newStoryBtn.grid(row=0, column=0, pady=5)
		continuePrevStoryBtn.grid(row=1, column=0, pady=5)


	# Starts a new chat, so that user can write a new story
	def startNewStory(self):
		# Clear previous chat messages and wipe story data since the user is starting a brand new slate
		self.master.unsavedStoryMessages = [] #type: ignore
		self.master.currentStory = None #type: ignore
		self.master.isSavedStory = False #type: ignore
		self.master.isRemixedStory = False #type: ignore

		# Redirect the user to the ai chat page
		self.master.openPage("AIChatPage") #type: ignore