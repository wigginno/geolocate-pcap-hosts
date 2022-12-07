#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ $# -ne 1 || $1 == '-h' ]] ; then
    echo 'Usage:' >/dev/tty
    echo '  geolocate_pcap.sh [path_to_pcap]' >/dev/tty
    echo 'Example usage with output redirection to a json file (GeoJSON map):' >/dev/tty
    echo "  ~/repos/geolocate-pcap-hosts/geolocate_pcap.sh cap1.pcapng > host_map.json" >/dev/tty
    exit 0
fi

# Extract the IP addresses from the pcap file
PCAP_FILE=$1
tshark -nr "$PCAP_FILE" -T fields -e ip.src -e ip.dst -E separator=$'\n' | tr , '\n' \
    | awk NF | sort | uniq > "${SCRIPT_DIR}/host_ips"

# Filter out private IP addresses
python3 "${SCRIPT_DIR}/filter_ips.py" "${SCRIPT_DIR}/host_ips"

# Clear ip_geo_data if it exists
: > "${SCRIPT_DIR}/ip_geo_data"

# Get ipinfo.io token
if [ ! -f "$SCRIPT_DIR/api_token.txt" ]
then
    echo -n "Enter your ipinfo.io api token: " >/dev/tty
    read token
else
    token=$(cat $SCRIPT_DIR/api_token.txt)
fi

# Loop through host_ips and request geolocation data from ipinfo.io
while read ip; do
    # Suppress stderr to hide curl progress output
    exec 3>&2
    exec 2> /dev/null
    curl ipinfo.io/${ip}?token=${token} | tr -d '\n' >> "${SCRIPT_DIR}/ip_geo_data"
    exec 2>&3
    echo >> ip_geo_data
done < host_ips

# Convert the geolocation data to a GeoJSON multipoint map
python3 "${SCRIPT_DIR}/map_hosts.py" "${SCRIPT_DIR}/ip_geo_data"

echo "Writing map data..." >/dev/tty

# Write out the GeoJSON map and delete the temporary files
echo $(cat "${SCRIPT_DIR}/hosts_map.json")

rm "${SCRIPT_DIR}/host_ips"
rm "${SCRIPT_DIR}/ip_geo_data"
rm "${SCRIPT_DIR}/hosts_map.json"

echo "Done! You can view the map in a browser at https://geojson.io/" >/dev/tty
