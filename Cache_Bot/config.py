import os

def Config():
    config={
            "token":'MTA0OTUxMTI4NDc3NDgwNTYwNQ.GTbqOC.K9o53DhOTVg28hdp5JpmU5CjUqbkrrPdGrlGvo',
            "command_pref":"!!",
            "permissions":8,
            "output_url" : f'{os.path.dirname(os.path.realpath(__name__))}/Output_CSVs'
            }
    return config
