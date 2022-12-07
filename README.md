# geolocate-pcap-hosts

## Description
Command line utility to create a GeoJSON-formatted world map of geolocated hosts from a network packet capture. The output json data can be visualized in another tool (e.g. pasted into https://geojson.io/).  
Run it on Linux, Mac, or WSL.

## Prerequisites
- Dependencies:
    - [curl](https://curl.se/)
    - [tshark](https://tshark.dev/)
    - [python3](https://www.python.org/)
- Get an account on [ipinfo.io](https://ipinfo.io/) (the free tier is fine)

## Setup
```bash
git clone https://github.com/wigginno/geolocate-pcap-hosts.git
cd geolocate-pcap-hosts
chmod +x geolocate_pcap.sh
# OPTIONAL - add your ipinfo.io api token to a text file (otherwise you'll be prompted for it):
echo [your_token] > api_token.txt
```

## Usage
**Basic usage**: `geolocate_pcap.sh [path_to_pcap]`  
<br>
**Example - Create a GeoJSON-formatted hosts map**:
```bash
$ # let's execute the script from another working directory and redirect stdout to a json file
$ ~/repos/geolocate-pcap-hosts/geolocate_pcap.sh cap1.pcapng > host_map.json
```
