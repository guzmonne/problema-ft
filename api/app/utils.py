import re
from typing import Any, List, Tuple
from .models.value import Value

def safe_get(l: Any, i: int, default=None) -> Any:
    """Safely get an element from a list by its index"""
    try:
        return l[i]
    except TypeError:
        return default
    except IndexError:
        return default

def identity(x: Any) -> Any:
    """Identiy function"""
    return x

def natural_language(number: int) -> str:
    """Converts an int into its natural language representation"""
    return str(int(number))

ILLIONS = {
    0: "",                  # 999
    1: " mil",               # 999 mil 999
    2: " millónes",         # 999 millónes 999 mil 999
    3: " mil",              # 999 mil 999 millónes 999 mil 999
    4: " billónes",         # 999 billónes 999 mil 999 millones 999 mil 999
    5: " mil",
    6: " trillónes",        # 999 mil 999 billónes 999 mil 999 millones 999 mil 999
    7: " mil",
    8: " cuatrillónes",
    9: " mil",
    10: " quintillónes", 
}

MULTIPLES_OF_100 = {
    "0": "",
    "1": "ciento",
    "2": "doscientos ",
    "3": "trescientos ",
    "4": "cuatroscientos ",
    "5": "quinientos ",
    "6": "seiscientos ",
    "7": "setecientos ",
    "8": "ochocientos ",
    "9": "novecientos ",
}

MULTIPLES_OF_10 = {
    "0": "",
    "1": "dieci", 
    "2": "veinti",
    "3": "treinta y ",
    "4": "cuarenta y ",
    "5": "cincuenta y ",
    "6": "sesenta y ",
    "7": "setenta y ",
    "8": "ochenta y ",
    "9": "noventa y ",
}

NUMBERS_CACHE = {
    "000": "",
    "0": "cero",
    "1": "uno",
    "2": "dos",
    "3": "tres",
    "4": "cuatro",
    "5": "cinco",
    "6": "seis",
    "7": "siete",
    "8": "ocho",
    "9": "nueve",
    "10": "diez",
    "11": "once",
    "12": "doce",
    "13": "trece",
    "14": "catorce",
    "15": "quince",
    "20": "veinte",
    "30": "treinta",
    "40": "cuarenta",
    "50": "cincuenta",
    "60": "sesenta",
    "70": "setenta",
    "80": "ochenta",
    "90": "noventa",
    "100": "cien",
    "1000": "mil",
    "1000000": "un millón",
    "1000000000000": "un billón",
    "1000000000000000000": "un trillón",
    "1000000000000000000000000": "un cuatrillón",
    "1000000000000000000000000000000": "un quintillón",
}

POSITION_TO_DICT = {
    0: MULTIPLES_OF_100,
    1: MULTIPLES_OF_10,
}

def single_digit_translator(number: str) -> str:
    return NUMBERS_CACHE.get(number)

def double_digit_translator(number: str) -> str:
    cached_number = NUMBERS_CACHE.get(number)
    if cached_number != None:
        return cached_number
    return "".join([MULTIPLES_OF_10.get(number[0]), NUMBERS_CACHE.get(number[1])])

def triple_digit_translator(number: str) -> str:
    cached_number = NUMBERS_CACHE.get(number)
    if cached_number != None:
        return cached_number
    return " ".join([MULTIPLES_OF_100.get(number[0]), double_digit_translator(number[1:3])])

TRANSLATORS = {
    1: single_digit_translator,
    2: double_digit_translator,
    3: triple_digit_translator,
}

def number_chunks(number: int, n: int) -> Tuple[List[str], int]:
    """Takes a number and returns a generator of chunks of n length"""
    inverse = str(int(number))[::-1]
    for i in range(0, len(inverse), n):
        yield (inverse[i:i + n][::-1], int(i / n))

def to_natural_language(number: str, multiple: int) -> str:
    """Converts a number under 999 to its natural language representation."""
    partial_result = []
    translator = TRANSLATORS[len(number)]
    result = translator(number)
    NUMBERS_CACHE[number] = result
    return result + ILLIONS.get(multiple, "")
    
def add_natural_language(value: Value) -> Value:
    """Adds a natural_language key to a value object"""
    if value is None:
        return
    try:
        struct = value.get("struct", {})
        number = struct.get("number", 0)
        result = []
        for (chunk, index) in number_chunks(number, 3):
            result.append(to_natural_language(chunk, index))        
        natural_language = " ".join(result[::-1])
        natural_language = re.sub(r"^uno\s|\sy\scero", "", natural_language)
        natural_language = re.sub(r"uno(?!$)", "un", natural_language)
        natural_language = re.sub(r"\s\s", " ", natural_language)
        value["natural_language"] = natural_language.strip()
        return value 
    except Exception:
        return value  
    