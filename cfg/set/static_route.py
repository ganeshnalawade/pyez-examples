__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()

# Yml table for static route configuration.
yaml_data = \
    """---
    StaticRouteTable:
      set: routing-options/static/route
      key-field:
        - route_name
      view: StaticRouteView
    StaticRouteView:
      fields:
        route_name: name
        hop: next-hop
    """
globals().update(FactoryLoader().load(yaml.load(yaml_data)))

with StaticRouteTable(dev, mode='exclusive') as srt:
    # Assign value to table fields
    srt.route_name = '192.168.47.0'
    srt.hop = '172.16.1.2'
    srt.append()           # append 1st record

    srt.route_name = '192.168.48.0'
    srt.hop = '172.16.1.3'
    srt.append()           # append 2nd record

    srt.load()
    print srt.diff()
    srt.commit()


'''
# Configuration XML snippet used as reference to create StaticRouteTable table.

root@junos# show routing-options static | display xml 
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1I0/junos">
    <configuration junos:changed-seconds="1459450525" junos:changed-localtime="2016-03-31 14:55:25 EDT">
            <routing-options>
                <static>
                    <route>
                        <name>192.168.47.0/32</name>
                        <next-hop>172.16.1.2</next-hop>
                    </route>
                    <route>
                        <name>192.168.48.0/32</name>
                        <next-hop>172.16.1.3</next-hop>
                    </route>
                </static>
            </routing-options>
    </configuration>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
'''
