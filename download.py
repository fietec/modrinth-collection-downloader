import requests
from bs4 import BeautifulSoup
from pathlib import Path

USER_FOLDER = str(Path.home()).replace("\\", "/")
MOD_DIR = f"{USER_FOLDER}/AppData/Roaming/.minecraft/mods"
FABRIC = "fabric"
FORGE = "forge"

def _get_project(id:str):
    return (id, requests.get(f"https://api.modrinth.com/v2/project/{id}").json()["title"])

def get_mods(collection_path, s_loader, s_version, output_dir=MOD_DIR):
    print("Searching for projects in collection..")
    content = requests.get(collection_path).content
    parsed_html = BeautifulSoup(content, features="html.parser")
    articles = parsed_html.body.find_all('article')
    mods = [_get_project(article.find('a', class_="icon").attrs['href'].split('/mod/')[1]) for article in articles]
    if len(mods) == 0:
        print(f"[ERROR] Could not find any projects for '{collection_path}'! Please check whether this is a valid collection link.")
        return
    print(f"Found projects ({len(mods)}):")
    for mod in mods:
        print(f"  - {mod[1]}")
    if not input("Continue? (y/n): ").startswith("y"):
        print("Interrupted.")
        return
    for mod in mods:
        print(f"Looking for versions of project '{mod[1]}'({mod[0]}) for {s_loader} {s_version}..")
        url = f"https://api.modrinth.com/v2/project/{mod[0]}/version"
        versions = [v['files'][0] for v in requests.get(url).json() if s_version in v['game_versions'] and s_loader in v['loaders']]
        if len(versions) == 0:
            print(f"  [ERROR] Could not find any matching version!")
            continue
        f_name = versions[0]['filename']
        f_url = versions[0]['url']
        print(f"  Downloading '{f_url}'..")
        data = requests.get(f_url).content
        output_name = f"{output_dir}/{f_name}"
        print(f"  Saving '{output_name}'..")
        with open(output_name, "wb") as f:
            f.write(data)
            
    print("Finished!")
            
if __name__ == "__main__":
    get_mods("https://modrinth.com/collection/P4AzVo8X", FABRIC, "1.21.5")