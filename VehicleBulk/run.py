import json
import copy
import os

CompanyAIConditionUsageMultiplier = 0.25
CompanyAIConditionUsageMultiplierOffroad = 0.4

def isVehiclePolice(vehicleJson):
    return 'Vehicle.Delivery.Police' in json.dumps(vehicleJson)

def isVehicleHeavy(vehicleJson):
    return 'Vehicle.Delivery.Heavy' in json.dumps(vehicleJson)

def isVehicleTrailer(vehicleJson):
    pass

# "ObjectName": "Vehicles_1",
# "OuterIndex": -5417,
def newDataTable(ObjectName, OuterIndex):
    return {
      "$type": "UAssetAPI.Import, UAssetAPI",
      "ObjectName": ObjectName,
      "OuterIndex": OuterIndex,
      "ClassPackage": "/Script/Engine",
      "ClassName": "DataTable",
      "PackageName": None,
      "bImportOptional": False
    }

# /Game/DataAsset/Vehicles/Vehicles_Ambulance
def newPackageImport(ObjectName):
    return {
      "$type": "UAssetAPI.Import, UAssetAPI",
      "ObjectName": ObjectName,
      "OuterIndex": 0,
      "ClassPackage": "/Script/CoreUObject",
      "ClassName": "Package",
      "PackageName": None,
      "bImportOptional": False
    }

def newComposite(index):
    return {
              "$type": "UAssetAPI.PropertyTypes.Objects.ObjectPropertyData, UAssetAPI",
              "Name": "10",
              "ArrayIndex": 0,
              "IsZero": False,
              "PropertyTagFlags": "None",
              "PropertyTagExtensions": "NoExtension",
              "Value": index
            }

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def vehicleChangeSetFieldValue(vehicle, fieldName, fieldValue):
    current_vehicle = copy.deepcopy(vehicle)
    for i in range(len(current_vehicle.get('Value', []))):
        current_line_json = current_vehicle['Value'][i]
        fname = current_line_json.get('Name')

        if fieldName == fname:
            current_line_json['Value'] = fieldValue

    return current_vehicle

def vehicleGetFieldValue(vehicle, fieldName):
    for i in range(len(vehicle.get('Value', []))):
        current_line_json = vehicle['Value'][i]
        fname = current_line_json.get('Name')

        if fieldName == fname:
            return current_line_json['Value']

    return None

def process_data(data, filename):
    if data:
        vehicles = data.get('Exports', [{}])[0].get('Table', {}).get('Data', [])
        replaced_vehicles = []
        for vehicle in vehicles:
            current_vehicle = copy.deepcopy(vehicle)

            if not isVehiclePolice(current_vehicle):
                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "CompanyAIConditionUsageMultiplier", CompanyAIConditionUsageMultiplier)
                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "CompanyAIConditionUsageMultiplierOffroad", CompanyAIConditionUsageMultiplierOffroad)
                
                bHidden = vehicleGetFieldValue(current_vehicle, "bHidden")
                bDisabled = vehicleGetFieldValue(current_vehicle, "bDisabled")
                if bHidden or bDisabled:
                    current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "bIsRaceCar", True)

                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "bHidden", False)
                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "bDisabled", False)

                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "bIsTaxiable", True)
                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "bIsLimoable", True)
                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "bIsBusable", True)

                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "NotSupportedPartTypes", [])
                current_vehicle = vehicleChangeSetFieldValue(current_vehicle, "NotOptionalPartTypes", [])
            
            replaced_vehicles.append(current_vehicle)
        
        # Patch Files
        if filename == 'Vehicles.json':
            index = len(data.get("Imports"))

            data['Imports'].append(newDataTable('Vehicles_Deprecated', (-1)*index-2  ))
            data['Imports'].append(newPackageImport('/Game/DataAsset/Vehicles/Vehicles_Deprecated'))

            # data['Exports'][0]['SerializationBeforeSerializationDependencies'].append((-1)*index-1)

            data['Exports'][0]['Data'][0]['Value'].append(newComposite((-1)*index-1))

            data['NameMap'].append('/Game/DataAsset/Vehicles/Vehicles_Deprecated')
            data['NameMap'].append('Vehicles_Deprecated')
        
        data['Exports'][0]['Table']['Data'] = replaced_vehicles
    return data

# Create output directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

input_dir = 'input'
for filename in os.listdir(input_dir):
    # if filename.endswith('.json') and 'Vehicles_1' not in filename:
    if filename.endswith('.json'):
        in_path = os.path.join(input_dir, filename)
        out_path = os.path.join(output_dir, filename)
        
        data = load_json(in_path)
        modified_data = process_data(data, filename)
        save_json(modified_data, out_path)