import requests
from bs4 import BeautifulSoup
from pathlib import Path

USER_FOLDER = str(Path.home()).replace("\\", "/")
MOD_DIR = f"{USER_FOLDER}/AppData/Roaming/.minecraft/mods"
FABRIC = "fabric"
FORGE = "forge"

def get_mods(s_collection, s_loader, s_version, output_dir=MOD_DIR):
    content = requests.get(s_collection).content
    parsed_html = BeautifulSoup(content, features="html.parser")
    articles = parsed_html.body.find_all('article')
    mods = [article.find('a', class_="icon").attrs['href'].split('/mod/')[1] for article in articles]
    print(mods)
    for mod in mods:
        url = f"https://api.modrinth.com/v2/project/{mod}/version"
        versions = [v['files'][0] for v in requests.get(url).json() if s_version in v['game_versions'] and s_loader in v['loaders']]
        if len(versions) == 0:
            print(f"Could not find any matching version for project '{mod}'")
            continue
        f_name = versions[0]['filename']
        f_url = versions[0]['url']
        print(f"  Downloading '{f_url}'")
        data = requests.get(f_url).content
        with open(f"{output_dir}/{f_name}", "wb") as f:
            f.write(data)
            
if __name__ == "__main__":
    get_mods("https://modrinth.com/collection/P4AzVo8X", FABRIC, "1.21.4")