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
    
def dont_use_model():
    # true means to not use the actual ml model and instead the random summarizer
    # must exist and must be set to 1
    ev = os.environ.get('CHATBERTA_NO_MODEL') 
    return (ev is not None and str(ev) == '1' ) 
 
SUMMARIZER_OPTIONS = load_options()
# Flag to use actual pytorch model or just a random summarizer
USE_ACTUAL_MODEL = not dont_use_model()

# SUMMARIZER_OPTIONS = [
#     ('UseStrict', 'Strict summary'),
#     ('TreatAsMonologue', 'Treat transcript as monologue')
# ]