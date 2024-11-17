company_types = ["small", "medium", "large"]

def avg_electric_bill(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(500, 1000)
    elif company_type == company_types[1]:  # medium
        return range(2000, 5000)
    else:  # large
        return range(10_000, 50_000)


def avg_gas_bill(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(10, 100)
    elif company_type == company_types[1]:  # medium
        return range(500, 2000)
    else:  # large
        return range(2_000, 10_000)


def avg_transport_cost(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(500, 1500)
    elif company_type == company_types[1]:  # medium
        return range(2000, 5000)
    else:  # large
        return range(10_000, 50_000)


def waste_generated_dummy(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(100, 500)
    elif company_type == company_types[1]:  # medium
        return range(500, 2000)
    else:  # large
        return range(2000, 10_000)


def recycled_waste(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(20, 40)
    elif company_type == company_types[1]:  # medium
        return range(30, 50)
    else:  # large
        return range(40, 60)


def travel_kms(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(10_000, 50_000)
    elif company_type == company_types[1]:  # medium
        return range(50_000, 1_00_000)
    else:  # large
        return range(1_00_000, 2_00_000)


def vehicle_fuel_efficiency(company_type: str) -> range:
    if company_type not in company_types:
        raise Exception("Wrong company size")

    if company_type == company_types[0]:  # small
        return range(5, 7)
    elif company_type == company_types[1]:  # medium
        return range(7, 9)
    else:  # large
        return range(9, 15)
