def check_is_one_word(name_to_check : str) -> bool:
    splitted = name_to_check.split()
    if len(splitted) == 1 and splitted[0].isalpha():
        return True
    else:
        return False

def get_two_strings(text) -> list:
    new_data = text.replace(' ,' , ',')
    new_data = new_data.replace(', ' , ',')
    res = new_data.split(',')
    return res
