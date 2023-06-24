import sys
from scapy.all import *

def traceroute(destination):
    # Set the destination IP address
    dest_ip = destination
    foundDestination = False
    # Set the maximum number of hops
    max_hops = 30

    # Perform the traceroute
    for ttl in range(1, max_hops + 1):
        # Create the IP packet with increasing TTL
        packet = IP(dst=dest_ip, ttl=ttl) / ICMP()

        # Send the packet and receive the response
        reply = sr1(packet, verbose=False, timeout=2)

        # If no response received, print timeout message and continue to the next hop
        if reply is None:
            print(f"{ttl}. * * *")
            continue

        # If the response is an ICMP Time Exceeded message, print the hop IP address and RTT
        if reply.type == 11 and reply.code == 0:
            hop_ip = reply.src
            rtt = reply.time - packet.sent_time
            print(f"{ttl}. {hop_ip} {round(rtt * 1000, 2)} ms")

            # If the destination IP address is reached, stop the traceroute
            if hop_ip == dest_ip:
                foundDestination = True
                break

        # If the response is an ICMP Echo Reply, print the hop IP address and RTT
        elif reply.type == 0:
            hop_ip = reply.src
            rtt = reply.time - packet.sent_time
            print(f"{ttl}. {hop_ip} {round(rtt * 1000, 2)} ms")
            foundDestination = True
            break

        # If the response is neither Time Exceeded nor Echo Reply, print an error message
        else:
            print(f"{ttl}. Unknown response: {reply.summary()}")
            foundDestination = True
            break
    #let the user know if it worked
    if not foundDestination:
        print("Destination not found within 30 hops")
    else:
        print("Traceroute completed")

if __name__ == '__main__':
    traceroute(sys.argv[1])
