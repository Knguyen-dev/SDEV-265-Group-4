from classes.utilities import convertStoryObjToJSON
import customtkinter as ctk
import sys
from classes.export import StoryPDF
from tkinter.filedialog import askdirectory
import os

sys.path.append("..")

'''
+ storyLibraryPage: Frame that represents the page wherre the user can see all of their saved stories.
	From here, the user will be able to select a story that they want to continue, remix a story, or delete a story.

Constructor:
- master: 'App' class instance from 'Main.py'

Attributes/Variables:
- master: 'App' class instance from 'Main.py'
- innerPageFrame (CTkFrame): Frame that contains all of the page's widgets
- savedStories (Array): An array of story objects.
- rowIndex (int): Indexes for structuring the grid of story cards
- columnIndex (int): Indexes for structuring the grid of story cards
- storyCard (CTkFrame): A container that displays the story's information and the buttons that the user is able to use
	to interact wtih that saved story
- cardHeader (CTkFrame): Header of the card
- cardTitle (CTkLabel): Title label of the card
- cardBody (CTkFrame): Body of the card
- continueSavedStoryBtn (CTkButton): Button that lets user to continue a saved story and opens AIChatPage
- openRemixStoryBtn (CTkButton): Button that lets user remix a saved story, and opens remixStoryPage
- deleteSavedStoryBtn (CTkButton): Button that deletes a story


Methods:
- continueSavedStory(self, story): Lets a user continue a story and redirects them to the AIChatPage
- deleteSavedStory(self, story): Deletes a saved story from the database.
'''


class storyLibraryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#EBEBEB")
        self.master = master
        innerPageFrame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", width=625, height=500)
        innerPageFrame.pack(expand=True)

        # Get the saved stories, from the logged in user, if there are any
        savedStories = self.master.loggedInUser.stories

        # If there aren't any stories saved, then just show a message, and stop it early
        if not savedStories:
            label = ctk.CTkLabel(
                innerPageFrame, text="No stories have been saved yet!", font=("Helvetica", 24))
            label.pack()
            return

        rowIndex = 0
        columnIndex = 0
        # iteratively create 'cards' or containers that display their information
        for story in savedStories:
            storyCard = ctk.CTkFrame(
                innerPageFrame, fg_color="#CFCFCF", width=200)

            # if true, then columnIndex story cards have already been placed, so reset
            # the column index, and move on to a new row
            if (columnIndex == 3):
                columnIndex = 0
                rowIndex += 1

            cardHeader = ctk.CTkFrame(storyCard)
            cardTitle = ctk.CTkLabel(cardHeader, fg_color="#BABABA", text_color="black",
                                     text=f"Title: {story.storyTitle}", wraplength=200)
            cardBody = ctk.CTkFrame(storyCard, fg_color="transparent")
            continueSavedStoryBtn = ctk.CTkButton(cardBody, text="Continue", text_color="white", fg_color="#0E4732",
                                                  hover_color="#3A6152", command=lambda story=story: self.continueSavedStory(story))
            openRemixStoryBtn = ctk.CTkButton(cardBody, text="Remix", text_color="white", fg_color="#0E4732", hover_color="#3A6152",
                                              command=lambda story=story: self.master.openPage("remixStoryPage", story))  # type: ignore
            deleteSavedStoryBtn = ctk.CTkButton(cardBody, text="Delete", text_color="white", fg_color="#0E4732",
                                                hover_color="#3A6152", command=lambda story=story: self.deleteSavedStory(story))
            exportStoryBtn = ctk.CTkButton(
                cardBody, text="Export", command=lambda story=story: self.exportSavedStory(story), text_color="white", fg_color="#0E4732", hover_color="#3A6152")

            # Structure the storyCard and its widgets
            storyCard.grid(row=rowIndex, column=columnIndex, padx=10, pady=10)
            cardHeader.grid(row=0, column=0, pady=10)
            cardTitle.grid(row=0, column=0)
            cardBody.grid(row=1, column=0)
            continueSavedStoryBtn.grid(row=0, column=0, pady=5)
            openRemixStoryBtn.grid(row=1, column=0, pady=5)
            exportStoryBtn.grid(row=2, column=0, pady=5)
            deleteSavedStoryBtn.grid(row=3, column=0, pady=5)
            columnIndex += 1

    def continueSavedStory(self, story):
        '''
        - Let the user continue a saved story and takes them to the AIChatPage
        '''
        # Update the currentStory that we are currently continuing
        # And set booleans to indicate that currentStory is a saved story, rather than a story we're remixing from
        self.master.currentStory = story  # type: ignore
        self.master.isSavedStory = True  # type: ignore
        self.master.isRemixedStory = False  # type: ignore

        # Convert story into openai json format
        storyJSON = convertStoryObjToJSON(story)

        # Set AI's knowledge to the selected story's messages and info
        self.master.storyGPT.populate(storyJSON)  # type: ignore

        # Reset unsaved messages since we are continuing a story (starting a new chat), and we don't want old messages
        self.master.unsavedStoryMessages = []  # type: ignore

        # Redirect user to the ai chat page
        self.master.openPage("AIChatPage")  # type: ignore

    def deleteSavedStory(self, story):
        '''
        - Deletes a story from the user's library
        - If currentStory == story, there are two cases:
        1. The story that the user is deleting is the same saved story that they are continuing
        2. The story that the user is deleting, is the story that they are currently remixing off of.

        - Else, currentStory != story, so they're deleting a story that's unrelated 
        to the story that they're current writing/continuing 
        '''
        if self.master.currentStory == story:  # type: ignore
            # Reset currentStory since it's being deleted from database
            self.master.currentStory = None  # type: ignore

            # Clear the AI's knowledge of the current story, since that's what we're deleting
            self.master.storyGPT.clear()  # type: ignore

            # Reset unsaved messages since they're apart of the story that's being deleted
            self.master.unsavedStoryMessages = []  # type: ignore

            # 1
            if self.master.isSavedStory:  # type: ignore
                self.master.isSavedStory = False  # type: ignore
            elif self.master.isRemixedStory:  # type: ignore
                # 2
                self.master.isRemixedStory = False  # type: ignore

        # Delete story from database
        self.master.session.delete(story)  # type: ignore
        self.master.session.commit()  # type: ignore

        # Open/reload the storyLibraryPage for changes to take effect
        self.master.openPage("storyLibraryPage")  # type: ignore

    def continueSavedStory(self, story):
        '''
        - Let the user continue a saved story and takes them to the AIChatPage
        '''
        # Update the currentStory that we are currently continuing
        # And set booleans to indicate that currentStory is a saved story, rather than a story we're remixing from
        self.master.currentStory = story  # type: ignore
        self.master.isSavedStory = True  # type: ignore
        self.master.isRemixedStory = False  # type: ignore

        # Convert story into openai json format
        storyJSON = convertStoryObjToJSON(story)

        # Set AI's knowledge to the selected story's messages and info
        self.master.storyGPT.populate(storyJSON)  # type: ignore

        # Reset unsaved messages since we are continuing a story (starting a new chat), and we don't want old messages
        self.master.unsavedStoryMessages = []  # type: ignore

        # Redirect user to the ai chat page
        self.master.openPage("AIChatPage")  # type: ignore

    def deleteSavedStory(self, story):
        '''
        - Deletes a story from the user's library
        - If currentStory == story, there are two cases:
        1. The story that the user is deleting is the same saved story that they are continuing
        2. The story that the user is deleting, is the story that they are currently remixing off of.

        - Else, currentStory != story, so they're deleting a story that's unrelated 
        to the story that they're current writing/continuing 
        '''
        if self.master.currentStory == story:  # type: ignore
            # Reset currentStory since it's being deleted from database
            self.master.currentStory = None  # type: ignore

            # Clear the AI's knowledge of the current story, since that's what we're deleting
            self.master.storyGPT.clear()  # type: ignore

            # Reset unsaved messages since they're apart of the story that's being deleted
            self.master.unsavedStoryMessages = []  # type: ignore

            # 1
            if self.master.isSavedStory:  # type: ignore
                self.master.isSavedStory = False  # type: ignore
            elif self.master.isRemixedStory:  # type: ignore
                # 2
                self.master.isRemixedStory = False  # type: ignore

        # Delete story from database
        self.master.session.delete(story)  # type: ignore
        self.master.session.commit()  # type: ignore

        # Open/reload the storyLibraryPage for changes to take effect
        self.master.openPage("storyLibraryPage")  # type: ignore

    def exportSavedStory(self, story):
        pdf = StoryPDF(story_name=story.storyTitle)
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        for idx, message in enumerate(story.messages):
            if idx == 0:
                # Prompt
                pdf.multi_cell(200, 20, str("Prompt: " + message.text), 0, 1)
            else:
                # Story
                pdf.multi_cell(80, 5, str(message.text), 0, 1)
        save_dir = askdirectory()
        if save_dir != ():
            file_path = os.path.join(save_dir, story.storyTitle+".pdf")
            pdf.output(file_path, 'F')
