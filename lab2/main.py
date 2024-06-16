import subprocess
import argparse
import socket


def find_min_mtu(destination, max_mtu=10000):
    mtu_bin_pow = 20
    min_mtu = 0
    while mtu_bin_pow >= 0:
        min_mtu += 2 ** mtu_bin_pow
        if min_mtu > max_mtu:
            min_mtu -= 2 ** mtu_bin_pow
            mtu_bin_pow -= 1
            continue
        cmd = ['ping', '-c', '1', '-M', 'do', '-s', str(min_mtu), destination]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if "100% packet loss" in result.stdout.decode() or "Message too long" in result.stderr.decode():
                min_mtu -= 2 ** mtu_bin_pow
            if "Unreachable" in result.stdout.decode() or "Unreachable" in  result.stderr.decode():
                print("Destination is not reachable or incorrect.")
                return None
            mtu_bin_pow -= 1
        except Exception as e:
            print(f"Error: {e}")
            return None

    if min_mtu == 0:
        print("ICMP is blocked.")
        return None
    return min_mtu + 28


def main():
    parser = argparse.ArgumentParser(description='Find minimum MTU.')
    parser.add_argument('destination', help='Destination address.')

    try:
        args = parser.parse_args()
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to parse arguments")

    try:
        socket.gethostbyname(args.destination)
    except socket.error:
        print("Destination is not reachable or incorrect.")
        return

    min_mtu = find_min_mtu(args.destination)

    if min_mtu:
        print(f"The minimum MTU to {args.destination} is {min_mtu} bytes.")
    else:
        print("Failed to determine the minimum MTU.")


if __name__ == "__main__":
    main()
