import os
import shutil
import subprocess
import json

BOOST = 10

# One place for the tool and the mappings, used for BOTH directions.
#
# What was wrong: quattroStorage.py read the assets with MotorTown719 and
# quattroConvert.bat wrote them back with MotorTown718. Unversioned properties
# are stored by schema position with no names in the file, so reading against one
# schema and writing against another shifts every property along -- that is the
# corrupt data. These assets really did change: BurgerCounter parses to 175KB
# under 719 and 150KB under 718.
#
# The local UAssetGUI.exe is v1.0.4 and writes an older JSON schema, which the
# game also rejects. D:\MT\UAssetGUI.exe is v1.1.1.
UASSETGUI = r'D:\MT\UAssetGUI.exe'
MAPPINGS = 'MotorTown719'
ENGINE_VERSION = 'VER_UE5_4'

FAILED_LOG = 'quattro_failed.log'


def uassetgui(*args):
    """UAssetGUI is a WinForms app: it exits 0 whether or not it wrote anything,
    so the only reliable success check is the output file existing."""
    subprocess.run([UASSETGUI, *args], check=True)


def to_json(uasset_path, json_path):
    if os.path.exists(json_path):
        os.remove(json_path)
    uassetgui('tojson', uasset_path, json_path, ENGINE_VERSION, MAPPINGS)
    return os.path.exists(json_path)


def from_json(json_path, uasset_path):
    for stale in (uasset_path, uasset_path.replace('.uasset', '.uexp')):
        if os.path.exists(stale):
            os.remove(stale)
    uassetgui('fromjson', json_path, uasset_path, MAPPINGS)
    return os.path.exists(uasset_path)


def modifyDeliveryPoint(data):
    boosted = 0
    exports = data.get('Exports')
    for export_index in range(0, len(exports)):
        export_data = exports[export_index]['Data']
        # A RawExport's Data is a base64 string, not a property list -- it means
        # that export did not parse, and indexing it would blow up.
        if not isinstance(export_data, list):
            continue
        if 'MissionPointType' in json.dumps(export_data):
            for line_index in range(0, len(export_data)):
                line_name = export_data[line_index]['Name']

                if line_name == 'MaxStorage':
                    value = data['Exports'][export_index]['Data'][line_index]['Value']
                    if isinstance(value, (int, float)):
                        data['Exports'][export_index]['Data'][line_index]['Value'] = value * BOOST
                        boosted += 1

                if line_name == 'StorageConfigs':
                    for storage_config in data['Exports'][export_index]['Data'][line_index]['Value']:
                        for line in storage_config["Value"]:
                            if line["Name"] == 'MaxStorage' and isinstance(line["Value"], (int, float)):
                                line["Value"] = line["Value"] * BOOST
                                boosted += 1
    return data, boosted


# Paths
source_dir = '../Output/Exports/MotorTown/Content/Objects/Mission/Delivery/DeliveryPoint/'
delivery_point_dir = 'DeliveryPoint'

# Step 1: Create or clear DeliveryPoint folder
if os.path.exists(delivery_point_dir):
    shutil.rmtree(delivery_point_dir)
os.mkdir(delivery_point_dir)

# Step 2: List all .uasset files
uassets = [f for f in os.listdir(source_dir) if f.endswith('.uasset')]

failed = []
skipped = []
total_boosted = 0

for uasset in uassets:
    base_name = os.path.splitext(uasset)[0]
    input_path = os.path.join(source_dir, uasset)
    # Stage the JSON next to the asset it came from, not in an empty folder.
    # UAssetGUI resolves an asset's siblings from disk, and a few of these
    # (Warehouse, WarehouseDoor, Factory_Raven, Factory_FormulaSCM) will not
    # write at all unless the rest of the export tree is beside them.
    json_path = os.path.join(source_dir, base_name + '.json')
    staged_uasset = os.path.join(source_dir, base_name + '.built.uasset')
    output_uasset = os.path.join(delivery_point_dir, base_name + '.uasset')

    # Step 3: read
    if not to_json(input_path, json_path):
        print(f'  FAILED to read {uasset} with {MAPPINGS}')
        failed.append(base_name)
        continue

    # Step 4: boost
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified_data, boosted = modifyDeliveryPoint(data)
    total_boosted += boosted

    # Nothing to boost means nothing to override. Shipping an unmodified copy
    # only risks re-serialising it worse than the game's own.
    if not boosted:
        os.remove(json_path)
        skipped.append(base_name)
        continue

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(modified_data, f, indent=4)

    # Step 5: write it back with the same mappings it was read with, then move
    # the result out of the vanilla export -- that folder stays pristine.
    built = from_json(json_path, staged_uasset)
    os.remove(json_path)
    if not built:
        print(f'  FAILED to build {base_name}')
        failed.append(base_name)
        continue

    staged_uexp = staged_uasset.replace('.uasset', '.uexp')
    shutil.move(staged_uasset, output_uasset)
    if os.path.exists(staged_uexp):
        shutil.move(staged_uexp, output_uasset.replace('.uasset', '.uexp'))

if os.path.exists(FAILED_LOG):
    os.remove(FAILED_LOG)
if failed:
    with open(FAILED_LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(failed) + '\n')

built = len(uassets) - len(failed) - len(skipped)
print(f'\n{built} delivery points built out of {len(uassets)} vanilla assets, '
      f'{total_boosted} MaxStorage values boosted x{BOOST}')
print(f'{len(skipped)} skipped with nothing to boost')
if failed:
    print(f'{len(failed)} FAILED, logged in {FAILED_LOG}: {failed}')
else:
    print('quattroStorage.py finished successfully.')
