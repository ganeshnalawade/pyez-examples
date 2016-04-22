__author__ = 'gnalawade'

from jnpr.junos import Device
from jnpr.junos.resources.staticroutes import StaticRouteTable

dev = Device('xxxx', user='xxxx', password='xxxx')
dev.open()

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

    srt.get()
    for item in srt:
        print 'route_name: ', item.route_name
        print 'hop: ', item.hop
        print
