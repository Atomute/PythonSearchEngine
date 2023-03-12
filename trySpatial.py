from urllib.parse import urljoin,urlparse

parsed_uri = urlparse(" https://www.serebii.net/")
root = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
print(root)