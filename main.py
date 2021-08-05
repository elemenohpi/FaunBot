import discord
import eletility as ele

L = ele.Log()

class FaunBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)

        self.role_message_id = 860950196098433044 # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name="pangames", id=861789742205763604): 860935128251367425, # ID of the role associated with unicode emoji 
            discord.PartialEmoji(name="pantopica", id=861794756295393300): 860935293975658496, # ID of the role associated with unicode emoji 
            discord.PartialEmoji(name="pandota", id=861788986895630338): 860934998944645150, # ID of the role associated with unicode emoji 
            discord.PartialEmoji(name="panwow", id=861788272924557324): 860934805200568332, # ID of the role associated with unicode emoji 
            discord.PartialEmoji(name="pansports", id=861843265954775061): 861845346150121512, # ID of the role associated with unicode emoji 
        }

        self.guild_id = 471416214141534208
        self.channel_id = 778670992809656371
        self.msg_id = 860950196098433044

    async def on_ready(self):
        print('Logged on as', self.user)
        channel = self.get_channel(self.channel_id)
        message = await channel.fetch_message(self.msg_id)
        await message.add_reaction(discord.PartialEmoji(name="pangames", id=861789742205763604))
        await message.add_reaction(discord.PartialEmoji(name="pantopica", id=861794756295393300))
        await message.add_reaction(discord.PartialEmoji(name="pandota", id=861788986895630338))
        await message.add_reaction( discord.PartialEmoji(name="panwow", id=861788272924557324))
        await message.add_reaction( discord.PartialEmoji(name="pansports", id=861843265954775061))
        

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            L.W("Role doesn't exist!")
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            L.W("Role doesn't exist!")
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            L.W("Member doesn't exist!")
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass


    # async def on_message(self, message):
    #     await self.getmsg(123)
    #     print("self.getmsg(123)", self.getmsg(123))

    #     if message.author == bot.user:
    #         return

    #     guild = message.guild
    #     channel = message.channel
    #     user = message.author

    #     if message.content.startswith("~parsa"):
    #         role = discord.utils.get(guild.roles, name="Movie")
    #         MESSAGE = "{0.name} is now officially a fan of parsa fanboi/gurl group of this channel!".format(user)
    #         await channel.send(MESSAGE)
    #         await user.add_roles(role)




bot = FaunBot()
bot.run("ODM1ODczNDAzMTQ2ODYyNTky.YIVxxQ.cUS67ThyO30iTxlHn3HDccIs_O8")

