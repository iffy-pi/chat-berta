import os
import sys
import xml.etree.ElementTree as ET


def parse_chatlog_xml(xml_str:str):
    xmlroot = ET.fromstring(xml_str)

    # parse the conversation parties from the config
    config_root = xmlroot.findall('config')
    
    if len(config_root) < 1:
        raise Exception('No chatlog config found!')

    config_root = config_root[0]

    parties = {}
    for party in config_root.findall('party'):
        party_id = party.attrib.get('id')
        if party_id is None:
            raise Exception('No party id included!')
        
        # populate our parties dictionary
        parties[party_id] = party.text
    
    # print the messages
    msgs_root = xmlroot.findall('messages')
    if len(msgs_root) < 1: raise Exception('No messages found!')
    msgs_root = msgs_root[0]

    for message in msgs_root.findall('message'):
        pid = message.attrib['pid']
        print('{}:'.format(parties[pid]))
        print(message.text)

def main():
    sample_chat = os.path.join( os.path.split(__name__)[0], '..', 'server-void', 'fec-proto', 'sample_chatlog.xml' )
    
    with open(sample_chat, 'r') as file:
        content = file.read()
    
    
    parse_chatlog_xml(content)

    return 0

if __name__ == '__main__':
    sys.exit(main())