import sys
import traceback
import time
import json
import os



# try:
#     from apiutils.functions.PushBulletFileServer import prettify
#     from apiutils.functions.ChatParser import create_chatlog_json
#     import requests
#     print('Importing network component...')
#     start0 = time.time()
#     from apiutils.nec.NetworkComponent import NetworkComponent
#     end0 = time.time()
#     print(f'Done importing network component: {end0-start0} seconds')
#     from apiutils.configs.summarizer import USE_ACTUAL_MODEL
# except:
#     # if any imports fail do
#     traceback.print_exc()
#     sys.exit(1)





def test_model_usage():
    try:
        root = os.path.abspath (os.path.join(os.path.split(__file__)[0], '..' ) )
        if root not in sys.path: sys.path.append(root)
        from apiutils.functions.PushBulletFileServer import prettify
        from apiutils.functions.ChatParser import create_chatlog_json
        import requests
        print('Importing network component...')
        start0 = time.time()
        from apiutils.nec.NetworkComponent import NetworkComponent
        end0 = time.time()
        print(f'Done importing network component: {end0-start0} seconds')
        from apiutils.configs.summarizer import USE_ACTUAL_MODEL


        print('In main!')
        root = os.path.abspath (os.path.join(os.path.split(__file__)[0], '..' ) )
        faddr = os.path.join ( root, 'apiutils', 'samples', 'sample_raw_chat_1.txt')

        with open(faddr) as file:
            sample_pkg = json.loads(create_chatlog_json( str(file.read())))


        summary_options = {
            "basic_options": [ "strictSummarize", "treatAsMonologue"],
            "summarize_only_for": -1 
        }

        use_model = True

        print('Loading network component')
        start1 = time.time()
        nec = NetworkComponent(use_model=use_model, propagate_errors=True)
        end1 = time.time()
        print(f'Model loading took: {end1-start1} seconds')

        print('Doing summary')
        start2 = time.time()
        res, summary_package = nec.summarize(sample_pkg, summary_options)
        end2 = time.time()
        print(f'Model summarization took: {end2-start2} seconds')

        if res != 0:
            raise Exception('Something went wrong!')
        
        print(prettify(summary_package))

        return 0
    except:
        traceback.print_exc()
        return 2

def main():
    return test_model_usage()
    

if __name__ == "__main__":
    sys.exit(main())
