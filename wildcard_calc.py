import itertools
from ipaddress import NetmaskValueError
import ipaddress
import argparse


MAX_DONT_CARE_BITS = 8


def acl_with_wildcard_to_netmasks(address_str: str, wildcard_str: str):
    """
    Translates an ACL (address, wildcard) to a list of ip_network objects (address, netmask)
    :param address_str: IP address string (v4 or v6)
    :param wildcard_str: wildcard mask (v4 or v6)
    :return: list of IP networks

    E.G for address="172.18.161.2" and wildcard "0.1.2.7"
    it returns:
        [IPv4Network('172.18.161.0/29'), IPv4Network('172.18.163.0/29'),
        IPv4Network('172.19.161.0/29'), IPv4Network('172.19.163.0/29')]
    """

    ip_addr = ipaddress.ip_address(address_str)
    wildcard = ipaddress.ip_address(wildcard_str)

    if wildcard.version != ip_addr.version:
        raise ValueError(f"IP version mismtach: address_str({address_str}), wildcard_str({wildcard_str})")

    # default values for v4
    _length = ipaddress.IPV4LENGTH
    _net_cls = ipaddress.IPv4Network
    if wildcard.version == 6:
        # values for v6
        _length = ipaddress.IPV6LENGTH
        _net_cls = ipaddress.IPv6Network

    mask_bits = [int(b) for b in format(int(wildcard), F"0{_length}b")]

    # We keep count of zero bits position (left-most is 0)
    dont_care_bits_index = [i for i, e in enumerate(reversed(mask_bits)) if e == 1]

    # We count how many contiguous zeros are from left-most bit, and we will mask them with a netmask
    hostmask_length = 0
    for (pos, bit) in enumerate(dont_care_bits_index):
        if pos != bit:
            break
        hostmask_length += 1

    # We only keep the bits that can't be dealt with by a netmask and need to be expanded to cartesian product
    dont_care_to_expand_index = dont_care_bits_index[hostmask_length:]

    # reverse in order to have the final loop iterate last through high order bits
    dont_care_to_expand_index.reverse()

    if len(dont_care_to_expand_index) > MAX_DONT_CARE_BITS:
        raise NetmaskValueError(f"{wildcard_str} contains more than {MAX_DONT_CARE_BITS} non-contiguous wildcard bits")

    ip_int_original = int(ip_addr)
    subnets = []
    for bits_values in itertools.product((0,1), repeat=len(dont_care_to_expand_index)):
        # enforce the bits_values in the IP address
        ip_int = ip_int_original
        for (index, val) in zip(dont_care_to_expand_index, bits_values):
            sb_mask = 1 << index
            if val:
                ip_int |= sb_mask
            else:
                ip_int &= ~sb_mask

        subnets.append(_net_cls((ip_int, _length-hostmask_length), strict=False))

    return subnets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", 
        "--address", 
        help="Address part of the statement, eg. 192.168.1.0", 
        dest="address",
        required=True,
        type=str
    )
    parser.add_argument(
        "-w", 
        "--wildcard", 
        help="Wildcard mask, eg. 0.0.0.255", 
        dest="wildcard",
        required=True,
        type=str
    )
    parser.add_argument(
        "-n",
        "--netmask",
        action="store_true",
        dest="netmask",
        help="Show ",
        required=False,
        default=False
    )
    arguments = parser.parse_args()
    
    print("\nAddress: '{}' Wildcard: '{}'".format(arguments.address, arguments.wildcard))
    results = acl_with_wildcard_to_netmasks(address_str=arguments.address, wildcard_str=arguments.wildcard)
    for result in results:
        if arguments.netmask:
            print(result.with_netmask)
        else:
            print(result.with_prefixlen)

if __name__ == '__main__':
    main()
