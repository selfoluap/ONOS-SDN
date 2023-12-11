#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, OVSController
# Traffic Control
from mininet.link import TCLink
import matplotlib.pyplot as plt

#change this to your remote controller ip
REMOTE_CONTROLLER_IP = "172.17.0.2"

def perfTest(num_hosts, test_with_remote_controller=True):
    # Create network and run simple performance test
    topo = SingleSwitchTopo(n=num_hosts)


    if test_with_remote_controller:
        print("Starting network with RemoteController at ", REMOTE_CONTROLLER_IP)
        net = Mininet(topo=topo, link=TCLink,
                    controller=lambda name: RemoteController(name, ip=REMOTE_CONTROLLER_IP, port=6633),
                    switch=OVSSwitch,
                    autoSetMacs=True)
    else:
        print("Starting network without ONOS")
        net = Mininet(topo=topo, link=TCLink, controller=OVSController)
    net.start()
    print("Testing bandwidth between first and last host")
    (server_speed, client_speed) = net.iperf()
    result = net.pingFull([net.hosts[0], net.hosts[num_hosts - 1]])
    avg_rtt = (result[0][2][3] + result[1][2][3])/2
    net.stop()
    return (server_speed, client_speed, avg_rtt, num_hosts)


class SingleSwitchTopo(Topo):
    # Single switch connected to n hosts
    def __init__(self, n=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1', protocols='OpenFlow14')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            # self.addLink(host, switch, bw=10, delay='5ms', loss=10)
            self.addLink(host, switch, bw=10)


topos = {'singleswitchtopo': (lambda: SingleSwitchTopo(n=4))}




def runTest(test_with_remote_controller=True):
    results = []
    number_of_hosts_range = [2, 4, 8, 16, 32]
    for number_of_hosts in number_of_hosts_range:
        server_speed, client_speed, avg_rtt, _ = perfTest(number_of_hosts, False)
        results.append((server_speed, client_speed, avg_rtt))

    server_speeds = [result[0] for result in results]
    client_speeds = [result[1] for result in results]
    avg_rtts = [result[2] for result in results]

    plt.figure(figsize=(10, 6))
    plt.plot(number_of_hosts_range, server_speeds, label="Server Speed")
    plt.plot(number_of_hosts_range, client_speeds, label="Client Speed")
    plt.xlabel("Number of Hosts")
    plt.ylabel("Performance (Mbps)")
    plt.title("Server and Client Performance vs. Number of Hosts")
    plt.legend()
    plt.grid(True)

    if test_with_remote_controller:
        plt.savefig("throughput_with_ONOS.png")
    else:
        plt.savefig("throughput_with_OVScontroller.png")

    plt.figure(figsize=(10, 6))
    plt.plot(number_of_hosts_range, avg_rtts, label="Average RTT")
    plt.xlabel("Number of Hosts")
    plt.ylabel("Average RTT (ms)")
    plt.title("Average RTT vs. Number of Hosts")
    plt.legend()
    plt.grid(True)

    if test_with_remote_controller:
        plt.savefig("rtt_with_ONOS.png")
    else:
        plt.savefig("rtt_with_OVScontroller.png")

if __name__ == '__main__':
    runTest(test_with_remote_controller=True)
    #runTest(test_with_remote_controller=False)