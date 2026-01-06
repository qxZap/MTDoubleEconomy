import json
import copy
import os

CompanyAIConditionUsageMultiplier = 0.25
CompanyAIConditionUsageMultiplierOffroad = 0.4

def isVehiclePolice(vehicleJson):
    return '[Vehicle.Delivery].Police' in json.dumps(vehicleJson)

def isVehicleHeavy(vehicleJson):
    return '[Vehicle.Delivery].Heavy' in json.dumps(vehicleJson)

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

def process_data(data, filename):
    if data:
        vehicles = data.get('Exports', [{}])[0].get('Table', {}).get('Data', [])
        replaced_vehicles = []
        for vehicle in vehicles:
            current_vehicle = copy.deepcopy(vehicle)
            for i in range(len(current_vehicle.get('Value', []))):
                current_line_json = current_vehicle['Value'][i]
                fieldName = current_line_json.get('Name')
                # Economy patch
                if fieldName == "CompanyAIConditionUsageMultiplier":
                    current_line_json['Value'] = CompanyAIConditionUsageMultiplier
                if fieldName == "CompanyAIConditionUsageMultiplierOffroad":
                    current_line_json['Value'] = CompanyAIConditionUsageMultiplierOffroad

                # Disabled / Hidden
                if fieldName == "bHidden":
                    current_line_json['Value'] = False
                if fieldName == "bDisabled":
                    current_line_json['Value'] = False

                # Taxi/Limo all besides Police meant
                if fieldName == "bIsTaxiable":
                    current_line_json['Value'] = True
                if fieldName == "bIsLimoable":
                    current_line_json['Value'] = True
                if fieldName == "bIsBusable":
                    current_line_json['Value'] = True
                if fieldName == "bIsRaceCar":
                    current_line_json['Value'] = True

                # patch parts
                if fieldName == "NotSupportedPartTypes":
                    current_line_json['Value'] = []
                if fieldName == "NotOptionalPartTypes":
                    current_line_json['Value'] = []
            
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
    if filename.endswith('.json'):
        in_path = os.path.join(input_dir, filename)
        out_path = os.path.join(output_dir, filename)
        
        data = load_json(in_path)
        modified_data = process_data(data, filename)
        save_json(modified_data, out_path)