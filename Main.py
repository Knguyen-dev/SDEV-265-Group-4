import importlib
import sqlite3
import tkinter as tk
import customtkinter as ctk 
from tkinter import messagebox 
import json, os, time
from PIL import Image
import datetime


ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"


class NavigationBar(ctk.CTkFrame):
	def __init__(self, master, openPageCallback):
		super().__init__(master, fg_color="black", corner_radius=0)
		self.master = master
		self.openPageCallback = openPageCallback

		# Create header message 
		welcomeLabel = ctk.CTkLabel(self, text="Welcome to BookSmart.AI!", text_color="white", font=("Helvetica", 32))
		welcomeLabel.grid(row=0, column=0, columnspan=5)
		# Create container for buttons and then the nav buttons
		navBtnFrame = ctk.CTkFrame(self, fg_color="black")
		navBtnFrame.grid(row=1, column=0, pady=20, columnspan=5)
		
		
		# List for all nav buttons
		self.navBtns = []
		# Create nav buttons with iteration
		self.navBtnMap = {
			"Home": "homePage",
			"AI Settings": "aiSettingsPage",
			"Library": "storyLibraryPage",
			"Login": "userLoginPage",
			"Account": "userAccountPage",
		}
		colCount = 0
		for key in self.navBtnMap:
			navBtn = ctk.CTkButton(navBtnFrame, corner_radius=0, text=f"{key}", command=lambda k=key:self.openPageCallback(self.navBtnMap[k]))
			navBtn.grid(row=0, column=colCount, padx=10)
			colCount += 1
			self.navBtns.append(navBtn)

		# Call function to make sure certain nav buttons direct users to the right places
		# based on their login state 
		self.updateNavButtons()


	'''
	- Update the nav buttons based on the login state of the user. If the user 
	isn't logged in, and they're trying to access pages that need an account logged in, 
	then we redirect them to the login page. Else we maintain our regular button links
	1. Get buttons that direct you to the library and account page
	2. If: The user is logged in, then those buttons lead to their respective places
	3. Else: Both buttons lead to the login page 
	'''
	def updateNavButtons(self):
		if self.master.loggedInUser:
			self.navBtns[2].configure(command=lambda: self.openPageCallback(self.navBtnMap["Library"]))
			self.navBtns[4].configure(command=lambda: self.openPageCallback(self.navBtnMap["Account"]))
		else:
			self.navBtns[2].configure(command=lambda: self.openPageCallback(self.navBtnMap["Login"]))
			self.navBtns[4].configure(command=lambda: self.openPageCallback(self.navBtnMap["Login"]))


class Footer(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="black", corner_radius=0)
		currentYear = datetime.datetime.now().year
		footerLabel = ctk.CTkLabel(self, text=f"BookSmart {currentYear}", text_color="white",	font=("Helvetica", 16))
		footerLabel.pack()

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("BookSmart.Ai")
		self.width = self.winfo_screenwidth()
		self.height = self.winfo_screenheight()
		self.geometry(f"{self.width}x{self.height}")

		# Attribute to keep track of the current page
		self.currentPage = None
		self.loggedInUser = None

		# Connect to database
		self.conn = sqlite3.connect("assets/PyProject.db")
		self.cursor = self.conn.cursor()
		
		# Call function to create navbar
		self.navBar = NavigationBar(self, self.openPage)
		self.navBar.pack(fill="x", side="top")		

		footer = Footer(self)
		footer.pack(side="bottom", fill="x")

		# Open the page you want, probably the home page, which would be the ai story, which is a good 
		# candidate for being the homePage

	def loadPage(self, pageName):
		try:
			module = importlib.import_module(f"pages.{pageName}")
			pageClass = getattr(module, pageName)
			return pageClass		
		except (ImportError, AttributeError):
			print(f"Error: Page {pageName} wasn't found.")
			return None
		
	def openPage(self, pageName, *args):
		pageClass = self.loadPage(pageName)
		if pageClass is None:
			return
		if self.currentPage:
			self.currentPage.destroy()
		self.currentPage = pageClass(self, *args)
		self.currentPage.pack(fill="both", expand=True)

if __name__ == "__main__":
	app = App()
	app.mainloop()