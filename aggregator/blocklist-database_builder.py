import yaml
import requests

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def process_blocklist_url(url, category, source):
    response = requests.get(url)
    for line in response.text.splitlines():
        url = extract_urls_from_line(line)
        if url:
            add_url(url, [category], [source])

def print_first_five_urls(url, category):
    response = requests.get(url)
    count = 0
    for line in response.text.splitlines():
        
        # First remove comments and empty lines
        if line.startswith('#'):
            continue
        if len(line) < 1:
            continue

        # Then remove things we don't need from the line
        count += 1
        if count > 4:
            break

if __name__ == "__main__":
    config = load_config('config.yaml')
    # print("doing stuff")
    # for category, urls in config['blocklists'].items():
    #     for url in urls:
    #         print(f"Processing {url} under category '{category}'")
    #         print_first_five_urls(url, category)

    urls = set()

    file = open("unprocessed.txt", "r")
    for line in file:

        if line.startswith('#') or len(line) < 2:
            continue

        if 'localhost' in line:
            continue

        # if line.startswith('127.0.0.1') or line.startswith('0.0.0.0'):
        #     line = line.split()[1]

        line = line.removeprefix('127.0.0.1 ')
        line = line.removeprefix('0.0.0.0')
        line = line.removesuffix('\n')
        line = line.removesuffix('^')
        line = line.removesuffix(' - Malware')
        line = line.removeprefix('127.0.0.1\t')
        line = line.removeprefix('0.0.0.0\t')

        if '#' in line:
            line = line.split('#')[0]

        
        urls.add(line)


    
    print(urls)