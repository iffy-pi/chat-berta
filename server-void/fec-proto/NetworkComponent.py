import json
import socket
# network component with the expected classes
# contains
class NetworkComponent:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def json_packet_rx(self):

        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        s.bind((self.host, self.port))

        # Listen for an incoming connection
        s.listen(1)

        # Wait for a connection
        connection, address = s.accept()

        # Receive the transmitted data (1024 bytes is a baseline maximum size)
        # TODO: determine maximum expected data buffer size.
        data = connection.recv(1024)
        if data:
            # Load the JSON packet
            self.json_packet = json.loads(data)

        # Store packet values
        self.summ_type = self.json_packet.get('type')
        self.summ_degree = self.json_packet.get('summarization_degree')
        self.input = self.json_packet.get('input')

    def generate_summary(self):
        # TODO: link output to summarizer NN output
        self.output = ''

    def create_json_packet(self):
        # Create a packet containing the input/output string pair
        packet = {
            'type': self.summ_type,
            'summarization_degree': self.summ_degree,
            'input': self.input,
            'output': self.output
        }

        self.json_packet = json.dumps(packet)

    def json_packet_tx(self):
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        s.connect((self.host, self.port))

        # Send the packet
        s.sendall(self.json_packet)

        # Close the connection
        s.close()
