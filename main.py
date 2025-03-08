#!/bin/python
import discord
from discord.ext import commands
import asyncio
import aiohttp
import json
import re
from zabbix_utils import AsyncZabbixAPI

with open('config.json') as config_file:
    config = json.load(config_file)

# Discord bot token en Zabbix API details
DISCORD_TOKEN = config['discord_token']
ZABBIX_URL = config['zabbix_host']
ZABBIX_TOKEN = config['api_token']

ZABBIX_AUTH = {
    "url": config['zabbix_host']
}

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Make sure to enable guilds intent
bot = commands.Bot(command_prefix='/', intents=intents)

async def create_zabbix_session():
    zapi = AsyncZabbixAPI(ZABBIX_URL, validate_certs=False)
    await zapi.login(token=ZABBIX_TOKEN)
    return zapi

async def get_or_create_hostgroup(zapi, group_name):
    groups = await zapi.hostgroup.get({'filter': {'name': group_name}})
    if groups:
        return groups[0]['groupid']
    else:
        group = await zapi.hostgroup.create({'name': group_name})
        return group['groupids'][0]

def sanitize_name(name):
    return re.sub(r'\W+', '', name)

async def get_or_create_host(zapi, guild_name, channel_name, hostgroup_id):
    sanitized_guild_name = sanitize_name(guild_name)
    host_name = f"{sanitized_guild_name}-{channel_name}"
    hosts = await zapi.host.get({'filter': {'host': host_name}})
    if hosts:
        return hosts[0]['hostid']
    else:
        host = await zapi.host.create({
            'host': host_name,
            'interfaces': [{
                'type': 1,
                'main': 1,
                'useip': 1,
                'ip': '127.0.0.1',
                'dns': '',
                'port': '10050'
            }],
            'groups': [{'groupid': hostgroup_id}]
        })
        return host['hostids'][0]

async def get_or_create_item(zapi, host_id, item_name, key):
    items = await zapi.item.get(filter={'hostid': host_id, 'name': item_name})
    if items:
        return items[0]['itemid']
    item = await zapi.item.create({
        'name': item_name,
        'key_': key,
        'hostid': host_id,
        'type': 2,  # Zabbix trapper item
        'value_type': 3  # Numeric unsigned
    })
    return item['itemids'][0]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.zapi = await create_zabbix_session()
    bot.hostgroup_id = await get_or_create_hostgroup(bot.zapi, 'Discord channels')
    bot.data = {}  # Nested dictionary to store host, item, and value data
    for guild in bot.guilds:
        for channel in guild.text_channels:
            # Controleer of de host al bestaat, zo niet, maak deze aan
            host_id = await get_or_create_host(bot.zapi, guild.name, channel.name, bot.hostgroup_id)
            bot.data[channel.id] = {'host_id': host_id, 'items': {}}
            print(f'Host created or found for channel: {sanitize_name(guild.name)}-{channel.name}')

@bot.event
async def on_guild_channel_create(channel):
    if isinstance(channel, discord.TextChannel):
        host_id = await get_or_create_host(bot.zapi, channel.guild.name, channel.name, bot.hostgroup_id)
        bot.data[channel.id] = {'host_id': host_id, 'items': {}}
        print(f'Host created or found for new channel: {sanitize_name(channel.guild.name)}-{channel.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    channel_id = message.channel.id
    host_data = bot.data.get(channel_id)

    if host_data:
        host_id = host_data['host_id']
        items = host_data['items']

        # Voeg een item toe voor elke gebruiker in het kanaal
        item_key = f'message.count[{message.author.id}]'
        if item_key not in items:
            item_id = await get_or_create_item(bot.zapi, host_id, f'Message count for {message.author.name}', item_key)
            items[item_key] = {'item_id': item_id, 'count': 0}
            print(f'Item created or found for user: {message.author.name}')

            # Check if there is existing history for the item
            last_count = await bot.zapi.history.get({
                'itemids': item_id,
                'sortfield': 'clock',
                'sortorder': 'DESC',
                'limit': 1
            })
            items[item_key]['count'] = int(last_count[0]['value']) if last_count else 0

        # Verhoog de teller voor het aantal berichten
        items[item_key]['count'] += 1
        await bot.zapi.history.push({
            'itemid': items[item_key]['item_id'],
            'clock': int(message.created_at.timestamp()),
            'value': items[item_key]['count']
        })
        print(f'Count updated for user: {message.author.name}')

bot.run(DISCORD_TOKEN)
