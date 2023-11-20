import urllib.request
import yaml
import argparse
def give_link(link):
    link_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    #chat gpt told me to do so, it defineds the web agent. some webs don't like pythons defult agent
    try:#if access denied or 404
            req = urllib.request.Request(link, headers=headers)
            response = urllib.request.urlopen(req)
            html_str = response.read().decode('utf-8')

            for i in range(len(html_str) - 6):
                if html_str[i:i + 6] == 'href="':
                    j = i + 6
                    curr_link = ""
                    if html_str[j:j+4] == 'http':
                        while html_str[j] != '"':
                            curr_link += html_str[j]
                            j+=1
                        link_list.append(curr_link)
            return (link_list)
    except:
        return []

def crawler(url, depth=2, mem=set()):
    links_yaml = open("links.yaml","w")
    def Crawler_rec(lst_url,depth_rec,d):
        if depth_rec==0:
            return
        lst_give_link_url=[]
        for url_link in lst_url:
            if url_link in mem:
                continue
            else:
                lst_give_link_url+=give_link(url_link)
                mem.add(url_link)
        yaml.dump({"level":d-depth_rec+1,"links":lst_give_link_url}, links_yaml)
        return Crawler_rec(lst_give_link_url,depth_rec-1,d)
    yaml.dump({"level":0,"links":url}, links_yaml)
    return (Crawler_rec([url],depth,depth))

parser = argparse.ArgumentParser(description='A simple program that uses command-line arguments.')
parser.add_argument('url', type=str, help='url to hey')
parser.add_argument('--depth', type=int, default=2, help='depth to dive in the links, default is 2')
args = parser.parse_args()
url = args.url
depth =args.depth

args = parser.parse_args()
url = args.url

crawler(url, depth)
