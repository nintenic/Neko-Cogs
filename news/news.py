import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help
import os
import asyncio

class News:
    """Allow users to signup for news."""

    def __init__(self, bot):
        self.bot = bot
        self.savefile = "data/news/registered.json"
        self.data = dataIO.load_json(self.savefile)
        

    @commands.group(pass_context=True, invoke_without_command=True)
    async def news(self, ctx):
        """Newsletter Commands"""
        
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    

    @newsletter.command(pass_context=True)
    async def start(self, ctx):
        """Start recieving newsletters."""
        
        weeb = ctx.message.author
        if weeb.id not in self.data:
            await self.bot.say("Ok {}, please wait a moment while I set things up.".format(weeb.mention))
            self.data[weeb.id] = {'send' : True}
            dataIO.save_json(self.savefile, self.data)
            await self.bot.say("You're now setup to recieve our newsletter! You can turn it off by saying `{}news stop`".format(ctx.prefix))
        else:
            news = self.data[weeb.id]['send']
            if news is False:
                self.data[weeb.id]['send'] = True 
                dataIO.save_json(self.savefile, self.data)
                await self.bot.say("Great! You will now start recieving newsletters!")
            else :    
                await self.bot.say("You're already registered for the newsletter.")
                
    @newsletter.command(pass_context=True)
    async def stop(self, ctx):
        """Stop recieving newsletters."""
        
        weeb = ctx.message.author
        if weeb.id in self.data:
            news = self.data[weeb.id]['send']
            if news is True:
                self.data[weeb.id]['send'] = False 
                dataIO.save_json(self.savefile, self.data)
                await self.bot.say("Ok, we'll turn off your newsletter subscription.")
            else:
                await self.bot.say("You're already unsubscribed from the newsletter.")
        else:
            await self.bot.say("{}, you need a newsletter account first. Say `{}news start` to begin.".format(weeb.mention, ctx.prefix))
            
            
    @checks.is_owner()
    @newsletter.command(pass_context=True)
    async def send(self, ctx, *, msg):
        """Owner Only - Sends a Newsletter."""

        if len(self.data) <= 0:
            await self.bot.say("You can't send a newsletter if no one is registered.")
            return
        
        for id in self.data:
            if self.data[id]['send']: 
                user = self.bot.get_user_info(id)
                message = "**{} Newsletter!\n\n**".format(self.bot.user.name)
                message += msg
                message += "\n\n*If you no longer want to get these messages, just say `{}news stop`".format(ctx.prefix)
                users = discord.utils.get(self.bot.get_all_members(),
                                  id=id)
                try:
                    await self.bot.send_message(users, message)
                    
                except:
                    await self.bot.say("The message didn't go thru :angry:")
                
                asyncio.sleep(1)
            else:
                pass
        else:
            await self.bot.say("Newsletter has been sent out!")

def check_folders():
    if not os.path.exists("data/news"):
        print("Creating the news folder, so be patient...")
        os.makedirs("data/news")
        print("Finish!")

def check_files():
    twentysix = "data/news/registered.json"
    json = {}
    if not dataIO.is_valid_json(twentysix):
        print("Derp Derp Derp...")
        dataIO.save_json(twentysix, json)

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Newsletter(bot))
