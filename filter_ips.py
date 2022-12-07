import ipaddress
import argparse

def main():
    '''Remove private IPs from a list of IPs.'''
    # Get file path to list of IPs from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('iplist', help='Path to host IPs file')
    args = parser.parse_args()
    # Read in host ips file
    with open(args.iplist, 'r') as f:
        host_ips = f.readlines()

    # Overwrite the file with only public IPs
    with open(args.iplist, 'w') as f:
        for line in host_ips:
            if not ipaddress.ip_address(line.strip()).is_private:
                f.write(line)

if __name__ == '__main__':
    main()
