from apiutils.configs.summarizer import USE_MODEL
if USE_MODEL:
    from apiutils.model.ChatBerta import ChatBerta

from apiutils.functions.apifuncs import random_summarizer


# Network Component that bridges gap between model and chat package format
class NetworkComponent:
    def __init__(self):
        pass

    # runs the summarization and returns the chat_package, and any other metrics
    def summarize(chat_package, summary_options):
        if not USE_MODEL:
            # just use the random summarizer
            return 0, random_summarizer( chat_package, fraction=0.25 )

        # call ChatBerta and do summary
        try:
            model = ChatBerta()

            chosen_message_ids, summary = model.summarize(
                messages = chat_package['messages'],
                summary_options = summary_options
            )

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



    