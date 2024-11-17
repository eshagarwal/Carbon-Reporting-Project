# Calculation functions
def calculate_CO2_from_energy_usage(electricity_bill, natural_gas_bill, fuel_bill):
    CO2_from_electricity_usage = electricity_bill * 12 * 0.0005
    CO2_from_natural_gas_usage = natural_gas_bill * 12 * 0.0053
    CO2_from_fuel_usage = fuel_bill * 12 * 2.32
    return (
        CO2_from_electricity_usage
        + CO2_from_natural_gas_usage
        + CO2_from_fuel_usage
    )

def calculate_CO2_from_waste(waste_per_month, recycling_percent):
    return waste_per_month * 12 * 0.57 - recycling_percent

def calculate_CO2_from_business_travel(distance_km, fuel_efficiency):
    return distance_km * 1 / fuel_efficiency * 2.31