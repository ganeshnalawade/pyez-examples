__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

# Connect to device.
dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()


'''
# Configuration XML snippet used as reference to create AutoSysTable table.

root@junos# show routing-options | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1I0/junos">
    <configuration junos:changed-seconds="1459272959" junos:changed-localtime="2016-03-29 13:35:59 EDT">
            <routing-options>
                <autonomous-system>
                    <as-number>100</as-number>
                </autonomous-system>
            </routing-options>
    </configuration>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
'''

# Yml table for autonomous-system configuration.
yaml_auto_data = \
    """---
  AutoSysTable:
    set: routing-options/autonomous-system
    key-field:
      - as_num
    view: AutoSysView

  AutoSysView:
    fields:
      as_num: as-number
   """

globals().update(FactoryLoader().load(yaml.load(yaml_auto_data)))

# Assign value to AutoSysTable field.
at = AutoSysTable(dev)
at.as_num = 100

# Apply configuration in running db.
at.set()

# Print configured autonomous-system value.
at_get = at.get()
for item in at_get:
    print 'as_num: ', item.as_num
    print ''


'''
# Configuration XML snippet used as reference to create BgpTable table.

root@junos# show protocols bgp | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1I0/junos">
    <configuration junos:changed-seconds="1459272959" junos:changed-localtime="2016-03-29 13:35:59 EDT">
            <protocols>
                <bgp>
                    <group>
                        <name>external_bgp</name>
                        <type>external</type>
                        <local-address>20.20.20.20</local-address>
                        <peer-as>200</peer-as>
                        <neighbor>
                            <name>30.30.10.10</name>
                        </neighbor>
                    </group>
                </bgp>
            </protocols>
    </configuration>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
'''

# Yml table for BGP configuration.
yaml_bgp_data = \
    """---
  BgpTable:
    set: protocols/bgp/group
    key-field:
      - bgp_name
    view: BgpView

  BgpView:
    groups:
      neigh : neighbor
    fields:
      bgp_name   : { 'name' : { 'type' : 'str', 'minValue' : 0, 'maxValue' : 255} }
      bgp_type   : {'type' : {'type': { 'enum': ['external', 'internal'] } } }
      local_addr : local-address
      peer       : { 'peer-as' : { 'type' : 'int' } }
    fields_neigh:
      neigh      : name
   """

globals().update(FactoryLoader().load(yaml.load(yaml_bgp_data)))

# Assign value to BgpTable field.
bgp = BgpTable(dev)
bgp.bgp_name = 'external_bgp'
bgp.bgp_type = 'external'
bgp.local_addr = '20.20.20.20'
bgp.peer = 200
bgp.neigh = '30.30.10.10'

# Apply configuration in running db.
bgp.set()

# Print configured BGP value.
bgp_get = bgp.get()
for item in bgp_get:
    print "bgp_name: ", item.bgp_name
    print "bgp_type: ", item.bgp_type
    print "local_addr: ", item.local_addr
    print "peer: ", item.peer
    print "neigh: ", item.neigh
    print ''
