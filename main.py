import json
import os
import shutil
import requests
import getpass

username = getpass.getuser()
Setting_file = os.path.join('./config.json')
if os.path.isfile(Setting_file):
    with open(Setting_file) as f:
        print("Found config file")
        setting = json.loads(f.read())
        f.close()
else:
    print("Load default config")
    setting = {
        "VIA_PATH": "C:/Users/{username}/AppData/Roaming/VIA/config.json",
        "Custom_file_id": "1L4trzhGTBm6HB-hTqzm6R1EnXld1Edpi"
    }


def download_file_from_google_drive():
    url = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(url, params={'id': setting['Custom_file_id']}, stream=True)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print(response.status_code)
        return None


def main():
    try:
        custom_config = download_file_from_google_drive()
        if custom_config:
            try:
                via_path = setting["VIA_PATH"].format(username=username)
            except:
                via_path = setting["VIA_PATH"]
            via_file = os.path.join(via_path)
            exist = os.path.isfile(via_file)
            if not exist:
                print("Please check VIA_PATH")
            else:
                with open(via_file) as file:
                    config = json.loads(file.read())
                    file.close()
                for key, value in custom_config.items():
                    config["remoteData"]["definitions"][key] = value
                if os.path.isfile(f'{via_path}.bk'):
                    os.remove(f'{via_path}.bk')
                shutil.copyfile(via_path, f'{via_path}.bk')
                print("Wait to finish.....")
                with open(via_file, 'w') as file:
                    json.dump(config, file, indent='\t')
                    file.close()
                print("Finished")
        else:
            print("Fail")
    except Exception as e:
        print(e)
        print("Fail")
    os.system('pause')


if __name__ == '__main__':
    main()
