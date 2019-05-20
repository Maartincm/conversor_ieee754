import re

class IEEE754Conversor:

    def __init__(self, number=False, *args, **kwargs):
        self.number = number

    def convert_to_32bit(self):
        binary = self.binary_conversion()
        normalized = self.normalize(binary)

    def normalize(self, signed_binary):
        sign = signed_binary.startswith('-')
        binary = sign and signed_binary[1:] or signed_binary
        mantissa = re.sub("[-.]", "", binary)[1:]
        comma_place = "." in binary and binary.find(".") \
            or len(binary)
        exponent = comma_place - 1 + 127
        sign_str = str(int(sign))
        exponent_str = self.convert_int_to_base(
            exponent, 2).rjust(8, '0')
        fraction_str = mantissa[:23].ljust(23, '0')
        normalized = ("%s%s%s") % (
            sign_str, exponent_str, fraction_str)
        print("Normalizing: %s -> %s" % (signed_binary, normalized))
        print(("Sign: %s, Exponent: %s, Mantissa: %s") % (
            sign_str, exponent_str, fraction_str))
        return normalized

    def binary_conversion(self):
        if not self.number:
            decimal_number = self.prompt_binary_conversion()
        else:
            decimal_number = self.number
        binary = self.convert_to_binary(decimal_number)
        return binary

    def convert_to_binary(self, number):
        sign = number < 0 and '-' or ''
        integer_part = int(number)
        fractional_part = round(number - integer_part, 3)
        binary_int = self.convert_int_to_base(integer_part, 2)
        binary_frac = self.convert_frac_to_base(fractional_part, 2)
        binary = ("%s%s%s") % (
            sign, binary_int,
            binary_frac and ".%s" % binary_frac or "")
        binary = binary or "0"
        print("Converting to binary: %s -> %s" % (number, binary))
        return binary

    def convert_int_to_base(self, int_num, base, result=False):
        if not result:
            result = []
        int_num = abs(int_num)
        if int_num in (1, 0):
            return str(int_num)
        ratio, remainder = divmod(int_num, base)
        if ratio == 1:
            result.append(remainder)
            result.append(1)
            return ("").join([str(x) for x in reversed(result)])
        result.append(remainder)
        return self.convert_int_to_base(ratio, base, result)

    def convert_frac_to_base(self, frac_num, base, max_tries=25,
                             tries=0, result=False):
        if not frac_num:
            return ""
        if not result:
            result = []
        frac_num = abs(frac_num)
        product = frac_num * base
        int_res = int(product)
        frac_res = product % 1
        if round(frac_res, 3) == 0 or tries >= max_tries:
            result.append(1)
            return ("").join([str(x) for x in result])
        result.append(int_res)
        tries += 1
        return self.convert_frac_to_base(frac_res, base,
                                         result=result, tries=tries)

    def prompt_binary_conversion(self):
        print("Real Decimal Number to IEEE754 Binary conversion:\n")
        integer_part = False
        fractional_part = False
        while not integer_part:
            try:
                integer_part = self.validate_3_digits(
                    input("Enter integer part: "))
            except InvalidInputError:
                print("Invalid input. Try again")
        while not fractional_part:
            try:
                fractional_part = self.validate_3_digits(
                    input("Enter fractional part: "))
            except InvalidInputError:
                print("Invalid input. Try again")
        return float("%s.%s" % (str(integer_part), str(fractional_part)))

    def validate_3_digits(self, number):
        try:
            num = int(number)
            assert (-999 <= num <= 999)
            return num
        except:
            raise InvalidInputError(
                ("Number '%s' has not a valid format " +
                 "(Should have 3 digits)") % number)


class InvalidInputError(BaseException):
    def __init__(self, message):
        self.msg = message


if __name__ == '__main__':
    conversor = IEEE754Conversor(-61.875)
    conversor.convert_to_32bit()

    conversor.number = False
    conversor.convert_to_32bit()
