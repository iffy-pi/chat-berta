import json
# network component with the expected classes
# contains
class NetworkComponent:
    def __init__(self):
        self.parties=[]
        self.messages=[]
    def json_packet_to_summarizer(self, json_packet):
        
        # Load JSON data to be stored
        data = json.loads(json_packet)
        # Store packet values
        for party in data['config']['parties']:
            self.parties.append({'id': party['id'], 'name': party['name']})
        for message in data['messages']:
            self.messages.append({'id': message['id'], 'pid': message['pid'], 'text': message['text']})

    def generate_summary(self, json_packet):
        self.json_packet_to_summarizer(json_packet)
        # TODO: link output ids to summarizer NN output
        self.output_ids = self.messages[0]['id']
        self.create_json_packet()

    def create_json_packet(self):
        # Create a packet containing the input/output string pair
        packet = {
            'config': {'parties': self.parties},
            'messages': self.messages,
            'output_messages': list(filter(lambda x: x['id'] == self.output_ids, self.messages))
        }

        self.json = json.dumps(packet)
