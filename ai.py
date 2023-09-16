import openai
from typing import Tuple, Dict, Optional, overload

openai.api_key = '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'

class VariableManager:
	'''
	A generic class for managing other Class' variabes in generic getter/setter methods
	Useful for utilizing class variables in other classes without instantiation
	'''
	def init(self):
		self.variables = {}

	def set_variable(self, var_name, value):
		'''
		Adds a variable to the dictionary using name: value format
		'''
		self.variables[var_name] = value

	def get_variable(self, var_name):
		'''
		Gets a variable from the dictionary using the name as a key
		'''
		return self.variables.get(var_name, None)
	
vm = VariableManager()

class ModelBase():
	def __init__(self, model: str, prompt: str, systemPrompt: str):
		self.system = systemPrompt
		self.prompt = prompt
		self.engine = model

		self.chat = [
			{"role": "system", "content": self.system},
			{"role": "assistant", "content": "Ok, I will be sure to carefully follow all your instructions as listed"}
		]

		# Default AI Attributes/Parameters
		self.temperature = 0.8
		self.top_p = 1
		self.presence_penalty = 0
		self.frequency_penalty = 0
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
				response = openai.ChatCompletion.create(model=self.engine, messages=self.chat, temperature=self.temperature, top_p=self.top_p, stream=True)

				for chunk in response:
					fullMessage.append(chunk["choices"][0]["delta"]["content"])
					if "content" in chunk["choices"][0]["delta"]:
						yield chunk["choices"][0]["delta"]["content"]
			except KeyError:
				yield "\n\n The End."

				fullMessage.append("\n\nThe End.")

			# print(fullMessage)

			self.chat.append({"role": "assistant", "content": ''.join(fullMessage)})
		else:
			response = openai.ChatCompletion.create(model=self.engine, messages=self.chat, tempurature=self.temperature, top_p=self.top_p, frequency_penalty=self.frequency_penalty, presence_penalty=self.presence_penalty, stream=False)

			self.chat.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})

			return response["choices"][0]["message"]["content"]

	@overload
	def addMessageAt(self, message: Dict[str, str], position: int):
		'''
		Adds a message at the specified position in the chat using a OpenAI formatted chat dictionary.
		You can use counting numbers to refer to the chat indexes since index 0 will always be `systemPrompt`.
		Message should be formatted like this: `{"role": "user" | "assistant", "content": content}`
		'''
		...

	@overload
	def addMessageAt(self, message: str, position: int, role="user"):
		'''
		Constructs an OpenAI formatted chat dictionary from the role and message strings.
		You can use counting numbers to refer to the chat indexes since index 0 will always be `systemPrompt`.
		No specfic input format is necessary except that `role` can only be one of two options: "user" and "assistant".
		'''
		...

	def addMessageAt(self, message: Dict[str, str] | str, position: int, role="user"):
		if isinstance(message, dict):
			self.chat.insert(position, message)

		elif isinstance(message, str):
			if role in ("user", "assistant"):
				formattedMessage = {"role": role, "content": message}

				self.chat.insert(position, formattedMessage)
			else:
				print('Only use "user" and "assistant" when working with roles')

	def populate(self, chatHistory: list[Dict[str, str]]):
		'''
		Populates an entire chat history with a list of predefined messages
		`chatHistory` only takes in a list of OpenAI dictionary formats. EX: 
		>>> {"role": "user", "content": "this is content"}
		'''
		if isinstance(chatHistory, list):
			try:
				if isinstance(chatHistory[0], dict):
					self.chat = chatHistory
				else:
					print('you have a list created and it\' populated, but you don\'t have elements of the dictionary type inside')
			except:
				print('There are no elements inside your list')
		else:
			print('your chatHistory object is not in the right format. It must be a list of OpenAI dictionaries')

	def clear(self):
		'''
		Wipes the entire chat history
		'''
		self.chat = self.chat[:3]

class InstructionsManager:
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

	@overload
	def removeRule(self, rule: str):
		'''
		Removes a rule from the list of AI rules using the exact string of the rule as the specifier
		'''
		...

	@overload
	def removeRule(self, rule: int):
		'''
		Removes a rule from the list of AI rules using the rule number as a specifier
		'''
		...

	def removeRule(self, rule: str | int):
		if isinstance(rule, str):
			self.ruleList.remove(rule)

		elif isinstance(rule, int):
			ruleIndex = rule - 1
			self.ruleList.pop(ruleIndex)

	def inject(self):
		'''
		Injects the rules at the end of a ChatGPT command to allow more close following of the rules
		'''
		return "\n\n" + "\n".join([rule for rule in self.ruleList]) + "\n"

class StoryGPT(ModelBase):
	def __init__(self):
		systemPrompt = ""
		prompt = "I am an avid reader looking to read some fantastic stories!"
		super().__init__('gpt-3.5-turbo', prompt, systemPrompt)

		self.manager = InstructionsManager("You will only generate stories, and nothing else", "You will not talk to the user", "You will follow all requirements for story style, length, and topic")

		self.addMessageAt(prompt, 2, "user")

	def sendStoryPrompt(self, topic: str, length: int = 75, style: str = "None"):
		'''
		Modifies the prompt to instruct ChatGPT to create a story
		'''
		self.prompt = f"Topic: {topic}\nLength: {length} words\nStyle: {style}"
		self.prompt += self.manager.inject()
		print(self.prompt)

		response = self.complete()

		return response

	def sendRemixPrompt(self, story: str, style: str = "None"):
		'''
		Modifies the prompt to instruct ChatGPT to remix an existing story
		'''
		self.prompt = f'Remix this story: "{story}"\nStyle: {style}'
		self.prompt += self.manager.inject()
		print(self.prompt)