import urllib.request
from urllib.parse import urlparse
def get_IP():
    ip_url = "https://api.ipify.org"
    ip_response = urllib.request.urlopen(ip_url)
    ip_data = ip_response.read()
    return ip_data.decode('utf-8')
print(get_IP())
