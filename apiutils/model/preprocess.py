
def preprocess_single_dialogue(dialogue):
    #print(dialogue)
    messages = dialogue.split('\n')
    #print(messages)
    party_to_id = {}
    message_id = 0
    # Dictionary to store preprocessed dialogue
    preprocessed_dialogue = []
    
    for message in messages:
        split_message = message.split(': ')
        party = split_message[0].strip()
        text = split_message[1].strip()
        if party not in party_to_id:
            party_to_id[party] = len(party_to_id)
        pid = party_to_id[party]

        preprocessed_dialogue.append({'id': message_id, 'pid': pid, 'text': text})
        message_id += 1

    messages = {
        "messages": preprocessed_dialogue
    }
    return messages['messages']

def preprocess_dialogues(dataset):
    dialogues = dataset["dialogue"]
    preprocessed_dialogues = []
    
    for dialogue in dialogues:
        preprocessed_dialogues.append(preprocess_single_dialogue(dialogue))
    
    return preprocessed_dialogues
