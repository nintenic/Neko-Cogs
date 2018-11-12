import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from .utils import checks
from __main__ import send_cmd_help
import os
import asyncio

class Newsletter:
    """Allow users to sign up for our newsletter."""

    def __init__(self, bot):
        self.bot = bot
        self.savefile = "data/news/registered.json"
        self.news = dataIO.load_json(self.savefile)
        

    @commands.group(pass_context=True, invoke_without_command=True)
    async def newsletter(self, ctx):
        """Newsletter Commands"""
        
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    

    @newsletter.command(pass_context=True)
    async def signup(self, ctx):
        """Signup for our newsletter."""
        
        weeb = ctx.message.author
        if weeb.id not in self.news:
            await self.bot.say("Ok {}, please wait a moment while I set things up.".format(weeb.mention))
            self.news[weeb.id] = {'send' : True}
            dataIO.save_json(self.new, self.news)
            await self.bot.say("You're now setup to recieve our newsletter! You can turn it off by saying `{}newsletter unsubscribe`".format(ctx.prefix))
        else:
            if news is False:
                self.news[weeb.id]['send'] = True 
                dataIO.save_json(self.new, self.news)
                await self.bot.say("Great! You will now start recieving newsletters!")
            else :    
                await self.bot.say("You're already registered for the newsletter.")
                
    @newsletter.command(pass_context=True)
    async def unsubscribe(self, ctx):
        """Allows you to turn off the your newsletter subscription."""
        
        weeb = ctx.message.author
        if weeb.id in self.news:
            news = self.news[weeb.id]['send']
            if news is True:
                self.news[weeb.id]['send'] = False 
                dataIO.save_json(self.new, self.news)
                await self.bot.say("Ok, we'll turn off your newsletter subscription.")
            else:
                await self.bot.say("You're already unsubscribed from the newsletter.")
        else:
            await self.bot.say("{}, you need a newsletter account first. Say `{}newsletter signup` to start.".format(weeb.mention, ctx.prefix))
            
            
    @checks.is_owner()
    @newsletter.command(pass_context=True)
    async def send(self, ctx, *, msg):
        """Owner Only - sends a newsletter."""

        if len(self.news) <= 0:
            await self.bot.say("You can't send a newsletter if no one is registered.")
            return
        
        for id in self.news:
            if self.news[id]['send']: 
                user = self.bot.get_user_info(id)
                message = "**{} Newsletter!\n\n**".format(self.bot.user.name)
                message += msg
                message += "\n\n*If you no longer want to get these notices, just say `{}newsletter unsubscribe`".format(ctx.prefix)
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
