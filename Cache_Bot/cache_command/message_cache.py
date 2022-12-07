#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 19:01:39 2022


"""

import disnake 
from disnake.ext import commands 
from disnake.ext.commands import Context
import pandas as pd
import re



class CSV_Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.category = 'Backend'
        
        
    @commands.command(
        name = 'CSVChannel',
        description = 'Creates a CSV containing every message and user in the #Introduction channel'
        )
    async def cacheChannel(self, context: Context, *, intro: str = None) -> None:
        columns = ['username', 'disc', 'message_content', 'mentions', 'time_stamp']
        df = pd.DataFrame(columns = columns)
        messages = await context.channel.history(limit=None).flatten()
        #discriminate between real intros and current user response to intro
        if intro is not None:
            for message in messages:
                #member = await disnake.Member(context.guild.getch_member(message.author.id))
                if True :  #(message.created_at - member.joined_at) < timedelta(days =3):
                    user = message.author.name
                    dics = message.author.discriminator
                    text = mention_to_user(content = message.content, guild = context.guild)
                    time_stamp = message.created_at
                    mens = []
                    for people in message.mentions:
                        mens += [str(people)]
                    temp_df = pd.DataFrame(data = {'username': [user], 'disc': [dics], 'message_content': [text],'mentions': mens, 
                    'time_stamp': [time_stamp.strftime("%m/%d/%Y, %H:%M:%S")]})
                    #temp_df = pd.DataFrame(data = [user, dics, content, time_stamp.strftime("%m/%d/%Y, %H:%M:%S")], Axis = 1)
                    #temp_df = {'username': user, 'disc': dics, 'message_content': content, 'time_stamp': time_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
                    df = pd.concat([df, temp_df], ignore_index = True)
                    
            #cache message 
            
        else:
            for message in messages:
                
                user = message.author.name
                dics = message.author.discriminator
                text = mention_to_user(content = message.content, guild = context.guild)
                
                
                time_stamp = message.created_at
                mens = []
                for people in message.mentions:
                    mens += [str(people)]
                temp_df = pd.DataFrame(data = {'username': [user], 'disc': [dics], 'message_content': [text],'mentions': [mens], 'time_stamp': [time_stamp.strftime("%m/%d/%Y, %H:%M:%S")]})
                #temp_df = pd.DataFrame(data = [user, dics, content, time_stamp.strftime("%m/%d/%Y, %H:%M:%S")], Axis = 1)
                #temp_df = {'username': user, 'disc': dics, 'message_content': content, 'time_stamp': time_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
                df = pd.concat([df, temp_df], ignore_index = True)
        
        df.to_csv(f'{self.bot.config["output_url"]}/{context.channel.name}.csv', sep = '~')
        print(f"Finished running on {context.channel.name}")

    @commands.command(
        name = 'CSVServer',
        description = 'Makes a CSV cache of the entire dircord server')
    async def CacheServer(self, context: Context) -> None:
        channels = await context.guild.fetch_channels()
        '''
        for channel in channels:
            print(channel.name)
            print(channel.type)
            print(channel.type == disnake.ChannelType.text)
            print('_______________________________')
        '''
        for channel in channels:
            messages=[]
            in_threads = {}
            for thread in channel.guild.threads:
                for message in await thread.history(limit=None).flatten() :
                    messages += [message]
                    in_threads[message.id] = [thread.name, channel.name]

            if channel.type == disnake.ChannelType.text:
                columns = ['username', 'disc', 'message_content', 'mentions','time_stamp', 'replied_to_message', 'replied_to_user', 'from_thread', 'from_thread_name']
                df = pd.DataFrame(columns = columns)
                messages += await channel.history(limit=None).flatten()

                for message in messages:
                    # check if the message is from a thread
                    if message.thread is not None:
                        thread = True
                        thread_name = message.thread.name + '-' + channel.name
                    elif message.id in in_threads:
                        thread_name = in_threads[message.id][0]+'-'+in_threads[message.id][1]
                    else:
                        thread = False
                        thread_name = ""
                    replied_to_message = ""
                    replied_to_user = ""
                    # regonize if the message is a reply
                    if message.type == disnake.MessageType.reply:
                        replied_to_message = message.reference.resolved.content
                        replied_to_user = message.reference.resolved.author.name

                    user = message.author.name
                    dics = message.author.discriminator
                    text = mention_to_user(content = message.content, guild = context.guild)
                    time_stamp = message.created_at
                    mens = []
                    for people in message.mentions:
                        mens += [str(people)]
                    temp_df = pd.DataFrame(data = {'username': [user], 'disc': [dics], 'message_content': [text],'mentions': [mens], 
                            'time_stamp': [time_stamp.strftime("%m/%d/%Y, %H:%M:%S")], 'replied_to_message': [replied_to_message], 'replied_to_user': [replied_to_user]
                            , 'from_thread': [thread], 'from_thread_name': [thread_name]})
                        #temp_df = pd.DataFrame(data = [user, dics, content, time_stamp.strftime("%m/%d/%Y, %H:%M:%S")], Axis = 1)
                        #temp_df = {'username': user, 'disc': dics, 'message_content': content, 'time_stamp': time_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
                    df = pd.concat([df, temp_df], ignore_index = True)
                
                df.to_csv(f'{self.bot.config["output_url"]}/{channel.name}.csv', sep = '~')
                print(f'Finished caching {channel.name}')
            else:
                pass
        print("Done")
    
    @commands.command(
        name = 'SingleCSV',
        description = 'Makes the whole server into a one CSV')
    async def SingleCSV(self, context: Context) -> None:
        channels = await context.guild.fetch_channels()
        columns = ['username', 'disc', 'user_roles', 'message_content', 'mentions','channel_name', 'guild','time_stamp']
        df = pd.DataFrame(columns = columns)
        
        for channel in channels:
            if channel.type == disnake.ChannelType.text:
                
                messages = await channel.history(limit=None).flatten()
                
                for message in messages:
                    


                    user = message.author.name
                    dics = message.author.discriminator
                    text = mention_to_user(content = message.content, guild = context.guild)
                    time_stamp = message.created_at
                    mens = []
                    for people in message.mentions:
                        mens += [str(people)]
                    '''    
                    user_roles = []
                    for roles in message.author.roles:
                        user_roles += [str(roles)]
                    '''    
                    
                    temp_df = pd.DataFrame(data = {'username': [user], 'disc': [dics], 'message_content': [text],'mentions': [mens], 
                    'channel_name': [channel.name],'guild':[context.guild.name], 'time_stamp': [time_stamp.strftime("%m/%d/%Y, %H:%M:%S")]})
                        #'user_roles': [user_roles[1:]
                        #temp_df = {'username': user, 'disc': dics, 'message_content': content, 'time_stamp': time_stamp.strftime("%m/%d/%Y, %H:%M:%S")}
            
                    df = pd.concat([df, temp_df], ignore_index = True)
                    
        df.to_csv(f'{self.bot.config["output_url"]}/{context.guild.name}_full.csv', sep = '~')
        print("Done running full server")
        
        
        
       
        
       
                
       
            
def setup(bot):
    bot.add_cog(CSV_Channel(bot))
    
def mention_to_user(content : str, guild: disnake.Guild) -> str:
    message = content
    
    for matches in re.findall(r'\<@\d+\>', content):
        
        user = guild.get_member(int(matches[2:-1]))
        output = re.sub(r'\<@\d+\>', str(user), message, count = 1)
        message = output
        
    return message 
        
        
        
            
        
