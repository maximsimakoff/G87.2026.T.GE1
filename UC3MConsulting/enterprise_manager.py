""" Enterprise Manager Class """

import json
from .EnterpriseManagementException import EnterpriseManagementException
from .EnterpriseRequest import EnterpriseRequest

digit_to_letter = {
    0: "J", 1: "A", 2: "B", 3: "C", 4: "D",
    5: "E", 6: "F", 7: "G", 8: "H", 9: "I"
}


class EnterpriseManager:
    """ Enterprise Manager Class """
    def __init__(self):
        pass

    def validate_cif(self, ci_f):
        """ Validate the CIF """
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE

        valid = False

        if ci_f is None:
            return False

        cif = ci_f.strip().upper()

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

        if letter in {"A", "B", "E", "H"}:
            valid = control.isdigit() and int(control) == base_digit
        elif letter in {"K", "P", "Q", "S"}:
            valid = control.isalpha() and control == digit_to_letter[base_digit]

        return valid


    def read_product_code_from_json( self, fi ):
        """ Read from the JSON file """

        try:
            with open(fi, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from e


        try:
            t_cif = data["cif"]
            t_phone = data["phone"]
            e_name = data["enterprise_name"]
            req = EnterpriseRequest(t_cif, t_phone,e_name)
        except KeyError as e:
            raise EnterpriseManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validate_cif(t_cif) :
            raise EnterpriseManagementException("Invalid FROM IBAN")
        return req
