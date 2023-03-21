import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import json

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

def create_chatlog_json(raw_chatstr:str, indent=None):
    # doing the chat parsing but for json
    lines = raw_chatstr.split('\n')
    parties = []
    cur_party_id = None
    messages = []

    for line in lines:
        if re.match('^[a-zA-z][a-zA-z]*:', line):
            # pull the party name from the line
            party = line.replace(':', '')
            if party not in parties:
                parties.append(party)
                cur_party_id = len(parties)-1
            else:
                cur_party_id = parties.index(party)

            continue

        if cur_party_id is None:
            raise Exception('No chat party found!')

        # parse the current line
        if line.strip() == '': continue

        # read the current line
        messages.append({
            'id': len(messages), 
            'pid': cur_party_id,
            'text': line.strip()
        })

    config = {
        'parties': []
    }

    # populate parties information in config
    for party_id, party in enumerate(parties):
        config['parties'].append({
            'id': party_id,
            'name': party
        })

    # make our JSON
    chatlog = {
        'config': config,
        'messages': messages
    }

    return json.dumps(chatlog, indent=indent)

def parse_chatlog_json( chatlog_json_str: str):
    # parses a created chatlog json
    chatlog = json.loads(chatlog_json_str)

    cur_party_id = None
    print_separator = False

    # print messages in transcript format
    for message in chatlog['messages']:
        if cur_party_id != message['pid']:
            # only print the space separator if there was a party before
            print_separator = ( cur_party_id is not None)
            cur_party_id = message['pid']
            # print the associated party for the message first
            # parties objects are ordered by id, so we can just index with the message pid
            if print_separator: print()
            print('{}:'.format( chatlog['config']['parties'][cur_party_id]['name'] ))


        # then print the associted message
        print(message['text'])
    
    # group the messages for each party into paragraphs
    prv_paragraph = None
    cur_paragraph = None
    cur_party_id = None

    for msg in chatlog['messages']:
        if cur_party_id is not None:
            if msg['pid'] != cur_party_id:
                # different party so print previously collated paragraph
                print(prv_paragraph)
                print('================')

                # reset current paragrapgh
                cur_paragraph = None
                cur_party_id = msg['pid']

        else:
            cur_party_id = msg['pid']

        cur_paragraph = msg['text'] if cur_paragraph is None else '{}{}{}'.format(cur_paragraph, '. ' if not cur_paragraph.endswith('.') else '',  msg['text'])
        prv_paragraph = cur_paragraph

    print(cur_paragraph)

def main():
    sample_xml_chat = os.path.join( os.path.split(__name__)[0], '..', 'samples', 'test.json' )
    sample_raw_chat = os.path.join( os.path.split(__name__)[0], '..', 'samples', 'sample_raw_chat.txt' )

    opt = 0

    if opt == 0:
        with open(sample_xml_chat, 'r') as file:
            content = file.read()
        parse_chatlog_json(content)

    else:
        with open(sample_raw_chat, 'r') as f: content = f.read()
        with open ('test.json', 'w') as file:
            file.write(create_chatlog_json(content, indent=4))
        

    

    return 0

if __name__ == '__main__':
    sys.exit(main())