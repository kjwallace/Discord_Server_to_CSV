import os

def Config():
    config={
            "token":'MTA0OTA1NDQ1MDg5NzE0MTg3MQ.GTQOza.kx9hxl15Wt8BZa4ptIwoshYDJOuDmGAPl1e6pA',
            "command_pref":"!!",
            "permissions":8,
            "output_url" : f'{os.path.dirname(os.path.realpath(__name__))}/Output_CSVs'
            }
    return config
