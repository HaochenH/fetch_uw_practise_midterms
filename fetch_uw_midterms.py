import httpx
import lxml.html
from rich import print
import re
import platform
import os

# url = "https://sites.math.washington.edu/~m208/Midterm1.php"
url = input("Input url: ")

parent_output_dir = os.path.expanduser('~/Downloads')
p = os.path.dirname(url).split('/')[-1].replace('~', '')
output_dir = os.path.join(parent_output_dir, p)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print('{} created'.format(output_dir))

res = httpx.get(url)

# convert html string into an etree
tree = lxml.html.fromstring(res.text)
print(type(tree)) # <class 'lxml.html.HtmlElement'>

# base_url = re.findall(r'(.*?:\/\/.*?)\/', url)[0]
url_path = os.path.dirname(url)
print(url_path)

a_texts = tree.xpath('//table//a/text()')
links = [url_path + l[1:] for l in tree.xpath('//table//a/@href')]
print(f'A text found: {a_texts}')
print('links found:')
print(links)

lcoal_paths = []
for link in links:
    res = httpx.get(link)
    filename = link.split('/')[-1]
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        size = f.write(res.content)
        print("{} bytes written to \"{}\"".format(size, filepath))
    lcoal_paths.append(filepath)

if platform.system() == 'Darwin':
    os.system('open "{}"'.format(output_dir))
elif platform.system() == 'Windows':
    os.system('explorer "{}"'.format(output_dir))