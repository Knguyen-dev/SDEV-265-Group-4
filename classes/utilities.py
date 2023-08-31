# Accepts list of entry widgets and clears their input
from tkinter import *
import customtkinter as ctk

## Clears entry widgets of any input
def clearEntryWidgets(entryWidgets):
    for entry in entryWidgets:
        entry.delete(0, END)




## Toggles whether or not an entry widget's input is hidden, accepts a checkbox
# Useful for hiding password input field and whatnot
def toggleHidden(entryWidget, checkVar):
	# If it's checked, user wants to hide password
	if checkVar.get() == "on":
		entryWidget.configure(show="*")
	else:
		entryWidget.configure(show="")

## strips the input of entry widget of trailing or leading whitespace
def stripEntryWidgets(entryWidgets):
	strippedWidgets = []
	for entry in entryWidgets:
		inputValue = entry.get().strip()
		entry.delete(0, END)
		entry.insert(0, inputValue)
		strippedWidgets.append(entry)
	return strippedWidgets

## Checks if any one of the entry widgets in the list entryWidgets has no input
def isEmptyEntryWidgets(entryWidgets):
	for entry in entryWidgets:
		if entry.get() == "":
			return True
	return False