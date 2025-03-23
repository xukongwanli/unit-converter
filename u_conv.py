import re
from collections import defaultdict

conversion_table = {
    # Length
    'm': {'factor': 1.0, 'dimensions': {'L': 1}},
    'km': {'factor': 1e3, 'dimensions': {'L': 1}},
    'cm': {'factor': 1e-2, 'dimensions': {'L': 1}},
    'mm': {'factor': 1e-3, 'dimensions': {'L': 1}},
    'inch': {'factor': 0.0254, 'dimensions': {'L': 1}},
    'in': {'factor': 0.0254, 'dimensions': {'L': 1}},
    'ft': {'factor': 0.3048, 'dimensions': {'L': 1}},
    'feet': {'factor': 0.3048, 'dimensions': {'L': 1}},
    'mile': {'factor': 1609.344, 'dimensions': {'L': 1}},
    'yard': {'factor': 0.9144, 'dimensions': {'L': 1}},
    'nm': {'factor': 1e-9, 'dimensions': {'L': 1}},      
    'dm': {'factor': 0.1, 'dimensions': {'L': 1}},        
    'fm': {'factor': 1e-15, 'dimensions': {'L': 1}},      
    'nmi': {'factor': 1852, 'dimensions': {'L': 1}},      
    'nanometer': {'factor': 1e-9, 'dimensions': {'L': 1}},
    'decimeter': {'factor': 0.1, 'dimensions': {'L': 1}},
    'femtometer': {'factor': 1e-15, 'dimensions': {'L': 1}},
    'nautical_mile': {'factor': 1852, 'dimensions': {'L': 1}}

    # Mass
    ,
    'kg': {'factor': 1.0, 'dimensions': {'M': 1}},
    'g': {'factor': 1e-3, 'dimensions': {'M': 1}},
    'mg': {'factor': 1e-6, 'dimensions': {'M': 1}},
    'lb': {'factor': 0.45359237, 'dimensions': {'M': 1}},
    'lbm': {'factor': 0.45359237, 'dimensions': {'M': 1}},
    'slug': {'factor': 14.5939029, 'dimensions': {'M': 1}},
    'ounce': {'factor': 0.0283495, 'dimensions': {'M': 1}},
    # Time
    's': {'factor': 1.0, 'dimensions': {'T': 1}},
    'sec': {'factor': 1.0, 'dimensions': {'T': 1}},
    'min': {'factor': 60.0, 'dimensions': {'T': 1}},
    'hour': {'factor': 3600.0, 'dimensions': {'T': 1}},
    'h': {'factor': 3600.0, 'dimensions': {'T': 1}},
    'day': {'factor': 86400.0, 'dimensions': {'T': 1}},
    'year': {'factor': 31536000.0, 'dimensions': {'T': 1}},
    # Force
    'N': {'factor': 1.0, 'dimensions': {'M': 1, 'L': 1, 'T': -2}},
    'lbf': {'factor': 4.4482216153, 'dimensions': {'M': 1, 'L': 1, 'T': -2}},
    # Energy
    'J': {'factor': 1.0, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    'kJ': {'factor': 1e3, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    'cal': {'factor': 4.184, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    'kcal': {'factor': 4184.0, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    'btu': {'factor': 1055.05585262, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    'Wh': {'factor': 3600.0, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    'kWh': {'factor': 3.6e6, 'dimensions': {'M': 1, 'L': 2, 'T': -2}},
    # Power
    'W': {'factor': 1.0, 'dimensions': {'M': 1, 'L': 2, 'T': -3}},
    'kW': {'factor': 1e3, 'dimensions': {'M': 1, 'L': 2, 'T': -3}},
    'hp': {'factor': 745.7, 'dimensions': {'M': 1, 'L': 2, 'T': -3}},
    # Area
    'acre': {'factor': 4046.8564224, 'dimensions': {'L': 2}},
    'hectare': {'factor': 1e4, 'dimensions': {'L': 2}},
    # Volume
    'liter': {'factor': 0.001, 'dimensions': {'L': 3}},
    'L': {'factor': 0.001, 'dimensions': {'L': 3}},
    'gal': {'factor': 0.00378541, 'dimensions': {'L': 3}},
    'quart': {'factor': 0.000946353, 'dimensions': {'L': 3}},
    'pint': {'factor': 0.000473176, 'dimensions': {'L': 3}},
    # Pressure
    'Pa': {'factor': 1.0, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'hPa': {'factor': 100.0, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'kPa': {'factor': 1e3, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'MPa': {'factor': 1e6, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'GPa': {'factor': 1e9, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'bar': {'factor': 1e5, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'psi': {'factor': 6894.757293168, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'atm': {'factor': 101325, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
    'mmHg': {'factor': 133.322, 'dimensions': {'M': 1, 'L': -1, 'T': -2}},
}

temperature_units = {'C', '°C', 'F', '°F', 'K'}

def parse_composite_unit(unit_str):
    if '/' in unit_str:
        numerator_part, denominator_part = unit_str.split('/', 1)
    else:
        numerator_part = unit_str
        denominator_part = '1'

    numerator_components = re.split(r'[*·]', numerator_part)
    denominator_components = re.split(r'[*·]', denominator_part)

    parsed_num = []
    for comp in numerator_components:
        comp = comp.strip()
        if comp == '1':
            continue
        match = re.match(r'^([^\^]+)\^?(-?\d+)?$', comp)
        if not match:
            raise ValueError(f"Invalid component '{comp}' in unit '{unit_str}'")
        unit = match.group(1)
        exponent = int(match.group(2)) if match.group(2) else 1
        parsed_num.append((unit, exponent))

    parsed_den = []
    for comp in denominator_components:
        comp = comp.strip()
        if comp == '1':
            continue
        match = re.match(r'^([^\^]+)\^?(-?\d+)?$', comp)
        if not match:
            raise ValueError(f"Invalid component '{comp}' in unit '{unit_str}'")
        unit = match.group(1)
        exponent = int(match.group(2)) if match.group(2) else 1
        parsed_den.append((unit, exponent))

    return parsed_num, parsed_den

def compute_dimensions(parsed_num, parsed_den):
    dimensions = defaultdict(int)
    # Process numerator
    for unit, exp in parsed_num:
        if unit not in conversion_table:
            raise ValueError(f"Unit '{unit}' not found in conversion table.")
        unit_dims = conversion_table[unit]['dimensions']
        for dim, val in unit_dims.items():
            dimensions[dim] += val * exp
    # Process denominator
    for unit, exp in parsed_den:
        if unit not in conversion_table:
            raise ValueError(f"Unit '{unit}' not found in conversion table.")
        unit_dims = conversion_table[unit]['dimensions']
        for dim, val in unit_dims.items():
            dimensions[dim] -= val * exp
    # Remove dimensions with zero exponent
    return {k: v for k, v in dimensions.items() if v != 0}

def conv_u(orig_unit, target_unit, value):
    orig_lower = orig_unit.strip().replace('°', '').upper()
    target_lower = target_unit.strip().replace('°', '').upper()

    orig_in_temp = any(temp in orig_unit for temp in temperature_units)
    target_in_temp = any(temp in target_unit for temp in temperature_units)

    if orig_in_temp or target_in_temp:
        if not (orig_in_temp and target_in_temp):
            raise ValueError("Cannot convert between temperature and non-temperature units.")

        orig_temp = orig_unit.strip().replace('°', '')
        target_temp = target_unit.strip().replace('°', '')

        if orig_temp == 'K':
            celsius = value - 273.15
        elif orig_temp == 'F':
            celsius = (value - 32) * 5 / 9
        elif orig_temp == 'C':
            celsius = value
        else:
            raise ValueError(f"Unsupported temperature unit: {orig_unit}")

        if target_temp == 'K':
            result = celsius + 273.15
        elif target_temp == 'F':
            result = (celsius * 9 / 5) + 32
        elif target_temp == 'C':
            result = celsius
        else:
            raise ValueError(f"Unsupported temperature unit: {target_unit}")

        return result
    else:
        orig_num, orig_den = parse_composite_unit(orig_unit)
        target_num, target_den = parse_composite_unit(target_unit)

        # Calculate dimensions
        orig_dims = compute_dimensions(orig_num, orig_den)
        target_dims = compute_dimensions(target_num, target_den)

        # Check if dimensions match
        if orig_dims != target_dims:
            raise ValueError(f"Cannot convert between different unit types. Original dimensions: {orig_dims}, Target dimensions: {target_dims}")

        # Calculate conversion factors
        orig_factor = 1.0
        for unit, exp in orig_num:
            orig_factor *= conversion_table[unit]['factor'] ** exp
        for unit, exp in orig_den:
            orig_factor /= conversion_table[unit]['factor'] ** exp

        target_factor = 1.0
        for unit, exp in target_num:
            target_factor *= conversion_table[unit]['factor'] ** exp
        for unit, exp in target_den:
            target_factor /= conversion_table[unit]['factor'] ** exp

        conversion_ratio = orig_factor / target_factor
        return value * conversion_ratio