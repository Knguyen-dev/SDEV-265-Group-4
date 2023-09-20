import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Message

'''
+ AIChatPage: Frame that represents the page where the user and AI send chat messages to each other in order to 
	write their story.

Attributes/Variables:
- master (App): 'App' class instance from 'Main.py' 
- remixGenObj: Generator object returned from AI that was passed from remixStoryPage.
	If it exists, the user is remixing a story, and this generator will output the AI's response, which 
	will be the first message in the user's remix. After it's used to generate the first message, we discard it, 
	and if the user goes to a different page, and then returns to continue the remix, remixGenObj should be None, but 
	the application will still correctly know that the user is remixing a story. 


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
- sendUserChat(self): Sends a user chat message to the AI and gets its response.
- renderChat(self, messageObj): Renders message text onto the screen given a messgae object.
'''
class AIChatPage(ctk.CTkFrame):
	def __init__(self, master, remixGenObj = None):
		super().__init__(master)
		self.master = master
		innerPageFrame = ctk.CTkFrame(self)
		innerPageFrame.pack(expand=True)
		header = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		heading = ctk.CTkLabel(header, text="Write Your Story!", font=("Helvetica", 32))
		storyStateMessage = ctk.CTkLabel(header, text="")
		self.pageStatusMessage = ctk.CTkLabel(header, text="StoryBot is currently waiting for your input.")
		
		self.chatBox = ctk.CTkTextbox(innerPageFrame, state="disabled", width=500, height=250)

		# Section with all of the input options the user has for the AIChatPage
		chatInputSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		self.chatEntry = ctk.CTkEntry(chatInputSection, width=300, placeholder_text="Send a message e.g. 'Once upon a time...'")
		self.openSaveStoryBtn = ctk.CTkButton(chatInputSection, text="Save Story", command=lambda: self.master.openPage("saveStoryPage")) #type: ignore
		self.sendChatBtn = ctk.CTkButton(chatInputSection, text="Send", command=self.sendUserChat)
		
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
		2. Using is currently writing a remixed story, it's unsaved. If remixGenObj, then the AI would be 
			generating the remix, which would be the first message of the chat.
		3. Using is continuing an unsaved story that isn't a remix.
		'''
		if self.master.isSavedStory: #type: ignore
			# Render saved messages associated with the current story
			for messageObj in self.master.currentStory.messages:
				self.renderChatMessageObj(messageObj)
			storyStateMessage.configure(text=f"Currently continuing '{self.master.currentStory.storyTitle}'!")
		elif self.master.isRemixedStory: #type: ignore
			'''
			NOTE: If remixGenObj exists, the user's previous page they were on was the remixStoryPage, and they were just redirected
			to the AIChatPage. 
			1. Process remixGenObj right after rendering unsavedStoryMessages to avoid duplication and rendering the content of remixGenObj twice.
			2. This also allows us to keep the logic for rendering unsaved messages in one place, which fits with all 3 cases very cleanly.
			'''
			storyStateMessage.configure(text=f"Currently writing a remix based on {self.master.currentStory.storyTitle}!")
		else:
			storyStateMessage.configure(text=f"Currently continuing writing a new story!")

		# If there have been any unsaved messages, render them 
		if self.master.unsavedStoryMessages:
			for messageObj in self.master.unsavedStoryMessages:
				self.renderChatMessageObj(messageObj)

		# Render the new message from the AI where the AI remixed the user's story
		if remixGenObj:
			self.processAIChat(remixGenObj)


	'''
	- Renders messageObj as chat messages on the screen
	- NOTE: Only good for rendering saved, unsaved, and user chats because those are easily in message object form.
		For rendering AI's response, it's a generator so use processAIChat(self).
	'''
	def renderChatMessageObj(self, messageObj):
		# Chat window is read and write now
		self.chatBox.configure(state="normal")
		messageText = messageObj.text

		# If it's an AI message, else it was a message sent by the user
		if messageObj.isAISender:
			messageText = "StoryBot: " + messageText
		else:
			messageText = f"{self.master.loggedInUser.username}: " + messageText

		# If the chatBox is empty, then it's the first message, else it's not the first message
		if self.chatBox.get("1.0", "end-1c") == "":
			self.chatBox.insert("1.0", messageText)
		else:
			self.chatBox.insert("end-1c", "\n\n" + messageText)

		# Scroll the chat window to the most recent message and make it read-only
		self.chatBox.see("end-1c")
		self.chatBox.configure(state="disabled")


	'''
	- Handles the proces of processing the AI's generated chat.
	1. Enable and disable certain parts of the UI, preventing the user from sending another 
		message to the AI until the first one is finished. Also prevent the user from being 
		able to redirect themselves to other pages, so that they don't lose their AI generated message.
	2. Renders chunks of the messages as they're being obtained from openai. 
	3. Save the ai's generated message to unsavedStoryMessages so that we can keep track of it
	'''
	def processAIChat(self, genObj):
		# Restrict user when AI is generating a response!
		self.sendChatBtn.configure(state="disabled")
		self.master.header.disableNavButtons()
		self.openSaveStoryBtn.configure(state="disabled")
		self.pageStatusMessage.configure(text="Please wait here until StoryBot is finished!")

		# Render the chunks of messages in the chatBox
		self.chatBox.configure(state="normal")
		chunkIndex = 0
		messageObj = Message(text="", isAISender=True) # message object that's going to represent store the message from the generator object
		for chunk in genObj:
			'''
			- Output Cases:
			1. First message in chat (chat is empty), and we're rendering the first chunk/part of the message
			2. First message in chat, but we aren't rendering the first chunk of said message
			3. Not the first message in chat, but we are rendering the first chunk
			4. Not the first message in chat, and it isn't the first chunk
			'''
			if self.chatBox.get("1.0", "end-1c") == "":
				if chunkIndex == 0:
					self.chatBox.insert("1.0", f"StoryBot: {chunk}")
				else:
					self.chatBox.insert("end-1c", chunk)
			else:
				if chunkIndex == 0:
					self.chatBox.insert("end-1c", "\n\n" + f"StoryBot: {chunk}")
				else:
					self.chatBox.insert("end-1c", chunk)
			chunkIndex += 1
			messageObj.text += chunk # add the chunk onto the message object's text since we want to keep track of this message
		self.master.unsavedStoryMessages.append(messageObj)
		
		# Scroll to bottom and make chatbox read only  
		self.chatBox.see("end-1c")
		self.chatBox.configure(state="disabled")
		'''
		- AI is done generating response, so unrestrict user!
		- After AI chat has been fully generated, allow the user to send a new message
		and go to other pages.
		'''
		self.sendChatBtn.configure(state="normal")
		self.openSaveStoryBtn.configure(state="normal")
		self.master.header.updateNavButtons()
		self.pageStatusMessage.configure(text="StoryBot is currently waiting for your input.")
		

	'''
	- Sends the user chat message to the ai, for the ai to respond, then goes to render both of those chat messages
	1. userMessage (Message): Message object containing text that the user sent
	2. AIMessage (Message): Message object containing text that the AI generated in response to the user
	'''
	def sendUserChat(self):
		# Get user's message as a message object. Then get AI's response message as a generator
		userMessage = Message(text=self.chatEntry.get(), isAISender=False)
		AIResponse = self.master.storyGPT.sendStoryPrompt(userMessage.text)

		# Clear entry widget when user sends a message
		self.chatEntry.delete(0, "end") 
		
		# Process and render user's message
		self.renderChatMessageObj(userMessage)
		self.master.unsavedStoryMessages.append(userMessage) #type: ignore	
		
		# Process and render AI's message
		self.processAIChat(AIResponse)