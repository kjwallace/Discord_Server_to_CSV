import json 
import os 
import platform 
import random 
import sys
from datetime import time  

import disnake 
from disnake import ApplicationCommandInteraction  
from disnake.ext.commands import Bot 
from disnake.ext.commands import Context 


from config import Config 



class Cache_Bot(commands.Bot):
    '''
    Load config variables, status variables, gm messages and intents
    '''
    config = Config()
    

#Bot command and interaction intents 
    intents = disnake.Intents.default()

    intents.dm_messages = True 
    intents.dm_reactions = True
    intents.members = True 
    intents.guild_typing = True 
    intents.typing = False
    intents.presences = False
    intents.reactions = True
    
    def __init__(self,config = config):
        
        self.config = config
        
        
        super().__init__(command_prefix = commands.when_mentioned_or(config['command_pref']),
                         intents = intents, 
                         case_insensitive = True )
        
        self.autoload_extensions('cache_command')
        
       
    
    
    def autoload_extensions(self, command_type):
        for file in os.listdir(f'./{command_type}'):
           extension = file[:-3]
           end = file[-3:]
           
           if end == '.py':
               try:
                   self.load_extension(f"cogs.{command_type}.{extension}")
                   print(f"Loaded {extension}!")
               except Exception as e:
                   exception = f"{type(e).__name__}: {e}"
                   print(f"Failed to load {extension} due to {exception}")
           else:
                print(f'Ignored {file}')
    
if __name__ == '__main__':
    bot = Cache_Bot()
    token = bot.config['token']
    #bot.remove_command('help')
    #bot.autoload_extensions('help')
    
    if token is not None:
        bot.run(token)
    else:
        print('Log In Failure, check location of token.')