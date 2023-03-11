import os
from apiutils.configs.sharedconfig import SHARED_CONFIG

def load_options():
    try:
        # then convert to python tuple
        opts = []
        for opt in SHARED_CONFIG['SUMMARIZER_OPTIONS']:
            opts.append((opt['tag'], opt['desc']))

        return opts

    except Exception as e:
        return [
            ('Failed', 'Failed: {}'.format(e))
        ]

SUMMARIZER_OPTIONS = load_options()
# Flag to use actual pytorch model or just a random summarizer
USE_ACTUAL_MODEL = False

# SUMMARIZER_OPTIONS = [
#     ('UseStrict', 'Strict summary'),
#     ('TreatAsMonologue', 'Treat transcript as monologue')
# ]