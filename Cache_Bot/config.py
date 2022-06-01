import os

def Config():
    config={
            "token":'your_token_here',
            "command_pref":"!!",
            "permissions":8,
            "output_url" : os.path.dirname(os.path.realpath(__name__))
            }
    return config
