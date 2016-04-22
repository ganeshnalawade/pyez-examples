__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.resources.autosys import AutoSysTable
from jnpr.junos.resources.bgp import BgpTable
from jnpr.junos.factory.cfgtable import CfgTable

# Connect to device.
dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()

# Assign value to AutoSysTable field.
at = AutoSysTable(dev)
at.as_num = 100

# append record
at.append()

# Apply configuration in running db.
at.set()
print dir(at)
print at._AutoSysTable___isfrozen
# Print configured autonomous-system value.
at_get = at.get()
for item in at_get:
    print 'as_num: ', item.as_num
    print ''

# Assign value to BgpTable field.
bgp = BgpTable(dev)
bgp.bgp_name = 'external_bgp'
bgp.bgp_type = 'external'
bgp.local_addr = '20.20.20.20'
bgp.peer = 200
bgp.neigh_addr = '30.30.10.10'

# append record
bgp.append()

# Apply configuration in running db.
bgp.set()

# Print configured BGP value.
bgp_get = bgp.get()
for item in bgp_get:
    print "bgp_name: ", item.bgp_name
    print "bgp_type: ", item.bgp_type
    print "local_addr: ", item.local_addr
    print "peer: ", item.peer
    print "neigh: ", item.neigh_addr
    print ''


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
