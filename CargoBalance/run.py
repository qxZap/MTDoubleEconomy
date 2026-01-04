import json
import copy

RATIO = 0.25

IN_FILE = 'input.json'
OUT_FILE = 'output.json'

data = None
with open(IN_FILE, 'r') as f:
    data = json.loads(f.read())


if data:
    cargos = data.get('Exports')[0].get('Table').get('Data')
    replaced_cargos = []

    for cargo in cargos:
        cargoId = cargo.get('Name')

        current_cargo = copy.deepcopy(cargo)
        for i in range(0, len(current_cargo['Value'])):
            current_line_json = current_cargo['Value'][i]
            
            if current_line_json.get('Name') == 'PaymentSqrtRatio':
                current_line_json['Value'] = 0.0
            
            if current_line_json.get('Name') == 'PaymentPer1Km':
                current_line_json['Value'] = float(current_line_json['Value']) * RATIO
    
        replaced_cargos.append(current_cargo)

    with open(OUT_FILE, 'w+') as f:
        data['Exports'][0]['Table']['Data'] = replaced_cargos
            
        f.write(json.dumps(data, indent=4))
    