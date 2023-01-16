import json
import os

def load_options():
    try:
        # read the json file
        read_options = open(os.path.join('..', 'src', 'shared', 'config.json')).read()

        # convert to actual python dict
        read_options = json.loads(read_options)

        # then convert to python tuple
        opts = []
        for opt in read_options['summarizerOptions']:
            opts.append((opt['tag'], opt['desc']))

        return opts

    except Exception as e:
        return [
            ('Failed', 'Failed: {}'.format(e))
        ]

SUMMARIZER_OPTIONS = load_options()

# SUMMARIZER_OPTIONS = [
#     ('UseStrict', 'Strict summary'),
#     ('TreatAsMonologue', 'Treat transcript as monologue')
# ]