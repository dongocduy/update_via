import json
import os
import shutil
import requests


def download_file_from_google_drive():
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': '1L4trzhGTBm6HB-hTqzm6R1EnXld1Edpi'}, stream=True)
    return json.loads(response.content.decode('utf-8'))


def main():
    custom_config = download_file_from_google_drive()
    via_path = 'C:/Users/Dell/AppData/Roaming/VIA/config.json'
    via_file = os.path.join(via_path)
    exist = os.path.isfile(via_file)
    if not exist:
        print("not exist Via")
    else:
        with open(via_file) as f:
            config = json.loads(f.read())
            f.close()
        for key, value in custom_config.items():
            config["remoteData"]["definitions"][key] = value
        if os.path.isfile(f'{via_path}.bk'):
            os.remove(f'{via_path}.bk')
        shutil.copyfile(via_path, f'{via_path}.bk')
        print("Wait to finish.....")
        with open(via_path, 'w') as f:
            json.dump(config, f, indent='\t')
            f.close()
        print("Finished")


if __name__ == '__main__':
    main()
