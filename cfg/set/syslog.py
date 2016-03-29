__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
import yaml
from lxml import etree

dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()

# Yml table for syslog configuration.
yaml_data = \
    """---
  SyslogTable:
    set: system/syslog/file
    key-field:
      - name
      - contents_name
    view: SyslogView

  SyslogView:
    groups:
      contents: contents
    fields:
      name : { 'name' : { 'default' : 'messages' } }
    fields_contents:
      info           : info
      contents_name  : name
      error          : error
   """

globals().update(FactoryLoader().load(yaml.load(yaml_data)))

sys = SyslogTable(dev)

# Assign value to SyslogTable field.
sys.name = 'message_3'
sys.contents_name = "any"
sys.error = ''

# Add previous fields xpath-value pair (1st record) to
# configuration xml.
sys.append

# 2nd record.
sys.name = "message_3"
sys.contents_name = "authorization"
sys.info = ''

# 3rd record.
sys.append

sys['name'] = "message_4"
sys['contents_name'] = "authorization"
sys['info'] = ''

# Apply configuration in candidate db.
sys.load()
print sys.pdiff()

# Commit configuration.
if sys.commit_check():
   sys.commit()
else:
   sys.rollback()

# Display syslog configuration.
cnf_filter = \
'''
<configuration>
    <system>
        <syslog>
            <file>
            </file>
        </syslog>
    </system>
</configuration>
'''
cnf = dev.rpc.get_config(filter_xml=etree.XML(cnf_filter))
print etree.tostring(cnf)

dev.close()

'''
# Configuration XML snippet used as reference to create SyslogTable table.

root@junos# show system syslog | display xml
<rpc-reply xmlns:junos="http://xml.juniper.net/junos/16.1I0/junos">
    <configuration junos:changed-seconds="1459276655" junos:changed-localtime="2016-03-29 14:37:35 EDT">
            <system>
                <syslog>
                    <file>
                        <name>message_3</name>
                        <contents>
                            <name>any</name>
                            <error/>
                        </contents>
                        <contents>
                            <name>authorization</name>
                            <info/>
                        </contents>
                    </file>
                    <file>
                        <name>message_4</name>
                        <contents>
                            <name>authorization</name>
                            <info/>
                        </contents>
                    </file>
                </syslog>
            </system>
    </configuration>
    <cli>
        <banner>[edit]</banner>
    </cli>
</rpc-reply>
'''
