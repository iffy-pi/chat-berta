import random


# random summarizer used instead
class RandomSummarizer2():
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
class SimpleNetworkComponent:
    def __init__(self, propagate_errors=False):
        self.propagate_errors = propagate_errors
        self.model = RandomSummarizer2()

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



    