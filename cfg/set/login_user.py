__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml

dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()

# Yml table for login user configuration.
yaml_data = \
    """---
    UserTable:
      set: system/login/user
      key-field:
        user
      view: userView
    userView:
      groups:
        auth: authentication
      fields:
        user: name
        uid: { uid : { 'type' : 'int', 'minValue' : 100, 'maxValue' : 64000 } }
        class_name: { class : { 'type' : { 'enum' : ['operator', 'read-only', 'super-user'] } } }
      fields_auth:
        password: encrypted-password
      """
globals().update(FactoryLoader().load(yaml.load(yaml_data)))

# Create object of UserTable
ut = UserTable(dev)

users = ['TestUser_1', 'TestUser_2']
identifiers = [1346, 1347]
passwds = ['AbcD', 'WxYz']

for usr, id, passwd in zip(users, identifiers, passwds):
    ut.user = usr
    ut.uid = id
    ut.class_name = 'read-only'
    ut.password = passwd
    # append record
    ut.append()

# Apply configuration in running db.
ut.set()

# Display login user configuration.
ut.get()
for item in ut:
    print 'name:', item.user
    print 'uid:', item.uid
    print 'class name:', item.class_name
    print ''

dev.close()

'''
# Configuration XML snippet used as reference to create UserTable table.

root@junos# show system login | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1I0/junos">
    <configuration junos:changed-seconds="1459278481" junos:changed-localtime="2016-03-29 15:08:01 EDT">
            <system>
                <login>
                    <user>
                        <name>TestUser_1</name>
                        <uid>1346</uid>
                        <class>read-only</class>
                        <authentication>
                            <encrypted-password>AbcD</encrypted-password>
                        </authentication>
                    </user>
                    <user>
                        <name>TestUser_2</name>
                        <uid>1347</uid>
                        <class>read-only</class>
                        <authentication>
                            <encrypted-password>WxYz</encrypted-password>
                        </authentication>
                    </user>
                </login>
            </system>
    </configuration>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
'''
