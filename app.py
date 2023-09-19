from ai import ModelBase, StoryGPT # <----- template model for later use
# from gui import UI
from textwrap import dedent

########################################################################
#                             AI                                       #
########################################################################

systemPrompt = "You are a masterful storyteller and author who can write captivating and fantastic stories on a whim."
prompt = 'Write a story about a man who programs SkyNet in three days'

def test_run(model: StoryGPT):
    '''
    This function demonstrates in a simple way the use of the base model class to get AI output.
    All results are returned in a generator, so they need to be iterated over to get the results.

    :PARAMS:
        `model` - The AI model to get responses from. Can be a base model or a refined model.
    '''
    mode = input("""
        
        Choose a mode: 
            Start a new story (new): Create a new story
            Start a new remix (remix): Create a new remix
            Stop: Close the application

        Story Mode > """) # Primer input
    
    mode = mode.lower() # convert all the test to lowercase

    while mode != "stop": # loop until the user types "stop"
        if mode == "new": # if the mode is a new story
            topic = input("Please enter the topic of your story > ") # get the topic of the story
            
            while True:
                try:
                    length = int(input("Please enter the length of your story in words using integers > "))
                except:
                    print('Please enter only integers')
                    continue

                if length < 0:
                    print('A story cannot have negative words, please reenter your length in positive integers only')
                    continue
                break
            
            style = input("Please enter the style of the story > ")

            response = model.sendStoryPrompt(topic, length, style)

        elif mode == "remix": # if the mode is remix
            story = input("Please enter the story you would like to remix > ")

            style = input("Please enter the style the story is written in (optional) > ")

            response = model.sendRemixPrompt(story, style)

        else: # input validation
            print("Please choose a valid option \n")

            mode = input("""
        
                Choose a mode: 
                    Start a new story (new): Create a new story
                    Start a new remix (remix): Create a new remix
                    Stop: Close the application

                Story Mode > """)
            mode = mode.lower()
            continue # skip over the rest of the code and restart the loop

        print('\n\n')

        # Print the response generation in real-time
        for chunk in response:
            # end has to equal an empty string to stop the print statement from printing every chunk on a new line
            # flush has to equal True so that the print statement can print the characters in real time
            print(chunk, end='', flush=True)

        # take input again and make it lowercase
        mode = input("""
        
            Choose a mode: 
                Start a new story (new): Create a new story
                Start a new remix (remix): Create a new remix
                Stop: Close the application

            Story Mode > """)
        mode = mode.lower()

########################################################################
#                            GUI                                       #
########################################################################



########################################################################
#                          DATABASE                                    #
########################################################################



########################################################################
#                              MAIN                                    #
########################################################################
def main():
    storyGPT = StoryGPT()
    # storyGPT = ModelBase('gpt-3.5-turbo', prompt, systemPrompt)

    test_run(storyGPT)

if __name__ == "__main__":
    main()