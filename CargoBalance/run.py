import json
import copy

# RATIO = 0.5
RATIO = 1
VANILLA_GAP = 84

IN_FILE = 'input.json'
OUT_FILE = 'Cargos.json'

data = None
with open(IN_FILE, 'r') as f:
    data = json.loads(f.read())


if data:
    cargos = data.get('Exports')[0].get('Table').get('Data')
    replaced_cargos = []
    iterated = 0

    for cargo in cargos:
        cargoId = cargo.get('Name')

        current_cargo = copy.deepcopy(cargo)

        for i in range(0, len(current_cargo['Value'])):
            current_line_json = current_cargo['Value'][i]
                
            # if iterated<VANILLA_GAP:
            if True:
                if current_line_json.get('Name') == 'PaymentSqrtRatio':
                    current_line_json['Value'] = 0.0
                    
                if current_line_json.get('Name') == 'PaymentPer1Km':
                    current_line_json['Value'] = float(current_line_json['Value']) * RATIO
            
            if current_line_json.get('Name') == 'bAllowStacking':
                current_line_json['Value'] = True
    
        replaced_cargos.append(current_cargo)

        iterated+=1

    with open(OUT_FILE, 'w+') as f:
        data['Exports'][0]['Table']['Data'] = replaced_cargos
            
        f.write(json.dumps(data, indent=4))
    