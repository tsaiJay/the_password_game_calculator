import json
import re

def load_atom_dict(path) -> dict:
    element_dict = {}
    with open(path, 'r') as f:
        ''' struct -> file['element'][0]['symbol', 'number'] '''
        data = json.load(f)
        data = data['elements']
    for d in data:
        element_dict[d['symbol']] = d['number']

    return element_dict

def count_dict_keys_in_str(input_str, source_dict):
    SPEC = '*MARKED*'
    # sort dict keys by length
    sorted_dict = dict(sorted(source_dict.items(), key=lambda item: len(item[0]), reverse=True))

    found = {}
    for k in sorted_dict.keys():
        input_str = input_str.replace(k, SPEC)
        c = input_str.count(SPEC)
        if c != 0:
            found[k] = c
            input_str = input_str.replace(SPEC, '')

    return found

def detect_roman_numerals(text):
    roman_list = []
    roman_pattern = r'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
    result = re.findall(roman_pattern, text)
    for r in result:
        for j in r:
            if j != '':
                roman_list.append(j)
    return roman_list

def roman_to_num(x: str) -> int:
    roman_dict = {  # I(1), V(5)，X(10)，L(50)，C(100)，D(500)，M(1000)
        'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10, 'XL': 40,
        'L': 50, 'XC': 90, 'C': 100, 'CD': 400, 'D': 500,
        'CM': 900, 'M': 100
    }
    answer = 0
    while x:
        if x[0:2] in roman_dict.keys():
            answer += roman_dict[x[0:2]]
            x = x[2:]
        elif x[0] in roman_dict.keys():
            answer += roman_dict[x[0]]
            x = x[1:]
    return answer

def get_number_sum(x: str):
    dets = ''
    for i in x:
        if i.isdigit():
            dets += i
        else:
            dets += ' '
    dets = dets.split(' ')
    nums = [int(i) for i in dets if i]
    total = sum(nums)
    return total, nums

def get_atom_sum(x: str, atom_dict: dict):
    counts_dict = count_dict_keys_in_str(x, atom_dict)
    total = 0
    for k in counts_dict.keys():
        total += atom_dict[k] * counts_dict[k]
    return total

def get_roman_product(x: str):
    dets_roman_list = detect_roman_numerals(x)
    dets_int_list = [roman_to_num(i) for i in dets_roman_list]
    if dets_roman_list == []:
        return None, [], []
    product = 1
    for num in dets_int_list:
        product *= num
    return product, dets_roman_list, dets_int_list


if __name__ == "__main__":
    atom_dict = load_atom_dict('./PeriodicTableJSON.json')

    while True:
        password = input("new code to extract: ")
        # password = "He df H sdf NNNNN NI"
        # password = "IVTVIhisVumerals: I, IV"

        print(f'|     rule                   | result  | need  |')

        ''' Rule 5 – The digits in your password must add up to 25 '''
        total, nums = get_number_sum(password)
        print(f'[Rule 5 : digits sum=25]    --> {total}, {nums}')

        ''' Rule 9 – The Roman numerals in your password should multiply to 35 '''
        roman_product, det_romans, det_ints = get_roman_product(password)
        print(f'[Rule 9 : roman product=35] --> {roman_product}, {det_romans}')

        ''' Rule 18 – The elements in your password must have atomic numbers that add up to 200 '''
        atom_sum = get_atom_sum(password, atom_dict)
        print(f'[Rule 18: atomic sum=200]   --> {atom_sum}, need {200 - atom_sum}')
