__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

# Connect to device.
dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()

# Yml table for interface configuration.
yaml_data = \
    """---
  InterfaceTable:
    set: interfaces/interface
    key-field:
      - name
    view: InterfaceView

  InterfaceView:
    groups:
      unit: unit
      bridge: unit/family/bridge
    fields:
      name: name
      native_vlan: native-vlan-id
    fields_unit:
      unit_name  : { 'name' : { 'default' : 0 } }
      desc       : description
    fields_bridge:
      mode: interface-mode
      vlan_list: vlan-id-list
   """

globals().update(FactoryLoader().load(yaml.load(yaml_data)))

intf = InterfaceTable(dev)

intf.name = "ge-1/1/8"
intf.mode = "trunk"
intf.vlan_list = [510, 520, 530]
intf.native_vlan = 510
intf.desc = "l2-interface created"

intf.lock()
intf.load()

if intf.commit_check():
   intf.commit(sync=True)
else:
   intf.rollback()

intf.unlock()

int = intf.get()
for item in int:
    print 'name: ', item.name
    print 'unit_name: ', item.unit_name
    print 'vlan_list: ', item.vlan_list
    print 'mode: ', item.mode
    print 'native_vlan: ', item.native_vlan
    print 'description: ', item.desc
    print ''

dev.close()

'''
# Configuration XML snippet used as reference to create InterfaceTable table.

root@junos# show interfaces ge-1/1/8 | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1I0/junos">
    <configuration junos:changed-seconds="1459279689" junos:changed-localtime="2016-03-29 15:28:09 EDT">
            <interfaces>
                <interface>
                    <name>ge-1/1/8</name>
                    <native-vlan-id>510</native-vlan-id>
                    <unit>
                        <name>0</name>
                        <description>l2-interface created</description>
                        <family>
                            <bridge>
                                <interface-mode>trunk</interface-mode>
                                <vlan-id-list>510</vlan-id-list>
                                <vlan-id-list>520</vlan-id-list>
                                <vlan-id-list>530</vlan-id-list>
                            </bridge>
                        </family>
                    </unit>
                </interface>
            </interfaces>
    </configuration>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
'''
