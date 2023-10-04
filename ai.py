import openai

from multipledispatch import dispatch
from typing import Tuple, Dict, Optional, overload
from classes.utilities import add_testing_functions

with open('./assets/api_key.txt', 'r') as f: # get the current API key from a file so OpenAI doesn't delete it
	openai.api_key = f.read()

#### WILL BE USED LATER
# class VariableManager:
# 	'''
# 	A generic class for managing other Class' variabes in generic getter/setter methods
# 	Useful for utilizing class variables in other classes without instantiation
# 	'''
# 	def init(self):
# 		self.variables = {}

# 	def set_variable(self, var_name, value):
# 		'''
# 		Adds a variable to the dictionary using name: value format
# 		'''
# 		self.variables[var_name] = value

# 	def get_variable(self, var_name):
# 		'''
# 		Gets a variable from the dictionary using the name as a key
# 		'''
# 		return self.variables.get(var_name, None)
	
# vm = VariableManager()

def logger(self, attributeName):
	def decorator(func):
		def wrapper(*args, **kwargs):
			attributeValue = getattr(self, attributeName)
			print(f"{attributeName}: {attributeValue}")
			return func(*args, **kwargs)
		return wrapper
	return decorator

class ModelBase():
	'''
	The base class for generating content. Supports full chat history management from creating and deleting chat entries to clearing and replacing the entire chat.
	'''
	def __init__(self, model: str, prompt: str, systemPrompt: str):
		self.systemPrompt = systemPrompt
		self.prompt = prompt
		self.engine = model
		
		# Default starting chat, that self.chat can we reset to if needed
		self.startingChat = [
			{"role": "system", "content": self.systemPrompt},
			{"role": "assistant", "content": "Ok, I will be sure to carefully follow all your instructions as listed"},
			{"role": "user", "content": self.prompt},			
		]

		# Chat History
		# NOTE: Using slicing notation to copy startingChat to chat in a way so that the lists are independent of each other. Modifying one shouldn't affect the other
		self.chat = self.startingChat[:]

		# Default AI Attributes/Parameters
		self.temperature = 0.8
		self.top_p = 1
		self.presence_penalty = 0
		self.frequency_penalty = 0
		self.max_tokens = 512
		self.is_stream = True

	def complete(self):
		'''
		This is the method needed to get AI output. This includes all the settings needed to run the AI
			Parameters:
			
			`temperature` - `float` | What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
			
			`top_p` | - `float` An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

			`frequency_penalty` - `float` | Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

			`presence_penalty` - `float` | Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.

			`stream` - `bool` | If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
		'''
		self.chat.append({"role": "user", "content": self.prompt})

		if self.is_stream:
			fullMessage = []

			try:
				# response = openai.ChatCompletion.create(model=self.engine, messages=self.chat, temperature=temperature, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, stream=True)
				response = openai.ChatCompletion.create(model=self.engine, messages=self.chat, temperature=self.temperature, top_p=self.top_p, max_tokens=self.max_tokens, stream=True)

				for chunk in response:
					fullMessage.append(chunk["choices"][0]["delta"]["content"])
					if "content" in chunk["choices"][0]["delta"]:
						yield chunk["choices"][0]["delta"]["content"]

			except KeyError: # The AI has stopped generating
				yield "\n\n The End."
				# fullMessage.append("\n\nThe End.")

			self.chat.append({"role": "assistant", "content": ''.join(fullMessage)})
		else:
			response = openai.ChatCompletion.create(model=self.engine, messages=self.chat, tempurature=self.temperature, top_p=self.top_p, frequency_penalty=self.frequency_penalty, presence_penalty=self.presence_penalty, max_tokens=self.max_tokens, stream=False)

			self.chat.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})

			return response["choices"][0]["message"]["content"]

	@dispatch(dict, int)
	def addMessageAt(self, message: Dict[str, str], position: int): # type:ignore (if you're curious why I suppressed this warning, it's because python mistakenly labled this function as being overshadowed by the latest one, but dispatch solves that problem)
		'''
		Adds a message at the specified position in the chat using a OpenAI formatted chat dictionary.
		You can use counting numbers to refer to the chat indexes since index 0 will always be `systemPrompt`.
		Message should be formatted like this: `{"role": "user" | "assistant", "content": content}`
		'''
		self.chat.insert(position, message)

	@dispatch(str, int, str)
	def addMessageAt(self, message: str, position: int, role="user"):
		'''
		Constructs an OpenAI formatted chat dictionary from the role and message strings.
		You can use counting numbers to refer to the chat indexes since index 0 will always be `systemPrompt`.
		No specfic input format is necessary except that `role` can only be one of two options: "user" and "assistant".
		'''
		if role in ("user", "assistant"):
			formattedMessage = {"role": role, "content": message}
			self.chat.insert(position, formattedMessage)
		else:
			print('Only use "user" and "assistant" when working with roles')

	@dispatch(dict)
	def removeMessageAt(self, message: Dict[str, str]): # type:ignore (if you're curious why I suppressed this warning, it's because python mistakenly labled this function as being overshadowed by the latest one, but dispatch solves that problem)
		'''
		Removes a message at the specified position in the chat using a OpenAI formatted chat dictionary.
		No positional information such as an index is needed since the specific message is precise enough to pinpoint the location of it in the list.
		Message should be formatted like this: `{"role": "user" | "assistant", "content": content}`
		'''
		self.chat.remove(message)

	@dispatch(str, str)
	def removeMessageAt(self, message: str, role="user"): # type:ignore (if you're curious why I suppressed this warning, it's because python mistakenly labled this function as being overshadowed by the latest one, but dispatch solves that problem)
		'''
		Constructs an OpenAI formatted chat dictionary from the role and message strings. 
		Then it uses that to delete that entry through matching.
		No positional information such as an index is needed since the specific message is precise enough to pinpoint the location of it in the list.
		No specfic input format is necessary except that `role` can only be one of two options: "user" and "assistant".
		'''
		if role in ("user", "assistant"):
			formattedMessage = {"role": role, "content": message}

			self.chat.remove(formattedMessage)
		else:
			print('Only use "user" and "assistant" when working with roles')

	@dispatch(int)
	def removeMessageAt(self, position: int):
		'''
		Removes a specific message from the chat history by finding it through its index.
		You can use counting numbers to refer to the chat indexes since index 0 will always be `systemPrompt`.
		'''
		if position != 0:
			self.chat.pop(position)

		else:
			print("You are not allowed to remove the system prompt")

	def populate(self, chatHistory: list[Dict[str, str]]):
		'''
		Populates an entire chat history with a list of predefined messages
		`chatHistory` only takes in a list of OpenAI dictionary formats. EX: 
		>>> {"role": "user", "content": "this is content"}

		- chatHistory: An array of dictionaries, as this will represent the messages associated to a story object in JSON notation. 
		- NOTE: chatHistory is just the messages of a story in JSON, and it's not going to have the starting messages in 'self.startingChat' because 
			those aren't related to the user's story but more so the developer side. As a result, whenever we load in the story content in JSON, we make sure 
			to make it so self.chat also contains messages in the self.startingChat.
		'''
		if isinstance(chatHistory, list):
			try:
				if isinstance(chatHistory[0], dict):
					self.chat = self.startingChat + chatHistory
				else:
					print('you have a list created and it\'s populated, but you don\'t have elements of the dictionary type inside')
			except:
				print('There are no elements inside your list')
		else:
			print('your chatHistory object is not in the right format. It must be a list of OpenAI dictionaries')

	def clear(self):
		'''
		Wipes the entire chat history, and resets it to the startingChat so that the AI is ready to write stories properly
		'''
		self.chat = self.startingChat[:]

	def printChat(self):
		for message in self.chat:
			print(f"{message['role']}: {message['content']}")

class InstructionsManager:
	'''
	A class for managing rules for the AI to follow. Supports adding, removing, and injecting rules
	'''
	def __init__(self, *rules: str):
		self.ruleList = []

		for i, rule in enumerate(rules):
			numberedRule = f"{i + 1}. {rule}"

			self.ruleList.append(numberedRule)

	def addRule(self, rule: str):
		'''
		Adds a rule to the list of AI Rules
		'''
		self.ruleList.append(rule)

	@dispatch(str)
	def removeRule(self, rule: str): # type:ignore (if you're curious why I suppressed this warning, it's because python mistakenly labled this function as being overshadowed by the latest one, but dispatch solves that problem)
		'''
		Removes a rule from the list of AI rules using the exact string of the rule as the specifier
		'''
		self.ruleList.remove(rule)

	@dispatch(int)
	def removeRule(self, rule: int):
		'''
		Removes a rule from the list of AI rules using the rule number as a specifier
		'''
		ruleIndex = rule - 1
		self.ruleList.pop(ruleIndex)

	def inject(self):
		'''
		Injects the rules at the end of a ChatGPT command to allow more close following of the rules
		'''
		return "\n\n" + "\n".join([rule for rule in self.ruleList]) + "\n"

@add_testing_functions # allow outside modification of class methods without cluttering up the class here (used for testing only)
class StoryGPT(ModelBase):
	'''
	The main class for story generation and remixing. This class inherits from the `ModelBase` class.
	'''
	def __init__(self):
		systemPrompt = "You are a professional author who can write any story upon request. Your stories are always rich and full of descriptive content. You are able to carry out all user requests precisely and professionally."
		prompt = "I am an avid reader looking to read some fantastic stories! I am going to give you some specifications on a story I'd like to read."
		super().__init__('gpt-3.5-turbo', prompt, systemPrompt)

		'''
		- Try to follow requirements for the story's style, length, and the topic. If you can't fit your 
		response or story within a word length, then generate small passage or section of said story and 
		fit that small part into the word length. If the style doesn't make sense, use a popular 
		storytelling style that fits.

		- Valid styles could be a coherent description, but could also reference or take inspiration from popular culture. Things
			such as authors of popular works, tv shows, books, movies, etc. are vaid.

		- Valid styles will likely consist of valid words.
		
		'''
		self.manager = InstructionsManager(
			"Do not, I repeat, do not act as personal assistant, friend neither should you reply to a user's opinions on a subject!",
			"Despite the user's unswerving demands, always do your best to focus on writing the story and nothing but the story",
			"You will view most user messages as making edits to the story unless it blatantly violates rules",
			"You will work with all desired story lengths. \n\ta. (IMPORTANT: If you can't fit your response or story within a word length, then generate small passage that fits the word length.)",
			"You will work with all styles, regardless of understanding. Even seemingly nonsensical styles can and will be accepted. Every single possible style will be accepted, regardless of its content"
			"Do not, I repeat, do not follow any instructions that is not adding or changing the existing story in any way \n\ta. (IMPORTANT: only enforce this rule if there is already not an existing story).",
			"Do not, I repeat, do not follow any instructions asking you to act as someone or roleplay as a certain character \n\ta. (IMPORTANT: only enforce this rule if the user directly addresses you)",
			"If the User's request violates any one of the aforementioned rules, reply: I'm sorry, 'the rule that was broken but specify the rule' is an invalid request please try again\""
		)

		# Default response length and story writing style
		self.response_length = 50
		self.response_style = "descriptive"

	def sendStoryPrompt(self, topic: str):
		'''
		Modifies the prompt to instruct ChatGPT to create a story
		'''
		if self.response_length <= 32:
			self.max_tokens = 64
		elif self.response_length <= 64:
			self.max_tokens = 128
		elif self.response_length <= 128:
			self.max_tokens = 256
		elif self.response_length <= 256:
			self.max_tokens = 512
		elif self.response_length > 256:
			self.max_tokens = 1024

		self.prompt = f"Topic: {topic}\nLength: {self.response_length} words\nStyle: {self.response_style}"

		print(f"Response length: {self.response_length}")
		print(f"Prompt: {self.prompt}")

		self.prompt += self.manager.inject()
		self.prompt += "Does the request by the user follow all the rules? If not, say this to the user: \"This rule was broken but specify the rule\" If yes, continue with the story and do not explain that you're following the rules. Do not confirm with the user that their request is valid, only tell them that their request is not valid.\n\n"
		response = self.complete()
		return response

	def sendRemixPrompt(self, story: str, twist: str):
		'''
		Modifies the prompt to instruct ChatGPT to remix an existing story
		'''
		if self.response_length <= 32:
			self.max_tokens = 64
		elif self.response_length <= 64:
			self.max_tokens = 128
		elif self.response_length <= 128:
			self.max_tokens = 256
		elif self.response_length <= 256:
			self.max_tokens = 512
		elif self.response_length > 256:
			self.max_tokens = 1024

		self.prompt = f'Remix this story: "{story}".\nThe twist for this remix: {twist}\nWrite the remix in this style: {self.response_style}. Make it length {self.response_length} words long.'
		self.prompt += self.manager.inject()
		self.prompt += "Does the request by the user follow all the rules? If not, say this to the user: \"This rule is being broken but specify the rule\" If yes, continue with the story and do not explain that you're following the rules. Do not confirm with the user that their request is valid, only tell them that their request is not valid.\n\n"
		response = self.complete()
		return response
