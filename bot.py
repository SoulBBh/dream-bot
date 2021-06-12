import discord
import json
from discord import embeds
from discord import channel
from discord.colour import Colour
from discord.ext import commands
import random

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="All Member | +help"))
    print('bot đã online')

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'đã Kick {member.mention}')

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Đã Banned {member.mention}')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Đã Unbanned {user.mention} Thành Công')
            return

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Bạn Éo Có Chức Để Dùng Cmd Này.')

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['hỏi', 'future'])
async def _8ball(ctx, *, question):
    responses = ['có.',
                 'không.']
    await ctx.send(f'câu hỏi: {question}\ntrả lời: {random.choice(responses)}')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        prefixes[str(guild.id)] = '+'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

@client.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Color.green()
    )

    embed.set_author(name="Cách Lệnh Của Bot(+help)")
    embed.add_field(name="+ping", value="Để Chs Ping Pong", inline=True)
    embed.add_field(name="+hỏi", value="để đặt câu hỏi có hoặc ko       ", inline=True)
    embed.add_field(name="+clear", value="xoá một số lượng cụ thể", inline=True)
    embed.add_field(name="+ban", value="cấm ng bị ban vào server", inline=True)
    embed.add_field(name="+kick", value="đá người vi phạm ra khoải server", inline=True)
    embed.add_field(name="+unban", value="huỷ lệnh cấm ng bị ban", inline=True)
    embed.add_field(name="+pray", value="lạy online", inline=True)
    embed.set_footer(text="đó là tất cả lệnh bot có(bot được lập trình bởi EpicDinoSuit#1234)")

    await ctx.send(embed=embed)

@client.command()
async def pray(ctx):
    await ctx.send(f'Tao Lạy Mày!!!')

client.run('ODA2NDMzMDU3MDcwMTIwOTYx.YBpXTw.4bKCtQWCXGjnsX_lxWbBTzju55E')
