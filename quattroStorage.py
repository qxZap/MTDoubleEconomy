import os
import shutil
import subprocess
import json

BOOST = 4

def modifyDeliveryPoint(data):
    exports = data.get('Exports')
    for export_index in range(0,len(exports)):
        export_data = exports[export_index]['Data']
        if 'MissionPointType' in json.dumps(export_data):
            for line_index in range(0, len(export_data)):
                line_name = export_data[line_index]['Name']
                
                if line_name == 'MaxStorage':
                    data['Exports'][export_index]['Data'][line_index]['Value'] = data['Exports'][export_index]['Data'][line_index]['Value']*BOOST
                
                if line_name == 'StorageConfigs':
                    for storage_config in data['Exports'][export_index]['Data'][line_index]['Value']:
                        for line in storage_config["Value"]:
                            if line["Name"] == 'MaxStorage':
                                line["Value"] = line["Value"] * BOOST
            # TODO: fix MaxStorage from StorageConfig
    return data

# Paths
source_dir = '../Output/Exports/MotorTown/Content/Objects/Mission/Delivery/DeliveryPoint/'
delivery_point_dir = 'DeliveryPoint'

# Step 1: Create or clear DeliveryPoint folder
if os.path.exists(delivery_point_dir):
    shutil.rmtree(delivery_point_dir)
os.mkdir(delivery_point_dir)

# Step 2: List all .uasset files
uassets = [f for f in os.listdir(source_dir) if f.endswith('.uasset')]

# Step 3: Convert each .uasset to .json
for uasset in uassets:
    base_name = os.path.splitext(uasset)[0]
    input_path = os.path.join(source_dir, uasset)
    output_json = os.path.join(delivery_point_dir, base_name + '.json')

    command = [
        'UAssetGUI.exe',
        'tojson',
        input_path,
        output_json,
        'VER_UE5_5',
        'MotorTown718'
    ]

    subprocess.run(command, check=True)

# Step 4: Modify each .json
for file in os.listdir(delivery_point_dir):
    if not file.endswith('.json'):
        continue

    json_path = os.path.join(delivery_point_dir, file)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified_data = modifyDeliveryPoint(data)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(modified_data, f, indent=4)

print("quattroStorage.py finished successfully.")
