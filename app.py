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
    model.setStoryMode("Write a story about society in the year 2050. It's the turn of the decade, and AI technology has grown beyond mere chatbots and image generators. For the first time ever, they have now been implemented sucessfully into humanoid robots. In the story, talk about the challenges to the builders and programmers, talk about the benefits they brought to that society in 2050, and talk about the average person's fears of them. Do not make this an informational piece or a documentary non-fiction. Make this a captivating fiction story book in first person following Jake, an AI programmer for the robots.", 2500, "J.R.R. Tolkien")

    result = model.complete(stream=True)

    for chunk in result:
        print(chunk, flush=True, end='')

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
    storyGPT = StoryGPT('gpt-3.5-turbo', systemPrompt)
    # storyGPT = ModelBase('gpt-3.5-turbo', prompt, systemPrompt)

    test_run(storyGPT)

if __name__ == "__main__":
    main()