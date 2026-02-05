import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

class EnterpriseManager:
    def __init__(self):
        pass

    def ValidateCIF( self, CiF ):
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        if CiF is None:
            return False

        cif = CiF.strip().upper()

        if len(cif) != 9:
            return False

        letter = cif[0]
        number_block = cif[1:8]
        control = cif[8]

        if not letter.isalpha():
            return False
        if not number_block.isdigit():
            return False
        if not control.isalnum():
            return False

        digits = [int(d) for d in number_block]

        even_sum = digits[1] + digits[3] + digits[5]

        odd_sum = 0
        for idx in (0, 2, 4, 6):
            value = digits[idx] * 2
            if value >= 10:
                value = (value // 10) + (value % 10)
            odd_sum += value

        total = even_sum + odd_sum

        unit = total % 10
        base_digit = 0 if unit == 0 else 10 - unit

        digit_to_letter = {0: "J", 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}

        if letter in {"A", "B", "E", "H"}:
            return control.isdigit() and int(control) == base_digit

        if letter in {"K", "P", "Q", "S"}:
            return control.isalpha() and control == digit_to_letter[base_digit]

        return False

    def ReadproductcodefromJSON( self, fi ):

        try:
            with open(fi) as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e


        try:
            T_CIF = DATA["cif"]
            T_PHONE = DATA["phone"]
            E_NAME = DATA["enterprise_name"]
            req = EnterpriseRequest(T_CIF, T_PHONE,E_NAME)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.ValidateCIF(T_CIF) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req