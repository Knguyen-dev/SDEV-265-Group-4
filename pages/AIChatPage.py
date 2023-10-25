import time
import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Message

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
		super().__init__(master, fg_color="#EBEBEB")
		self.master = master
		innerPageFrame = ctk.CTkFrame(self)
		innerPageFrame.pack(expand=True)
		header = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		heading = ctk.CTkLabel(header, text="Write Your Story!", font=("Helvetica", 32))
		storyStateMessage = ctk.CTkLabel(header, text="")
		self.pageStatusMessage = ctk.CTkLabel(header, text="StoryBot is currently waiting for your input.")
		
		self.chatBox = ctk.CTkTextbox(innerPageFrame, state="disabled", fg_color="white", wrap="word", width=500, height=250)

		# Section with all of the input options the user has for the AIChatPage
		chatInputSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		self.chatEntry = ctk.CTkEntry(chatInputSection, width=300, placeholder_text="Send a message e.g. 'Once upon a time...'")
		self.openSaveStoryBtn = ctk.CTkButton(chatInputSection, text="Save Story", fg_color="#0E4732", hover_color="#3A6152", command=lambda: self.master.openPage("saveStoryPage")) #type: ignore
		self.sendChatBtn = ctk.CTkButton(chatInputSection, text="Send", fg_color="#0E4732", hover_color="#3A6152", command=self.processUserChat)
		
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
		if self.master.isSavedStory: #type: ignore
			# Render saved messages associated with the current story
			for messageObj in self.master.currentStory.messages:
				self.renderChatMessageObj(messageObj)
			storyStateMessage.configure(text=f"Currently continuing '{self.master.currentStory.storyTitle}'!")
		elif self.master.isRemixedStory: #type: ignore
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
		self.chatBox.configure(state="normal")
		messageText = messageObj.text

		# If it's an AI message, else it was a message sent by the user
		if messageObj.isAISender:
			messageText = "StoryBot: " + messageText
		else:
			messageText = f"{self.master.loggedInUser.username}: " + messageText #type: ignore

		# If the chatBox is empty, then it's the first message, else it's not the first message
		if self.chatBox.get("1.0", "end-1c") == "":
			self.chatBox.insert("1.0", messageText)
		else:
			self.chatBox.insert("end-1c", "\n\n" + messageText)

		# Scroll the chat window to the most recent message and make it read-only
		self.chatBox.see("end-1c")
		self.chatBox.configure(state="disabled")


	
	def processAIChat(self):
		'''
		- Handles the proces of processing the AI's generated chat.
		1. Enable and disable certain parts of the UI, preventing the user from sending another 
			message to the AI until the first one is finished. Also prevent the user from being 
			able to redirect themselves to other pages, so that they don't lose their AI generated message.
		2. Renders chunks of the messages as they're being obtained from openai. 
		3. Save the ai's generated message to unsavedStoryMessages so that we can keep track of it
		'''
		# Disable send chat button as user can't send another chat until the ai is finished
		self.sendChatBtn.configure(state="disabled")		

		# Make the chat box writable
		self.chatBox.configure(state="normal")

		# Ensure user can't navigate to other pages while AI is generating message
		self.master.header.disableNavButtons() #type: ignore
		self.openSaveStoryBtn.configure(state="disabled")

		# Update page status message to indicate that AI is currently generating a message 
		self.pageStatusMessage.configure(text="Please wait here until StoryBot is finished!")
		
		# Message object that contains the text from the generator
		messageObj = Message(text="", isAISender=True) 
		chunkIndex = 0

		# Insert two newlines so that there's a space between the user's message and the ai's message 
		self.chatBox.insert("end", "\n\nStoryBot: ")
		# Iterate through chunks to render and process them
		for chunk in self.master.storyGenObj: #type: ignore
			if any(chunk.endswith(char) for char in ['.', '?', '!']):
				punct_marks = ['.', '?', '!']
				for mark in punct_marks:
					if chunk.endswith(f'{mark}'):
						self.chatBox.insert('end', f"{mark}" + " ")
			else:
				self.chatBox.insert('end', chunk)
				
			# For smooth rendering
			self.chatBox.update()
			time.sleep(0.03)

			# add the chunk onto the message object's text since we want to keep track of this message; then increment chunkIndex
			messageObj.text += chunk
			chunkIndex += 1
			
		# AI response processing is done, so append message object and variables related to processing a message
		self.master.unsavedStoryMessages.append(messageObj) #type: ignore
		self.master.storyGenObj = None #type: ignore

		# Scroll to bottom and make chatbox read only
		self.chatBox.see("end-1c")
		self.chatBox.configure(state="disabled")

		# Allow the user to send another message and navigate to other pages
		self.openSaveStoryBtn.configure(state="normal")
		self.sendChatBtn.configure(state="normal")
		self.master.header.updateNavButtons() #type: ignore

		# Update the page status message to indicate the ai is done
		self.pageStatusMessage.configure(text="StoryBot is currently waiting for you input.")
		


	
	def processUserChat(self):
		'''
		- Sends the user chat message to the ai, for the ai to respond, then goes to render both of those chat messages
		1. userMessage (Message): Message object containing text that the user sent
		2. AIResponse (Generator): Generator object containing text that the AI generated in response to the user
		'''
		# Check if user actually sent something
		if (self.chatEntry.get().strip() == ""):
			self.pageStatusMessage.configure(text="Please enter text before trying to send a message!")
			return

		# Process and render the user's message
		userMessage = Message(text=self.chatEntry.get(), isAISender=False)
		self.renderChatMessageObj(userMessage)
		self.master.unsavedStoryMessages.append(userMessage) #type: ignore	
		
		# Clear entry widget when user sends a message
		self.chatEntry.delete(0, "end")
			
		AIResponse = self.master.storyGPT.sendStoryPrompt(userMessage.text) #type: ignore
		self.master.storyGenObj = AIResponse # type: ignore 

		# Process and render AI's message
		self.processAIChat()