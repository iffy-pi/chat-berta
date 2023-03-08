The messages from the frontend are packaged in the following format in JSON:

```json
"messages": [
        {
            "id": 0,
            "pid": 0,
            "text": "Apples are my favourite fruit, what are yours?"
        },
        {
            "id": 1,
            "pid": 1,
            "text": "I like oranges better, apples be gross sometime"
        },
        {
            "id": 2,
            "pid": 0,
            "text": "Oh really, I think apples are superior"
        },
        {
            "id": 3,
            "pid": 1,
            "text": "Interesting"
        }
    ]
```

The message fields are as follows:
- The `id` is a unique ID assigned to each message in the transcript, which we can call the message ID
- The `pid` is the party ID, and is the party ID of the party that sent the message
	- This is what you can use to identify the speaking turn
- The text is the actual text of the message. This can include multiple sentences.

The party ID is mapped to parties in the config section of the chat package as shown below:

```json
"config": {
        "parties": [
           {
                "id": 0,
                "name": "John"
            },
            {
                "id": 1,
                "name": "Jane"
            }
        ]
    }
```

However, you will not require access to this information as you can do integer comparisons for the speaking turns.

The Network Component can automatically parse the chat package to provide the list of messages in the format of a python dictionary e.g. `message['id'], message['pid'] etc`. 

**You will need to track the message ID of the sentences that are included in the summary, this will be required by the network component to create the summary chat package**.

As for the monologue option, this is included in the `summarizer_options` object in the Network Component as a field:

```json
"summary_options": {
        "basic_options": [],
        "summarize_only_for": -1 // -1 for no party, otherwise set to the party id for what we would like to summarize
    }
```

The value of `summarize_only_for` is the party ID of the person who we are summarizing only for. 

There are two ways to handle this:
- At the NC level: The network component filters out all the messages by the different party, and then just sets a `monologue` flag or something when calling the model
- At hte model level: I pass you the summarizer_options object and you can handle it as you wish.

**The model output should be:**
- The generated summary paragraph (if it is available)
- The message IDs of the sentences that were included in the summary

