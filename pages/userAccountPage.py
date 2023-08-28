import tkinter as tk
import customtkinter as ctk

# For images
from PIL import Image, ImageTk
from urllib.request import URLopener

# May not even need these classes though, could just create 
# all of it in the constructor 'userAccountPage'

'''
BOOK MARK:
1. Create a user class so that you can test out how it looks
2. Finish this design. 
3. Then start working on login and register logic for database


'''

class userImageFrame(tk.Canvas):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		# Then user master to access a user 

class userInfoSection(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
class userAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		

		