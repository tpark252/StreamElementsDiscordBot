# to request api data
import requests
# necessary to utilize the Discord app
import discord
# config
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# username is the streamelements channel
username = config['CHANNEL']['Username']
# defines the Discord client
client = discord.Client()
# config.ini for all secret tokens and ids
token = config['STREAMELEMENTS']['Token']
channel_id = config['CHANNEL']['Channel_id']
bot_token = config['DISCORD']['Bot_Token']


# registers events
@client.event
# This signifies when the bot is logged in and running
async def on_ready():
    print("STATUS: LOGGED IN {0.user}".format(client))


@client.event
# The on_message signifies when the bot receives a message, but *if* the user submitting a message is the client
# user, *then* the code will return or skip over.
async def on_message(message):
    args = message.content.split(' ')
    if message.author == client.user:
        return

        # if user sends a specific message, the bot will respond with written "".
    if message.content.startswith("borkithy"):
        await message.channel.send("what you want")
    if message.content.startswith("!getpoints") and len(args) == 2:
        target_user = args[1]
        points = \
            requests.get('https://api.streamelements.com/kappa/v2/points/{}/{}'.format(channel_id, target_user)).json()[
                'points']
        await message.channel.send("{}'s points: {}".format(target_user, points))
    if message.content.startswith("!editpoints") and message.author.guild_permissions.administrator and len(args) == 3:
        target_user = args[1]
        points = args[2]
        header = {'authorization': 'Bearer {}'.format(token)}
        balance = \
            requests.put('https://api.streamelements.com/kappa/v2/points/{}/{}/{}'.format(channel_id, target_user, points),
                         headers=header).json()['newAmount']
        await message.channel.send("Added points to {}".format(target_user))
        await message.channel.send("Previous balance: {}".format((int(balance) - int(points))))
        await message.channel.send("New balance: {}".format(balance))
    if message.content.startswith("!leaderboard"):
        param = {'limit': '10', 'offset': '0'}
        embed = discord.Embed(title="Leaderboard", url="https://streamelements.com/borktea/leaderboard", color=0xccf2ff)
        embed.set_thumbnail(url="https://i.imgur.com/PhwV8dG.jpg")

        for user in \
                requests.get('https://api.streamelements.com/kappa/v2/points/{}/top'.format(channel_id),
                             params=param).json()[
                    'users']:
            embed.add_field(name="{}".format(user['username']), value="{}".format(user['points'], inline=False))

        await message.channel.send(embed=embed)


# runs the environment variable to connect the discord bot
client.run(bot_token)
