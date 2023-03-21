from apiutils.model.ChatBerta import ChatBerta
import random


# random summarizer used instead
class RandomSummarizer():
    def __init__(self):
        pass

    def summarize(self, messages=[], summary_options={}, fraction: float = 0.25 ):
        # takes a chat package and selects random messages to be in the summary

        # including 10% of messages as summary
        num_msgs = len(messages)
        num_summary_msgs = round(num_msgs * fraction)
        summary_msg_ids = random.sample(range(0, num_msgs ), num_summary_msgs)

        summary_paragaph = '\n'.join([ messages[id]['text'] for id in summary_msg_ids ])

        return summary_msg_ids, summary_paragaph



# Network Component that bridges gap between model and chat package format
class NetworkComponent:
    def __init__(self, use_model, propagate_errors=False):
        self.use_model = use_model
        self.propagate_errors = propagate_errors
        self.model = self.get_actual_model() if self.use_model else RandomSummarizer()

    def get_actual_model(self):
        # gets the actual chat berta model
        if self.propagate_errors:
            return ChatBerta()
        
        else:
            try:
                return ChatBerta()
            except:
                # if module loading or importation failed, keep web API up and just set model to None
                return None

    def use_model(self, use_model:bool):
        # figure out if we need to reset model
        if (not self.use_model) == use_model:
            # if they are opposites we know we have to instantiate a new model
            self.model = self.get_actual_model() if use_model else RandomSummarizer()

        # set the model usage
        self.use_model = use_model

    # runs the summarization and returns the chat_package, and any other metrics
    def summarize(self, chat_package, summary_options):
        # call ChatBerta and do summary

        if self.model is None:
                # if no model and we are meant to use it return -1
                return -1, None

        if self.propagate_errors:
            # do without try catch to propagate exception upwards
            chosen_message_ids, summary = self.model.summarize(
                    messages = chat_package['messages'],
                    summary_options = summary_options
                )

            # combine into a paragraph
            summary = (' '.join(summary.split('\n'))).strip()
        
        else:
            try:

                chosen_message_ids, summary = self.model.summarize(
                    messages = chat_package['messages'],
                    summary_options = summary_options
                )

                # combine into a paragraph
                summary = (' '.join(summary.split('\n'))).strip()

            except:
                # it failed for some reason, return -1 and no chat package
                # tells API to return with server error
                return -1, None
        
        # remove duplicate message ids
        chosen_message_ids = list(dict.fromkeys(chosen_message_ids))

        # then use the message ids to populate the summary chat package
        summary_chat_package = dict(chat_package)

        summary_chat_package['summary'] = {
            'paragraph' : summary,
            'message_ids': chosen_message_ids
        }

        return 0, summary_chat_package



    