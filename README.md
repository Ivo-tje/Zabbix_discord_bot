# A dicord bot to monitor your guild/server using Zabbix!

Install the requirements, build the config.json with your tokens and the IP of the zabbix server (DNS somehow gives errors)
To get a token for discord, visit https://discord.com/developers and signup for a new application
In the menu, go to Bot to reset your token and get it.
Also make sure to enable the intents:
 - PRESENCE INTENT
 - SERVER MEMBERS INTENT
 - MESSAGE CONTENT INTENT

 Then go to Installation and copy the install link, paste in a new browserwindow and let it join the server you want.
 Start main.py (in a docker or wherever you can run it 24/7 with access to your zabbix server and internet)

 It will make a Hostgroup called "Discord channels" and add a host per channel. (Guild - Channel)
 Every user will become an item the first time they send a messgage and it will be raised on every message.
 A second item wil sum the length of all messages together, so typing less but longer messages will be monitored!
 The bot will keep the ids and counts in memory to save on api calls to zabbix, after a restart it will get the data from zabbix again on first message.
