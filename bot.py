import os
import discord
import sqlite3
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

conn = sqlite3.connect('ClanPoints.sqlite')
cur = conn.cursor()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='potm')
@commands.has_role('Admin')
async def player_of_the_month(ctx, place, player):
    place = int(place)
    if place == 1:
        await ctx.send(f'1st place Player of the Month is {player}')
        sql = 'UPDATE ClanPoints SET points=points+7 WHERE player=?'
        cur.execute(sql, [player])
        conn.commit()
    elif place == 2:
        await ctx.send(f'2nd place Player of the Month is {player}')
        sql = 'UPDATE ClanPoints SET points=points+4 WHERE player=?'
        cur.execute(sql, [player])
        conn.commit()
    elif place == 3:
        await ctx.send(f'3rd place Player of the Month is {player}')
        sql = 'UPDATE ClanPoints SET points=points+2 WHERE player=?'
        cur.execute(sql, [player])
        conn.commit()
    else:
        print('error')

    sql = 'SELECT points FROM ClanPoints WHERE player=?'
    cur.execute(sql, [player])
    for row in cur.fetchall():
        points = row[0]
        print(player, 'now has', points, 'points')
        if points >= 62:
            ctx.send(f'{player} now has enough Clan Points to be an Admin')
        elif points >= 42:
            ctx.send(f'{player} is now a General')
        elif points >= 28:
            ctx.send(f'{player} is now a Captain')
        elif points >= 17:
            ctx.send(f'{player} is now a Lieutenant')
        elif points >= 8:
            ctx.send(f'{player} is now a Sergeant')
        elif points >= 3:
            ctx.send(f'{player} is now a Corporal')


@bot.command(name='cap', help='Type Discord or player name after command')
@commands.has_role('Admin')
async def on_cap(ctx, player):
    await ctx.send(f'Successfully updated {player}')
    print(player, 'capped')
    sql = 'UPDATE ClanPoints SET points=points+2 WHERE player=?'
    cur.execute(sql, [player])
    conn.commit()
    sql = 'SELECT points FROM ClanPoints WHERE player=?'
    cur.execute(sql, [player])
    for row in cur.fetchall():
        points = row[0]
        print(player, 'now has', points, 'points')
        if points >= 62:
            ctx.send(f'{player} now has enough Clan Points to be an Admin')
        elif points >= 42:
            ctx.send(f'{player} is now a General')
        elif points >= 28:
            ctx.send(f'{player} is now a Captain')
        elif points >= 17:
            ctx.send(f'{player} is now a Lieutenant')
        elif points >= 8:
            ctx.send(f'{player} is now a Sergeant')
        elif points >= 3:
            ctx.send(f'{player} is now a Corporal')


@bot.event
async def on_member_join(member):
    welcome_message = 'welcome to the SAD Clan Discord server!'
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, {welcome_message}'
    )
    role = discord.utils.get(member.guild.roles, name='Recruit')
    await member.add_roles(role)
    try:
        sql = 'INSERT INTO ClanPoints VALUES (?, 1)'
        cur.execute(sql, [member.name])
    except:
        print(member.name, 'is already in the database')


@bot.event
async def on_raw_reaction_add(payload):
    print(payload)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    if 'capped' in message.content.lower() and message.channel.name == 'citadel-and-recruitment':
        author = (str(message.author).split('#'))
        player = author[0]
        await message.channel.send(f'Thank you for capping at the citadel, {player}!')
        sql = 'UPDATE ClanPoints SET points=points+2 WHERE player=?'
        cur.execute(sql, [player])
        conn.commit()
        print(player, 'capped')
        sql = 'SELECT points FROM ClanPoints WHERE player=?'
        cur.execute(sql, [player])
        for row in cur.fetchall():
            points = row[0]
            print(player, 'now has', points, 'points')
            if points >= 62:
                role = discord.utils.get(message.author.guild.roles, name='Admin')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='General')
                await message.author.remove_roles(role2)
            elif points >= 42:
                role = discord.utils.get(message.author.guild.roles, name='General')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Captain')
                await message.author.remove_roles(role2)
            elif points >= 28:
                role = discord.utils.get(message.author.guild.roles, name='Captain')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Lieutenant')
                await message.author.remove_roles(role2)
            elif points >= 17:
                role = discord.utils.get(message.author.guild.roles, name='Lieutenant')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Sergeant')
                await message.author.remove_roles(role2)
            elif points >= 8:
                role = discord.utils.get(message.author.guild.roles, name='Sergeant')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Corporal')
                await message.author.remove_roles(role2)
            elif points >= 3:
                role = discord.utils.get(message.author.guild.roles, name='Corporal')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Recruit')
                await message.author.remove_roles(role2)

    elif 'capped' in message.content:
        await message.channel.send('''
        If you capped at the citadel, please type "capped" in the "citadel-and-recruitment" channel''')

    if 'recruited' in message.content.lower() and message.channel.name == 'citadel-and-recruitment':
        player = (str(message.author).split('#')[0])
        await message.channel.send(f'{player}, Thank you for recruiting!')
        sql = 'UPDATE ClanPoints SET points=points+2 WHERE player=?'
        cur.execute(sql, [player])
        conn.commit()
        print(player, 'recruited someone')
        sql = 'SELECT points FROM ClanPoints WHERE player=?'
        cur.execute(sql, [player])
        for row in cur.fetchall():
            points = row[0]
            print(player, 'now has', points, 'points')
            if points >= 62:
                role = discord.utils.get(message.author.guild.roles, name='Admin')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='General')
                await message.author.remove_roles(role2)
            elif points >= 42:
                role = discord.utils.get(message.author.guild.roles, name='General')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Captain')
                await message.author.remove_roles(role2)
            elif points >= 28:
                role = discord.utils.get(message.author.guild.roles, name='Captain')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Lieutenant')
                await message.author.remove_roles(role2)
            elif points >= 17:
                role = discord.utils.get(message.author.guild.roles, name='Lieutenant')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Sergeant')
                await message.author.remove_roles(role2)
            elif points >= 8:
                role = discord.utils.get(message.author.guild.roles, name='Sergeant')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Corporal')
                await message.author.remove_roles(role2)
            elif points >= 3:
                role = discord.utils.get(message.author.guild.roles, name='Corporal')
                await message.author.add_roles(role)
                role2 = discord.utils.get(message.author.guild.roles, name='Recruit')
                await message.author.remove_roles(role2)

    elif 'recruited' in message.content.lower():
        await message.channel.send('''
        If you recruited someone, please say who you recruited in the "citadel-and-recruitment" channel''')


@bot.event
async def on_member_update(before, after):
    if before.name != after.name:  # to only run on status
        cur.execute('UPDATE ClanPoints SET player=after WHERE player=before')
        print(before, 'changed their name to', after)
    if before.add_roles != after.add_roles:
        player = str(after).split('#')[0]
        print(player, 'has a new role')


@bot.event
async def on_command_error(ctx, exception):
    await ctx.send(exception)


@bot.event
async def on_error(event, *args):    # add **kwargs if needed
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
            print('===unhandled message===')
        else:
            raise


bot.run(TOKEN)
