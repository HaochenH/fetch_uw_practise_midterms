import httpx
import lxml.html
import sys
import platform
import os

if len(sys.argv) > 1: # accept url as terminal parameter
    print('URL Received: {}'.format(sys.argv[1]))
    url = sys.argv[1]
else:
    url = input("Input url here\n(default: https://sites.math.washington.edu/~m208/Midterm1.php):\n>>> ")
if not url or not url.startswith('http'):
    url = "https://sites.math.washington.edu/~m208/Midterm1.php"

def output_dir(url):
    parent_output_dir = os.getcwd() # current working directory
    p = os.path.dirname(url).split('/')[-1].replace('~', '')
    output_dir = os.path.join(parent_output_dir, p)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print('{} created'.format(output_dir))
    return output_dir

def find_links(url):
    res = httpx.get(url)
    tree = lxml.html.fromstring(res.text) # convert html string into an etree
    url_path = os.path.dirname(url)
    print(f'URL path: {url_path}')
    print(f'Text found: {tree.xpath("//table//a/text()")}')
    links = [url_path + l[1:] for l in tree.xpath('//table//a/@href')]
    return links

def save_files(links, output_dir):
    local_paths = []
    for link in links:
        res = httpx.get(link)
        filename = link.split('/')[-1]
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            size = f.write(res.content)
            print('{} bytes written to "{}"'.format(size, filepath))
        local_paths.append(filepath)
    return local_paths

def open_dir(path):
    if platform.system() == 'Darwin':
        os.system('open "{}"'.format(path))
    elif platform.system() == 'Windows':
        os.system('explorer "{}"'.format(path))
    elif platform.system() == 'Linux':
        os.system('xdg-open "{}"'.format(path))
        
output_dir = output_dir(url)
links = find_links(url)
save_files(links, output_dir)
open_dir(output_dir)