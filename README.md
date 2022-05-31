# Pulling Discord Data Instrcutions

Prepared for the LabDAO <> TalentDAO collaborative effort on server health and community interaction. 

## Summary

---


This execution of a server exporting bot is done using Python on top of the disnake pythonic discord API and outputs to a location of your choice on your local machine. 

Package Requirements:
    - Python 3.8+
    - Disnake==2.4.0
    - Pandas, current distribution
    - aiohttp
    
This implementation also requires you to have a bot token created through the discord developer portal, found [here](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications). That is added to the target server. It is required that the bot has 'read_channel_history' permissions turned on. 

## Included Commands

1. CSV Channel
    - Run with !!CSVChannel
    - Makes a cache of the channel in which the command message is sent and saves to a CSV. 
2. CSVServer
    - Run with !!CSVServer
    - Makes a individual CSV for every channel in the server with each CSV titled the same as the channel.
3. SingleCSV
    - Run with !!SingleCSV 
    - Makes 1 CSV with every message sent in the server, with a column identifying which channel each message was sent in.

Output Fields:
- Discord Usernames 
- Discord Discriminator 
- Message Content
- Users Mentioned in the Message
- Time Stamp 
- If using 'SingleCSV' channel name is included.

If needed, including attachments, replies and other media can be developed in the future.

## Bot Installation and Setup 

The method requires three total files:
    - bot_main.py 
    - config.py 
    - cache_channel.py

As I am not familiar with the details of your machine, I will leave the installation of python and the relevant packages to you. 
All that is needed is a Python environment with Pandas and the disnake package installed. 
For a quick tutorial about making a bot and getting a token, see this [tutorial](https://www.howtogeek.com/364225/how-to-make-your-own-discord-bot/).

For this method, you only need to download the "Cache_Bot" folder onto your local machine.

1. Editing the Config File:
    - After making a bot on the discord developer portal,copy the token into the 'token section' of the file. 
    - The command prefix is the text string that triggers the bot, it can be changed based on user preference.
    - Do not change the "permissions" field.
    - The bot defaults to saving the output in the same folder as the code. If you would like to change this, put the file path in the form of a string in this field.

2. Add the bot to your discord server.
    - How to do this is covered in the tutorial linked above. 
    - The bot will automatically generate itself a role, make sure it has read channel history permissions. 

3. From your terminal, run bot_main.py.
    - You should see the bot appear online in discord and see a message printed on you terminal confirming your are logged in. 

4. In the discord type the name of a command with the command prefix set in the config file without spaces.
    - Example !!CSVServer
    - User sending the message must have administrator permission within the server.

5. Command completion.
    - After step 4, a CSV with '~' as its deliminator should appear in the desired location. and a Command complete message will appear in the terminal. 
    - For debugging, contact me **kellyd73#0168** on discord.
    

