import json

final_data = {}

with open("input.json", "r") as f:
    data = json.load(f)

    cargos = data.get('Cargo', {})
    cargo_type = cargos.get('PaymentMultipliers',{})

    final_cargo_data = {}

    for key, value in cargo_type.items():
        final_cargo_data[key] = value * 2
    
    final_data={'Cargo': {'PaymentMultipliers': final_cargo_data}}

with open("output.json", "w") as f:
    json.dump(final_data, f, indent=4)