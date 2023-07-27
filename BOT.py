

import random
import discord

intents = discord.Intents.default()
intents.presences = True
intents.guilds = True
intents.members = True
intents.messages = True
intents.guild_messages = True
intents.reactions = True
intents.emojis = True
intents.message_content=True
client = discord.Client(intents=intents)
trigger_phrases = ['hello',  'greetings', 'heya', 'helo', 'hey','hiya']
trigger_phrases2 = ['hello!', 'hi!', 'greetings!', 'heya!', 'helo!', 'hey!']
trigger_phrases3=['hello', 'hi' ,'greetings', 'heya', 'helo', 'hey']
responses = ['hello human',  'hi human', 'greetings human']
allowed_roles_ids=[1093538779266039829,1093528370177904710,1093526905531146240]
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check for trigger phrases and reply to the message
    if message.content.lower() in trigger_phrases3 or any(message.content.lower().startswith(trigger) for trigger in trigger_phrases2) or any(message.content.lower().startswith(trigger) for trigger in trigger_phrases):
        # Check if the message is a reply
        if message.reference is not None:
            replied_message_id = message.reference.message_id
            replied_message = await message.channel.fetch_message(replied_message_id)
            response = random.choice(responses)
            await replied_message.reply(response, mention_author=False)
        else:
            response = random.choice(responses)
            await message.reply(response, mention_author=False)

    # Handle whisper command
    if message.content.startswith('-whisper '):
        await message.channel.send(message.content[8:])
 
    if message.content.startswith('-echo '):
     
     if any(role.id in allowed_roles_ids for role in message.author.roles):
      try:
        channel_id = message.content[8:27]
        channel = await client.fetch_channel(channel_id)
        await channel.send(message.content[28:])
      except Exception as ex:
         await message.channel.send("couldnt find channel/improper syntax")

    if message.content.startswith('-edit ') and any(role.id in allowed_roles_ids for role in message.author.roles):

        try:
          message_id = int(message.content[6:25])
          message_content = message.content[26:]
          channel = message.channel
          message_to_edit = await channel.fetch_message(message_id)

          if message_to_edit.author != client.user:
              # message was not sent by bot
              await message.channel.send("Cannot edit message: not sent by bot")
          else:
              await message_to_edit.edit(content=message_content)


        except ValueError:
          # message_id is not a valid integer
          await message.channel.send("Invalid message ID")

        except discord.Forbidden:
          # bot doesn't have permission to edit the message
          await message.channel.send("Cannot edit message: insufficient permissions")

        except discord.NotFound:
          # message with message_id was not found
          await message.channel.send("Cannot find message with given ID")


  # Run the Discord client

try:
    client.run('MTA2NTYwMDk4OTE2OTcxMzIzNA.GXsHMP.PgDT-urh3WewqenTW-a_6X4cVKFPiyE34cBa9E')
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e