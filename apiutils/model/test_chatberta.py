import sys
from apiutils.model.ChatBerta import ChatBerta

def main():
    messages = {
            "messages": [
            {
                "id": 0,
                "pid": 0,
                "text": "Apples are my favourite fruit, what are yours?"
            },
            {
                "id": 1,
                "pid": 1,
                "text": "I like oranges better, apples be gross sometimes"
            },
            {
                "id": 2,
                "pid": 0,
                "text": "Oh really? I think apples are superior."
            },
            {
                "id": 3,
                "pid": 1,
                "text": "Interesting."
            },
            {
                "id": 4,
                "pid": 0,
                "text": "Why do you think oranges are better than apples?"
            },
            {
                "id": 5,
                "pid": 1,
                "text": "I think oranges are sweeter and juicier than apples."
            },
            {
                "id": 6,
                "pid": 0,
                "text": "But apples have a wider variety of flavors and textures."
            },
            {
                "id": 7,
                "pid": 1,
                "text": "I guess that's true, but I just prefer oranges."
            },
            {
                "id": 8,
                "pid": 0,
                "text": "Have you ever tried a Honeycrisp apple? They're amazing."
            },
            {
                "id": 9,
                "pid": 1,
                "text": "No, I haven't. I'll have to try one sometime."
            },
            {
                "id": 10,
                "pid": 0,
                "text": "Definitely do. They're the perfect combination of sweet and tart."
            },
            {
                "id": 11,
                "pid": 1,
                "text": "I'll keep that in mind. Thanks for the recommendation."
            }
        ]
    }

    messages = messages["messages"]

    summary_options = {
        "basic_options": [],
        "summarize_only_for": -1 
    }

    chat_berta = ChatBerta()
    chosen_message_ids, summary = chat_berta.summarize(messages=messages, summary_options = summary_options)

    print(summary)
    print(chosen_message_ids)

    return 0

if __name__ == '__main__':
    sys.exit(main())