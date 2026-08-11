from scapy.all import IP, TCP, Raw, wrpcap

packets = []

# Generate standard HTTP traffic
for i in range(5):
    pkt = IP(src="192.168.1.50", dst="142.250.190.46") / TCP(sport=50000+i, dport=443, flags="S")
    packets.append(pkt)

# Generate synthetic anomaly burst
for i in range(15):
    pkt = IP(src="10.0.0.88", dst="192.168.1.1") / TCP(sport=40000+i, dport=80, flags="S") / Raw(load="GET /admin HTTP/1.1\r\nHost: target\r\n\r\n")
    packets.append(pkt)

wrpcap("sample_traffic.pcap", packets)
print("[+] Successfully generated 'sample_traffic.pcap' with test network traffic.")
