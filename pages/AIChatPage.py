import time
import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Message
from tkinter import messagebox

'''
+ AIChatPage: Frame that represents the page where the user and AI send chat messages to each other in order to 
	write their story.

Attributes/Variables:
- master (App): 'App' class instance from 'Main.py' 
- innerPageFrame (CTkFrame): Page frame that contains all of the widgets for the page and is used to center it
- header (CTkFrame): Header of the page frame
- heading (CTkLabel): Heading message
- storyStateMessage (CTkLabel): Label that tells the user what kind of story they're writing, whether they're remixing, writing 
	a new story, continuing a saved story, etc.
- pageStatusMessage (CTkLabel): Indicates status of the page like when the user is currently waiting on the AI for a response
	or whether an occur has occurred.
- chatBox (CTkTextbox): Textbox that shows the messages of the user and AI.
- chatInputSection (CTkFrame): Section with all of the input related widgets
- chatEntry (CTkEntry): Input text box where user types in their message
- openSaveStoryBtn (CTkButton): Button that redirects the user to the saveStoryPage
- sendChatBtn (CTkButton): Button that sends the chat to the AI.

Methods:
- processUserChat(self): Sends a user chat message to the AI and gets its response.
- renderChat(self, messageObj): Renders message text onto the screen given a messgae object.
'''
class AIChatPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)

		# This logic prevents the dynamically resizing msgbox from overexpanding - Nuke The Dev
		self.msgbox_height=20
		self.max_msgbox_height = 300
		
		innerPageFrame = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		innerPageFrame.pack(expand=True)
		header = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		heading = ctk.CTkLabel(header, text="Write Your Story!", font=("Helvetica", 32), text_color=self.master.theme["label_clr"])
		storyStateMessage = ctk.CTkLabel(header, text="", text_color=self.master.theme["label_clr"])
		self.pageStatusMessage = ctk.CTkLabel(header, text="StoryBot is currently waiting for your input.", text_color=self.master.theme["label_clr"])

		# Section with all of the input options the user has for the AIChatPage
		chatInputSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		self.chatEntry = ctk.CTkEntry(chatInputSection, width=300, placeholder_text="Send a message e.g. 'Once upon a time...'", fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"], )
		self.chatBox = ctk.CTkScrollableFrame(innerPageFrame, fg_color=self.master.theme["main_clr"], width=500, height=250)
		self.openSaveStoryBtn = ctk.CTkButton(chatInputSection,  text="Save Story", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=lambda: self.master.openPage("saveStoryPage"))
		self.sendChatBtn = ctk.CTkButton(chatInputSection, text="Send",  text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"], command=self.processUserChat)
	
		# Structure and style widgets accordingly
		header.grid(row=0, column=0, pady=10)
		heading.grid(row=0, column=0)
		storyStateMessage.grid(row=1, column=0)
		self.pageStatusMessage.grid(row=2, column=0)
		self.chatBox.grid(row=1, column=0, pady=10)
		chatInputSection.grid(row=2, column=0, pady=20)
		self.chatEntry.grid(row=0, column=0, padx=10, pady=5)
		self.sendChatBtn.grid(row=0, column=1, padx=10)
		self.openSaveStoryBtn.grid(row=0, column=2, padx=10)

		'''
		- Cases for the initial state:
		1. User is continuing a saved story
		2. Using is currently writing a remixed story, it's unsaved. If storyGenObj is detected with the constructor's logic then 
			we're rendering the AI's first response to a user's remixed story, which would be the first message of the chat.
		3. Using is continuing an unsaved story that isn't a remix.
		'''
		if self.master.isSavedStory: 
			# Render saved messages associated with the current story
			for messageObj in self.master.currentStory.messages:
				self.renderChatMessageObj(messageObj)
			storyStateMessage.configure(text=f"Currently continuing '{self.master.currentStory.storyTitle}'!")
		elif self.master.isRemixedStory: 
			storyStateMessage.configure(text=f"Currently writing a remix based on '{self.master.currentStory.storyTitle}'!")
		else:
			storyStateMessage.configure(text=f"Currently continuing writing a new story!")

		# If there have been any unsaved messages, render them 
		if self.master.unsavedStoryMessages:
			for messageObj in self.master.unsavedStoryMessages:
				self.renderChatMessageObj(messageObj)

		# if storyGenObj exists, then we have to process a generator that the AI returned
		# NOTE: In this case, when storyGenObj exists here, that means it was set by the remixStoryPage, 
		# and this generator contains a response for remixing a story
		if self.master.storyGenObj:
			self.processAIChat()


	
	def renderChatMessageObj(self, messageObj):
		'''
		- Renders messageObj as chat messages on the screen
		- NOTE: Only good for rendering saved, unsaved, and user chats because those are easily in message object form.
			For rendering AI's response, it's a generator so use processAIChat(self).
		'''
		# Chat window is read and write now
		messageText = messageObj.text


		# If there are messages write the response in the current msgbox, if not create one then write to it
		if self.master.msgboxes:
			msgbox = self.master.msgboxes[len(self.master.msgboxes)]
			msgbox.insert("1.0", messageText)
		else:
			# access the last msgbox to print to
			msgbox = self.drawMsgBox()
			msgbox.insert("1.0", messageText)

		num_chars = len(messageObj.text)  # The number of characters in the text

		# Calculate the number of lines at 61 characters per line of text onscreen
		num_lines = num_chars // 61  # Use integer division to get the number of full lines
		if num_chars % 61 > 0:  # If there are any remaining characters, they will form an additional line
			num_lines += 1

		# Calculate the height
		height = num_lines * 10  # Each line is 10 units high

		# Now you can use `height` to set the height of your CTkTextbox
		msgbox.configure(height=height)
		
		# If it's an AI message, else it was a message sent by the user
		if messageObj.isAISender:
			self.drawSenderTag(sender='Story Bot:')
		else:
			self.drawSenderTag(sender=f'{self.master.loggedInUser.username}') 

	def processUserChat(self):
		'''
		- Sends the user chat message to the ai, for the ai to respond, then goes to render both of those chat messages
		1. userMessage (Message): Message object containing text that the user sent
		2. AIResponse (Generator): Generator object containing text that the AI generated in response to the user
		'''
		# Check if user actually sent something
		if (self.chatEntry.get().strip() == ""):
			messagebox.showwarning('Empty Message!', 'Please enter a valid message!')
			return

		# Process and render the user's message
		# The .strip() method ensures that a user cannot type whitespaces 
		# before the message content which has been known to cause an openAI api exception
		userMessage = Message(text=self.chatEntry.get().strip(), isAISender=False)
		self.renderChatMessageObj(userMessage)
		self.master.unsavedStoryMessages.append(userMessage) 	
		
		# Clear entry widget when user sends a message
		self.chatEntry.delete(0, "end")
			
		AIResponse = self.master.storyGPT.sendStoryPrompt(userMessage.text) 
		self.master.storyGenObj = AIResponse # type: ignore 

		# Process and render AI's message
		self.processAIChat()

	def drawMsgBox(self):
		msgbox = ctk.CTkTextbox(self.chatBox, fg_color=self.master.theme["entry_clr"], width=450, height=10, wrap="word", activate_scrollbars=True)
		msgbox.configure(font=("Helvetica", 16))
		self.master.msgboxes.append(msgbox)
		msgbox.grid(row=len(self.master.msgboxes), column=0, padx=5, pady=5, sticky="nsew")
		return msgbox
	
	def drawSenderTag(self, sender):
		sender_lbl = ctk.CTkLabel(self.chatBox, font=("Helvetica", 12), text=sender)
		sender_lbl.grid(row=[len(self.master.msgboxes)-1], column=0, padx=10, pady=5, sticky="w")
		return

	def processAIChat(self):
		'''
		- Handles the proces of processing the AI's generated chat.
		1. Enable and disable certain parts of the UI, preventing the user from sending another 
			message to the AI until the first one is finished. Also prevent the user from being 
			able to redirect themselves to other pages, so that they don't lose their AI generated message.
		2. Renders chunks of the messages as they're being obtained from openai. 
		3. Save the ai's generated message to unsavedStoryMessages so that we can keep track of it
		'''

		# Access the current messagebox at it's index
		# Disable send chat button as user can't send another chat until the ai is finished
		self.sendChatBtn.configure(state="disabled")		

		# Ensure user can't navigate to other pages while AI is generating message
		self.master.sidebar.disableSidebarButtons()
		self.openSaveStoryBtn.configure(state="disabled")

		# Update page status message to indicate that AI is currently generating a message 
		self.pageStatusMessage.configure(text="Please wait here until StoryBot is finished!")
		
		# Message object that contains the text from the generator
		messageObj = Message(text="", isAISender=True) 
		chunkIndex = 0

		
		# Create a new real-time dynamically resizing msg bubble to display AI response in
		msgbox = self.drawMsgBox()
		# Make the chat box writable
		msgbox.configure(state="normal")

		self.drawSenderTag(sender='Story Bot:')
		# Iterate through chunks to render and process them
		for chunk in self.master.storyGenObj: 
			if any(chunk.endswith(char) for char in ['.', '?', '!']):
				punct_marks = ['.', '?', '!']
				for mark in punct_marks:
					if chunk.endswith(f'{mark}'):
						msgbox.insert('end', f"{mark}" + " ")
				# Increment the height of the textbox in real-time
				inc_height=4
			else:
				msgbox.insert('end', chunk)
				inc_height=2
			
			# Enables smooth real time typing
			if (self.msgbox_height <= self.max_msgbox_height):
					self.msgbox_height += inc_height

			# Dynamically resize the height of the current msgbox
			msgbox.update()
			msgbox.configure(height=self.msgbox_height)
			# add the chunk onto the message object's text since we want to keep track of this message; then increment chunkIndex
			messageObj.text += chunk
			chunkIndex += 1

		#reset the msgbox height after each message
		self.msgbox_height=20
			
		# AI response processing is done, so append message object and variables related to processing a message
		self.master.unsavedStoryMessages.append(messageObj) 
		self.master.storyGenObj = None 

		# Scroll to bottom and make chatbox read only
		msgbox.see("end-1c")
		msgbox.configure(state="disabled")

		# Allow the user to send another message and navigate to other pages
		self.openSaveStoryBtn.configure(state="normal")
		self.sendChatBtn.configure(state="normal")
		self.master.sidebar.updateSidebar() 

		# Update the page status message to indicate the ai is done
		self.pageStatusMessage.configure(text="StoryBot is currently waiting for you input.")