import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re

def parse_chatlog_xml(xml_str:str):
    xmlroot = ET.fromstring(xml_str)

    # parse the conversation parties from the config
    config_root = xmlroot.find('config')
    if config_root is None:
        raise Exception('No chatlog config found!')

    parties_root = config_root.find('parties')
    if parties_root is None:
        raise Exception('No chat parties found!')

    parties = {}
    for party in parties_root.findall('party'):
        party_id = party.attrib.get('id')
        if party_id is None:
            raise Exception('No party id included!')
        
        # populate our parties dictionary
        parties[party_id] = party.text
    
    # print the messages
    msgs_root = xmlroot.find('messages')
    if msgs_root is None: raise Exception('No messages found!')

    for message in msgs_root.findall('message'):
        pid = message.attrib['pid']
        print('{}:'.format(parties[pid]))
        print(message.text)

def create_chatlog_xml(raw_chatstr:str):
    # creates the chatlog xml
    root = ET.Element("chatlog")
    config_root = ET.SubElement(root, "config")
    msgs_root = ET.SubElement(root, "messages")

    lines = raw_chatstr.split('\n')

    parties = []
    current_party_id = None
    message_id = 0
    for line in lines:
        # is a party indicator line
        if re.match('^[a-zA-z][a-zA-z]*:', line):
            # get the party
            party = line.replace(':', '')
            if party not in parties:
                parties.append(party)
                current_party_id = len(parties)-1
            else:
                current_party_id = parties.index(party)
            continue

        if current_party_id is None:
            raise Exception('No chat party found!')

        if line.strip() == '':
            continue

        # is a regular line, so add to the messages
        msg = ET.SubElement(msgs_root, "message")
        msg.set('pid', str(current_party_id))
        msg.set('id', str(message_id))
        msg.text = line.strip()
        
        message_id += 1

    # handle the parties in the config section
    parties_tag = ET.SubElement(config_root, "parties")
    for i,p in enumerate(parties):
        ptag = ET.SubElement(parties_tag, "party")
        ptag.set('id', str(i))
        ptag.text = p

    return prettify_xml(root)

def prettify_xml(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def main():
    sample_xml_chat = os.path.join( os.path.split(__name__)[0], 'sample_chatlog.xml' )
    sample_raw_chat = os.path.join( os.path.split(__name__)[0], 'sample_raw_chat.txt' )

    opt = 1

    if opt == 0:
        with open(sample_xml_chat, 'r') as file:
            content = file.read()
        parse_chatlog_xml(content)

    else:
        with open(sample_raw_chat, 'r') as f: content = f.read()

        create_chatlog_xml(content)

    

    return 0

if __name__ == '__main__':
    sys.exit(main())