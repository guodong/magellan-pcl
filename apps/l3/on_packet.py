
mac_to_port = {}  # learning mac_table
ip_to_mac = {}    # learning arp_table
port_port_to_path = {
  ('s1:1', 'r1:1'): ['s1:2'],
  ('s1:2', 'r1:1'): ['s1:1'],
  ('s2:1', 'r1:2'): ['s2:2'],
  ('s2:2', 'r1:2'): ['s2:1'],
  ('r1:1', 'h3:1'): ['r1:2', 's2:1'],
  ('r1:1', 'h4:1'): ['r1:2', 's2:2'],
  ('r1:2', 'h1:1'): ['r1:1', 's1:1'],
  ('r1:2', 'h2:1'): ['r1:1', 's1:2'],
}
subnet_to_port = {
  '10.0.0.1/24': 'r1:1',
  '192.168.1.1/24': 'r1:2'
}
STP = {
  's1:1': ['s1:2', 's1:3'],
  's1:2': ['s1:1', 's1:3'],
  's1:3': ['s1:1', 's1:2'],
  's2:1': ['s2:2', 's2:3'],
  's2:2': ['s2:1', 's2:3'],
  's2:3': ['s2:1', 's2:2']
}
ip_to_port = {
  '10.0.0.1': 'r1:1',
  '192.168.1.1': 'r1:2',
  '10.0.0.101': 'h1:1',
  '10.0.0.102': 'h2:1',
  '192.168.1.101': 'h3:1',
  '192.168.1.102': 'h4:1'
}

def on_packet(pkt, inport: 'l2'):
  mac_to_port.insert(pkt.eth.src, inport, 500) # mac, port, timeout
  if pkt.eth.dst in mac_to_port:
    return port_port_to_path[inport, mac_to_port[pkt.eth.dst]], pkt
  else:
    return STP[inport], pkt

def on_packet(pkt, inport: 'router'):
  if pkt.eth.type == 0x0806: # ARP packet
    handle_arp(pkt, inport) # offline
  elif pkt.eth.type == 0x0800:  # IPv4 packet
    port = subnet_to_port.lpm(pkt.ipv4.dst)
    if pkt.ipv4.dst in ip_to_mac:
      new_pkt = rewrite(pkt, {'eth.dst': ip_to_mac[pkt.ipv4.dst]})
      return port_port_to_path[port, ip_to_port[pkt.ipv4.dst]], new_pkt
    else:
      handle_ip_to_mac_miss(pkt, port)
  else:
    return DROP