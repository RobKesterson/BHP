import threading
import time
from netaddr import IPNetwork,IPAddress
--snip--

#host listen on
host = "192.168.0.187"

#subnet to target
subjet = "192.168.0.0/24"

#magic string we'll check ICMP requests for
magic_message = "PYTHONRULES!"

#this sprays out the UDP datagrams
def udp_sender(subnet,magic_message):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message,("%s" % ip,65212))
        except:
            pass
        
--snip--


#start sending packets
t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()

--snip--
try:
    while True:
        --snip--
        print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code)
        
        #now check for the Type 3 and CODE
        if icmp_header.code == 3 and icmp_header.type == 3:
                 
                 #make sure host is in our target subnet
                 if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                     
                     #make sure it has our magic message
                     if raw_buffer[len(raw_buffer)-len(magic_message):] == magic_message:
                         print "Host Up: %s" % ip_header.src_address