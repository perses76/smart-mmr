import os
import shutil
import yaml
import glom


PROJECT_FOLDER = os.path.join(os.path.dirname(__file__), "mmr")

def main():
    #convert_booking_channels()
    convert_data(
        input_data="airlines.yml",
        output_folder="airline",
        items_selector=lambda data: data['items'],
        key_selector=lambda item: item['id'],
        spec={
            'key': 'id',
            'name': 'name'
        }
    )


def convert_data(input_data, output_folder, items_selector, key_selector, spec):
    with open(os.path.join(PROJECT_FOLDER,  input_data)) as f:
        data = yaml.load(f.read())

    items_folder = os.path.join(PROJECT_FOLDER, output_folder)
    if os.path.exists(items_folder):
        shutil.rmtree(items_folder)
    os.mkdir(items_folder)

    for item in items_selector(data):
        key = key_selector(item)
        path = os.path.join(items_folder, f"{key}.yml")
        with open(path, 'w') as f:
            f.write(yaml.dump(
                glom.glom(item, spec),
                default_flow_style=False
            ))


def convert_booking_channels():
    with open(os.path.join(PROJECT_FOLDER, 'booking_channels.yml')) as f:
        data = yaml.load(f.read())

    items_folder = os.path.join(PROJECT_FOLDER, 'booking_channel')
    if os.path.exists(items_folder):
        shutil.rmtree(items_folder)
    os.mkdir(items_folder)

    for item in data['items']:
        key = item['id']
        path = os.path.join(items_folder, f"{key}.yml")
        with open(path, 'w') as f:
            f.write(yaml.dump({
                "code": item["id"],
                "name": item["name"],
            }, default_flow_style=False))

main()
