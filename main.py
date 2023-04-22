import  time, threading, json, os
import discord
from discord import app_commands

from libs import twitch

class Data():
    tokens_data = open('Integrity_tokens.txt',"r").read().splitlines()

def update_tok():
    while True:
        Data.tokens_data = open('Integrity_tokens.txt',"r").read().splitlines()
        time.sleep(100)

threading.Thread(target=update_tok).start()

config = json.loads(open("config.json","r", encoding="utf8").read())
proxies = open('proxy.txt',"r").read().splitlines()

banner = "https://cdn.discordapp.com/attachments/1086656323837513769/1086656384520704071/excer.png"
embed_color = 16705372



class Discord_Bot:

    bot = None
    TwitchTools = None
    followed_users = []
    friend_users = []
    view_list = {}

    def __init__(self) -> None:

        self.TwitchTools = twitch.Tools()
        self.TwitchFollowers = twitch.Follow()

        self.bot_prefix = config['bot_config']["prefix"]
        self.bot_token = config['bot_config']["token"]
        self.server_id = config['bot_config']["server_id"]
        self.twitch_channel = config['bot_config']["twitch_channel"]

        os.system("cls")

        self.run_bot()
        

    def commands(self):

        @self.bot.event
        async def on_ready():
            await self.tree.sync(guild=discord.Object(id=self.server_id))
            await self.bot.change_presence(activity=discord.Game(name=f"excer.pro"))
            

        # USER
        
        @self.tree.command(name="tfollow",description="[TWITCH] Send twitch followers to selected channel", guild=discord.Object(id=self.server_id))
        async def tfollow(interaction, username: str,):
            if interaction.channel.id == self.twitch_channel:
                target_id = self.TwitchTools.user_id(username)
                if target_id in self.followed_users:
                    embed = discord.Embed(color=embed_color, description=f"```Cant follow 2 times same account wait for restock```")
                    embed.set_image(url=banner)
                    await interaction.response.send_message(embed=embed)
                    return
                if target_id != False:
                    for role_name in reversed(config['tfollow']):
                        if discord.utils.get(interaction.guild.roles, name=role_name) in interaction.user.roles:
                            follow_count = config['tfollow'][role_name]
                            self.TwitchFollowers.send_follow(target_id, follow_count, Data.tokens_data)
                            self.followed_users.append(target_id)
                            embed = discord.Embed(color=embed_color, description=f"```Excer Followers -> {follow_count}```")
                            embed.set_image(url=banner)
                            await interaction.response.send_message(embed=embed)
                            return
                else:
                    embed = discord.Embed(color=embed_color, description=f"```Invalid Username```")
                    embed.set_image(url=banner)
                    await interaction.response.send_message(embed=embed)
                    return

        
    def run_bot(self):

        self.bot = discord.Client(
            command_prefix=self.bot_prefix, 
            help_command=None, 
            intents=discord.Intents().all()
        )

        self.tree = app_commands.CommandTree(self.bot)

        self.commands()
        self.bot.run(self.bot_token)
        


if __name__ == "__main__":

    Discord_Bot()
