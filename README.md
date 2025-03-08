# A dicord bot to monitor your guild/server using Zabbix!

Install the requirements, build the config.json with your tokens and the IP of the zabbix server (DNS Somehow gives errors)
To get a token for discord, visit https://discord.com/developers and signup for a new application
In the menu, go to Bot to reset your token and get it.
Also make sure to enable the intents:
 - PRESENCE INTENT
 - SERVER MEMBERS INTENT
 - MESSAGE CONTENT INTENT

 Then go to Installation and copy the install link, paste in a new browserwindow and let it join the server you want.
 Start main.py (in a docker or wherever you can run it 24/7 with access to your zabbix server and internet)

 It will make a Hostgroup called "Discord channels" and add a host per channel.
 Every user will become an item the first time they send a messgage and it will be raised on every message.
 The bot will keep the count in memory to save on history get items, after a restart it will get the state from zabbix again on first message.
