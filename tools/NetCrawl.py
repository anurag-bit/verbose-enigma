import optparse
from dataclasses import dataclass
from typing import List, Dict

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


@dataclass
class ScapyResult:
    ip: str
    mac: str


@dataclass
class NetworkMap:
    network: str
    results: List[ScapyResult]

    def to_dict(self) -> Dict[str, List[Dict[str, str]]]:
        return {
            self.network: [{'ip': result.ip, 'mac': result.mac} for result in self.results]
        }


class NetworkScanner:
    def __init__(self, network):
        self.network = network

    def scan(self):
        arp_request = ARP(pdst=self.network)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        clients_list = []
        for sent, received in answered_list:
            clients_list.append(ScapyResult(ip=received.psrc, mac=received.hwsrc))

        return NetworkMap(network=self.network, results=clients_list)

    @staticmethod
    def print_result(network_map: NetworkMap):
        print("IP\t\t\tMAC Address")
        print("-----------------------------------------")
        for result in network_map.results:
            print(result.ip + "\t\t" + result.mac)


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-n", "--network", dest="network", help="Network range to scan")
    (options, arguments) = parser.parse_args()
    if not options.network:
        parser.error("[-] Please specify a network range, use --help for more info.")
    return options


options = get_arguments()
scanner = NetworkScanner(options.network)
network_map = scanner.scan()
scanner.print_result(network_map)
