import copy
import json
import os

RATIO = 0.5
# RATIO = 1
VANILLA_GAP = 91
FLAG_OVERSIZED = 67

# Get all JSON files in the current directory
json_files = [f for f in os.listdir(".") if f.endswith(".json")]

for file_name in json_files:
    data = None
    with open(file_name, "r") as f:
        data = json.loads(f.read())

    if data:
        cargos = data.get("Exports")[0].get("Table").get("Data")
        replaced_cargos = []
        iterated = 0

        for cargo in cargos:
            cargoId = cargo.get("Name")

            current_cargo = copy.deepcopy(cargo)
            # Initialize scaling flag for this cargo; assume it should be scaled unless flagged oversized
            scaling = {cargoId: True}

            for i in range(0, len(current_cargo["Value"])):
                current_line_json = current_cargo["Value"][i]

                if True:
                    if current_line_json.get("Name") == "PaymentSqrtRatio":
                        # if current_line_json["Value"] == 0.0:
                        #     scaling[cargoId] = True
                        current_line_json["Value"] = 0.0
                    if current_line_json.get("Name") == "CargoFlags":
                        if current_line_json["Value"] == FLAG_OVERSIZED:
                            scaling[cargoId] = False

            for i in range(0, len(current_cargo["Value"])):
                current_line_json = current_cargo["Value"][i]

                if True:
                    if scaling[cargoId]:
                        if current_line_json.get("Name") == "PaymentPer1Km":
                            current_line_json["Value"] = (
                                float(current_line_json["Value"]) * RATIO
                            )

                if current_line_json.get("Name") == "bAllowStacking":
                    current_line_json["Value"] = True

            replaced_cargos.append(current_cargo)

            iterated += 1

        with open(file_name, "w+") as f:
            data["Exports"][0]["Table"]["Data"] = replaced_cargos

            f.write(json.dumps(data, indent=4))

print("Cargo Files Changed")
