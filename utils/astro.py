def ra_to_decimal(ra_str):
    """Converts RA 'HH:MM:SS.ss' to Decimal Degrees"""
    if isinstance(ra_str, (int, float)):
        return float(ra_str) # Already decimal
        
    parts = ra_str.replace(" ", ":").split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid RA format: {ra_str}")
        
    h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
    decimal_hours = h + (m / 60.0) + (s / 3600.0)
    return round(decimal_hours * 15.0, 5)

def dec_to_decimal(dec_str):
    """Converts DEC '+DD:MM:SS.ss' to Decimal Degrees"""
    if isinstance(dec_str, (int, float)):
        return float(dec_str) # Already decimal
        
    parts = dec_str.replace(" ", ":").split(":")
    if len(parts) != 3:
        raise ValueError(f"Invalid DEC format: {dec_str}")
        
    d, m, s = float(parts[0]), float(parts[1]), float(parts[2])
    sign = -1 if d < 0 or str(parts[0]).startswith('-') else 1
    
    decimal_degrees = abs(d) + (m / 60.0) + (s / 3600.0)
    return round(decimal_degrees * sign, 5)
