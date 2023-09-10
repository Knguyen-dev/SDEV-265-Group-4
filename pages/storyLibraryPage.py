import customtkinter as ctk

# Page for storing all of the user's saved stories
class storyLibraryPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# Inner page frame for centering content at center of storyLibraryPage frame
		innerPageFrame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=625, height=500)
		innerPageFrame.pack(expand=True)
		
		# Get the saved stories, from the logged in user, if there are any
		savedStories = self.master.loggedInUser.stories

		# If there aren't any stories saved, then just show a message, and stop it early
		if not savedStories:
			label = ctk.CTkLabel(innerPageFrame, text="No stories have been saved yet!", font=("Helvetica", 24))
			label.pack()
			return

		rowIndex = 0
		columnIndex = 0
		# At this point, there are stories, so iteratively create 'cards' or containers that display
		# their information
		for story in savedStories:
			storyCard = ctk.CTkFrame(innerPageFrame, fg_color="#7dd3fc", width=200)

			# columnIndex number of story cards per row
			# if true, then columnIndex story cards have already been placed, so reset
			# the column index, and move on to a new row
			if (columnIndex == 3):
				columnIndex = 0
				rowIndex += 1

			cardHeader = ctk.CTkFrame(storyCard)
			cardTitle = ctk.CTkLabel(cardHeader, fg_color="#7dd3fc", text=f"Title: {story.storyTitle}", wraplength=200)
			cardBody = ctk.CTkFrame(storyCard, fg_color="#7dd3fc")
			continueSavedStoryBtn = ctk.CTkButton(cardBody, text="Continue", command=lambda story=story: self.continueSavedStory(story))
			openRemixStoryBtn = ctk.CTkButton(cardBody, text="Remix", command=lambda story=story: self.master.openPage("remixStoryPage", story))  #type: ignore
			deleteSavedStoryBtn = ctk.CTkButton(cardBody, text="Delete", command=lambda story=story: self.deleteSavedStory(story))
			
			# Structure the storyCard and its widgets
			storyCard.grid(row=rowIndex, column=columnIndex, padx=10, pady=10)
			cardHeader.grid(row=0, column=0, pady=10)
			cardTitle.grid(row=0, column=0)
			cardBody.grid(row=1, column=0)
			continueSavedStoryBtn.grid(row=0, column=0, pady=5)
			openRemixStoryBtn.grid(row=1, column=0, pady=5)
			deleteSavedStoryBtn.grid(row=2, column=0, pady=5)

			# Increment column count
			columnIndex += 1
		
	'''
	+ continueSavedStory: Let the user continue where they left off 
	'''
	def continueSavedStory(self, story):
		# Update the saved story that we are currently continuing
		self.master.currentStory = story #type: ignore
		self.master.isSavedStory = True #type: ignore
		self.master.isRemixedStory = False #type: ignore

		# If the user is continuing a saved story, they're starting a new chat, so wipe out all of the unsaved messages they have first
		self.master.unsavedStoryMessages = [] #type: ignore

		# Redirect user to the ai chat page
		self.master.openPage("AIChatPage") #type: ignore


	# Deletes a story from the user's library
	def deleteSavedStory(self, story):
		'''
		- If currentStory == story, there are two cases:
		1. The story that the user is deleting is the same saved story that they are continuing
		2. The story that the user is deleting, is the story that they are currently remixing off of.
		'''
		if self.master.currentStory == story: #type: ignore
			# Reset currentStory since it's being deleted from database
			self.master.currentStory = None #type: ignore
			# 1
			if self.master.isSavedStory: #type: ignore
				self.master.isSavedStory = False #type: ignore
			elif self.master.isRemixedStory: #type: ignore
			# 2
				self.master.isRemixedStory = False #type: ignore	
			# Wipe the unsaved story messages because they would have been related to the story that 
			# the user was going to delete.
			self.master.unsavedStoryMessages = [] #type: ignore
		
		# Delete story from database
		self.master.session.delete(story) #type: ignore
		self.master.session.commit() #type: ignore
		# Reload the story library page
		self.master.openPage("storyLibraryPage") #type: ignore	