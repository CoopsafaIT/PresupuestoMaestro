

def create_years_base(year, stop=10):
    temporal_list = [('', '-- Seleccione Año Base --')]
    for i in range(year, year - stop, -1):
        temporal_list.append((i, i))
    return tuple(temporal_list)
