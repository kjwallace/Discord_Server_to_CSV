import os

def Config():
    config={
            "token":'MTA1NjMwMDYyOTEyMDc5ODc2MA.GOnaoV.a3F9gcnSXzWvaNMVC732J5V5oz89u01Y28PPFE',
            "command_pref":"!!",
            "permissions":8,
            "output_url" : f'{os.path.dirname(os.path.realpath(__name__))}/Output_CSVs'
            }
    return config
