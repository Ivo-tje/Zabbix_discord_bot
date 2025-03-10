## Creating a dashboard

Add a new dashboard, add a host navigator for Host group "Discord channels", name it "Guild - Channel"
Add a item navigator for the same hostgroup, for the hosts select the Host navigator (Guild - Channel) we just made. Name it "Users".

Add a graph, remove the default dataset, add a new dataset as Item list and point it to the item navigator (Users).
I used the line color #0080FF, line widht 2, missing data "connected" and selected Staircase, but feel free to use your own settings!

I also added 2 honeycombs.
The first:
 - Name: Message count
 - Hostgroup: Discord Channels
 - Hosts: widget -> Guild - Channel
 - Item Patern: Message count *
 - Advanced configuration > Primary label > Text: {{ITEM.NAME}.regrepl("Message count for", "")}

The second:
 - Name: Message length
 - Hostgroup: Discord Channels
 - Hosts: widget -> Guild - Channel
 - Item Patern: Message length *
 - Advanced configuration > Primary label > Text: {{ITEM.NAME}.regrepl("Message length for", "")}

[image/Dashboard.png]
