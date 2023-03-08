# network component with the expected classes
# contains
class NetworkComponent:
    def __init__(self):
        self.chat_package = {}
        self.summarizer_options = {}

    # loads the nc with the chat package and summarizer options
    def load(self, chat_package, summarizer_options):
        self.chat_package = chat_package
        self.summarizer_options = summarizer_options

    # runs the summarization and returns the chat_package, and any other metrics
    def summarize(self):
        # check summmarize_only_for_field and filter out messages that arent the party id

        # convert message JSON objects into whatever format the model needs
        # HAILING TODO: How does the model receive input? You will need to track an id for every sentence the model takes in

        # convert model ouput into the summary messages format, will need the model output to have 
        # the message ids so that we can map the party info
        # HAILING TODO: Give model outputs and we need the message ids

        # complete the chat package by adding summary chat messages field

        # return along with metrics
        pass



    