import urllib.request
import yaml
import argparse
def give_link(link):
    return_link_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    #chat gpt told me to do so, it defineds the agent. some webs don't like pythons defult agent
    try: #if access denied or 404
            req = urllib.request.Request(link, headers=headers)
            response = urllib.request.urlopen(req)
            text_str = response.read().decode('utf-8')

#create the home link. maybe the link on the page doesnt start with "http...", so we can to add it for the link
            if link[-1] != "/":
                link += "/"
            home_link = "https://"
            for i in link[8:]: #whith out the "https://
                if i != "/": #the end of the home page
                    home_link += i
                else:
                    break

            for i in range(len(text_str) - 6):
                if text_str[i:i + 6] == 'href="':
                    j = i + 6
                    now_link = ""

#get the link
                    while text_str[j] != '"':
                        now_link += text_str[j]
                        j += 1
#check if its a legal link
                    if now_link[0:4] == 'http':
                        return_link_list.append(now_link)
                    elif now_link[0] == "/": #check if its even link or not
                        return_link_list.append(home_link + now_link)

            return (return_link_list)
    except:
        return ["No access"]

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
