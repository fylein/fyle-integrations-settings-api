def dict_compare_keys(dict1, dict2):
    """
    Compare two dictionaries and return a list of key differences.
    Returns empty list if dictionaries have same keys.
    """
    keys1 = set(dict1.keys()) if dict1 else set()
    keys2 = set(dict2.keys()) if dict2 else set()
    
    missing_in_dict2 = keys1 - keys2
    extra_in_dict2 = keys2 - keys1
    
    differences = []
    if missing_in_dict2:
        differences.append(f"Keys missing in dict2: {missing_in_dict2}")
    if extra_in_dict2:
        differences.append(f"Extra keys in dict2: {extra_in_dict2}")
    
    return differences 
