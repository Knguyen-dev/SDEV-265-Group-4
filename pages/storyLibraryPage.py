from classes.utilities import convertStoryObjToJSON
import customtkinter as ctk
import sys, os
from classes.export import StoryPDF
from tkinter.filedialog import asksaveasfilename
import zipfile
from PIL import Image 
from tkinter import messagebox

sys.path.append("..")

'''
+ storyLibraryPage: Frame that represents the page wherre the user can see all of their saved stories.
	From here, the user will be able to select a story that they want to continue, remix a story, or delete a story.

Constructor:
- master: 'App' class instance from 'Main.py'

Attributes/Variables:
- master: 'App' class instance from 'Main.py'
- innerPageFrame: (CTKFrame): Frame that contains all widgets
- storiesContainer (CTkFrame): Frame that contains all of the story cards 
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

- Methods:
- continueSavedStory(self, story): Lets a user continue a story and redirects them to the AIChatPage
- deleteSavedStory(self, story): Deletes a saved story from the database.
'''


class storyLibraryPage(ctk.CTkFrame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master, fg_color=self.master.theme["main_clr"], corner_radius=0)

        innerPageFrame = ctk.CTkFrame(self, fg_color="transparent")
        innerPageFrame.pack(expand=True)

        '''
        1. If there aren't any stories saved for this user, then just show a message, and stop it early
        2. Else, the user has stories to save, so render appropriate markup and GUI components 
        '''
        if not self.master.loggedInUser.stories:
            label = ctk.CTkLabel(
                innerPageFrame, text="No stories have been saved yet!", font=("Helvetica", 24), text_color=self.master.theme["label_clr"])
            label.grid(row=0, column=0)
            return
        
        # Render section for exporting all stories in the library
        bulkExportBtnFrame = ctk.CTkFrame(innerPageFrame, fg_color="transparent", width=500, height=500)
        bulkExportStoryBtn_image = ctk.CTkImage(Image.open(os.path.join(self.master.image_path, 'glass_bulk_export_btn.png')),
				size=(75, 75))
        bulkExportStoryBtn = ctk.CTkButton(bulkExportBtnFrame, image=bulkExportStoryBtn_image, text="Export all to .zip ", height=10, width=5, command=self.exportAllStories, text_color=self.master.theme["btn_text_clr"], fg_color='transparent', hover_color=self.master.theme["hover_clr"])
        bulkExportStoryBtn.pack(expand=True)
        bulkExportBtnFrame.grid(row=0, column=0)

        # Container/section where all story cards appear.
        storiesContainer = ctk.CTkScrollableFrame(innerPageFrame, fg_color="transparent", width=625, height=500)
        storiesContainer.grid(row=1, column=0)

        # Iteratively create 'cards' or containers that display their information
        rowIndex = 0
        columnIndex = 0
        for story in self.master.loggedInUser.stories:
            storyCard = ctk.CTkFrame(
                storiesContainer, fg_color=self.master.theme["sub_clr"])

            # if true, then columnIndex story cards have already been placed, so reset
            # the column index, and move on to a new row
            if (columnIndex == 3):
                columnIndex = 0
                rowIndex += 1

            cardHeader = ctk.CTkFrame(storyCard, fg_color="transparent")
            cardTitle = ctk.CTkLabel(cardHeader, text_color=self.master.theme["label_clr"],
                                     text=f"Title: {story.storyTitle}", wraplength=200)
            cardBody = ctk.CTkFrame(storyCard, fg_color="transparent")
            continueSavedStoryBtn = ctk.CTkButton(cardBody, text="Continue", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"],
                                                  hover_color=self.master.theme["hover_clr"], command=lambda story=story: self.continueSavedStory(story))
            openRemixStoryBtn = ctk.CTkButton(cardBody,  text="Remix", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"],
                                              command=lambda story=story: self.openRemixStoryPage(story))  # type: ignore
            deleteSavedStoryBtn = ctk.CTkButton(cardBody,  text="Delete", text_color=self.master.theme["btn_text_clr"], fg_color=self.master.theme["btn_clr"],
                                                hover_color=self.master.theme["hover_clr"], command=lambda story=story: self.deleteSavedStory(story))
            exportStoryBtn_image = ctk.CTkImage(Image.open(os.path.join(self.master.image_path, 'glass_single_export_btn.png')),
				size=(50, 50))
            exportStoryBtn = ctk.CTkButton(cardBody, image=exportStoryBtn_image, text="Export", height=10, width=5, command=lambda story=story: self.exportSavedStory(story), text_color=self.master.theme["btn_text_clr"], fg_color='transparent', hover_color=self.master.theme["hover_clr"])

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

    def openRemixStoryPage(self, story):
        '''
        Prepares the application for remixing a story and also redirects
        the user to the remix story page

        1. Set remixStoryObj so that application remembers what story they were trying to remix.
            In case the user wants to toggle the theme on the remixStoryPage, which reloads the page,
            we'll be able to remember the story they were selecting whilst maintaining the theme toggling functionality.

        2. Then open the remixStoryPage

        NOTE: remixStoryPage can only be accessed by clicking the openRemixStoryBtn,
            which will always reassign remixStoryObj to a valid/existing remixStoryObj.
            Meaning, there should be no need to clear remixStoryObj when deleting stories, accounts, etc. as
            remixStoryObj will always be assigned to a valid value when it matters.
        '''
        self.master.remixStoryObj = story
        self.master.openPage("remixStoryPage")

    def continueSavedStory(self, story):
        '''
        + Let the user continue a saved story and takes them to the AIChatPage
        1.
        - Update the currentStory that we are currently continuing
        - And set booleans to indicate that currentStory is a saved story, rather than a story we're remixing from 
        2.
        - Convert story into openai json format
        - Set AI's knowledge to the selected story's messages and info
        - Reset unsaved messages since we are continuing a story (starting a new chat), and we don't want old messages
        - Redirect user to the ai chat page
        '''
        # 1
        self.master.currentStory = story  # type: ignore
        self.master.isSavedStory = True  # type: ignore
        self.master.isRemixedStory = False  # type: ignore
        # 2        
        storyJSON = convertStoryObjToJSON(story)
        self.master.storyGPT.populate(storyJSON)  # type: ignore
        self.master.unsavedStoryMessages = []  # type: ignore
        self.master.openPage("AIChatPage")  # type: ignore



    def deleteSavedStory(self, story):
        '''
        + Deletes a story from the user's library
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


    def getStoryPDF(self, story):
        '''
        + Converts a story object into a pdf
        '''
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
        return pdf
    
    def exportSavedStory(self, story):
        '''
        + Prompts user to save a singular story as a pdf. 
        1. Convert story into a pdf object
        2. Prompt the user for the path where they want to save their file, and prompt for the name of the file.
        3. If filePath exists/is valid, then download pdf to that file path.
        '''
        pdf = self.getStoryPDF(story)
        savePath = asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"{pdf.story_name}",
            filetypes=[("Pdf Files", "*.pdf"), 
                       ("All files", "*.*")]
        )
        if savePath:
            pdf.output(savePath, 'F')

    def exportAllStories(self):
        '''
        + Prompts user to save all of the pdfs in their library into a single zip file.
        1. If user doesn't have any stories, then abort function early
        2. Convert all saved story objects into pdf objects.
        3. Prompt for a file path and file name for where they want the zip file to be.
        4. If path for zip file is valid, create zip file and write all pdf data into that file.
            Finally, download the file to the user's entered path.
        '''
        # Msgbox pop-up to reassure our user that their story is exporting
        messagebox.showinfo('Export Loading', f'Please wait your stories are loading...') 
        if not self.master.loggedInUser.stories:
            return
        all_stories_pdfs = []
        for story in self.master.loggedInUser.stories:
            pdf = self.getStoryPDF(story)
            all_stories_pdfs.append(pdf)
        zipPath = asksaveasfilename(
            defaultextension=".zip",
            initialfile="BookSmartBulkExport",
            filetypes=[("Zip files", "*.zip"), ("All files", "*.*")]
        )
        if zipPath:
            with zipfile.ZipFile(zipPath, mode="w") as bulk_export:
                for pdf_story_file in all_stories_pdfs:
                    bulk_export.writestr(
                        zinfo_or_arcname=pdf_story_file.story_name+".pdf", 
                        data=pdf_story_file.output(dest="S").encode('latin-1')
                    )