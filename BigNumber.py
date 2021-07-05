class BigNumber:

    def __init__(self, n):
        self.v = FloatString(n)

    def __str__(self):
        return f"{self.v}"

    def __repr__(self):
        return f"BigNumber(\"{self.v}\")"

    def add(self, n, trim=True):
        a, b = self.v.__str__(), BigNumber(n).__str__()
        a, b = self.normalize_df_numbers(a, b, index=1)  # make a > b by len(frac_part)
        a, b = self.equalize_df_numbers(a, b)  # add zeros to b to get len(a_frac_part) = len(b_frac_part)
        a, b = self.normalize_df_numbers(a, b)  # make a > b by len(int_part)
        a, b = a.split("."), b.split(".")
        result = self.recheck_result([
            self.terms_addition(a[0], b[0]), self.terms_addition(a[1], b[1])
        ])  # int & frac parts are separated
        ans = f"{''.join(result[0])}.{''.join(result[1])}"  # create a final floatstring
        if trim: ans = self.trim_zeros(ans)
        return ans

    def sub(self, n):
        pass

    def mult(self, n):
        pass

    def div(self, n):
        pass

    def check_terms(self, arr):
        """
        Checks if there is a number > 9 in the arr[1]. Performs += 1
        to arr[0] in this case, substracts 10 from arr[1]
        :param arr: intermediary unchecked result
        :return: calculated intermediary result
        """
        if len(arr) > 1 and int(arr[1]) > 9:
            arr.insert(0, str(int(arr.pop(0)) + 1))
            arr.insert(1, str(int(arr.pop(1)) - 10))
        return arr

    def normalize_df_numbers(self, a, b, index=0):
        """
        a > b but greatness is compared by length of integer or fractional part
        :param a, b str(float)
        :param index 0 - int part, 1 - frac part
        """
        a, b = a.split("."), b.split(".")
        if len(a[index]) < len(b[index]): a, b = b, a
        return ".".join(a), ".".join(b)

    def equalize_df_numbers(self, a, b):
        """
        Equalizes number of numbers in two floatstring numbers by
        adding zeros to one of it
        :param a: floatstring
        :param b: floatstring
        :return: equalized floatstring numbers
        """
        a_split, b_split = a.split("."), b.split(".")
        zeros_num = len(a_split[1]) - len(b_split[1])
        b_split.append(b_split.pop(1) + zeros_num * "0")
        return ".".join(a_split), ".".join(b_split)

    def terms_addition(self, a, b):
        """
        Consequently adds every term of intstring and checks for > 9
        :param a, b: intstring
        :return: list with split calculated terms
        """
        arr = []
        for i in range(len(a)):
            if b == "":
                arr.insert(0, a)
                arr = self.check_terms(arr)
                break
            arr.insert(0, str(int(a[-1]) + int(b[-1])))
            arr = self.check_terms(arr)
            a, b = a[:-1], b[:-1]
        return arr

    def recheck_result(self, arr):
        """
        Rechecks result by fractional part. If sum of frac parts gave > 1, add one
        to int part and combines int and frac part into single arr
        :param arr: list(int_part, frac_part)
        :return: list(checked_int_part, checked_frac_part)
        """
        if len(arr[1][0]) > 1:  # check if fractional part sum > 1
            arr[0].append(str(int(arr[0].pop(-1)) + 1))
            arr[1].insert(0, str(int(arr[1].pop(0)) - 10))
            int_part_checked = []
            for i in arr.pop(0)[::-1]:  # check for > 9 in current result int part
                int_part_checked.insert(0, i)
                self.check_terms(int_part_checked)
            arr.insert(0, int_part_checked)  # combine int and frac part
        return arr

    def trim_zeros(self, fs):
        """
        :param fs: floatstring to trim
        :return: trimmed floatstring
        """
        for i in range(len(fs)):
            if not fs[::-1][i] == "0":
                fs = fs[:len(fs) - i]
                break
        return fs


class FloatString:

    def __init__(self, n):
        self.v = f"{n}.0" if "." not in str(n) else str(n)  # str e.g. "1.0", "23.0"

    def __str__(self):
        return f"{self.v}"

    def __repr__(self):
        return f"FloatString(\"{self.v}\")"


class IntString:

    def __init__(self, n):
        self.v = str(n)[:str(n).index(".")] if "." in str(n) else str(n)  # str e.g. "3", "245"

    def __str__(self):
        return f"{self.v}"

    def __repr__(self):
        return f"IntString(\"{self.v}\")"


def main():
    a = BigNumber("12.1232342344534534552342342342342345354678908765432134567890765432456789")
    b = BigNumber("1212.3242435678907654356786543567890876543456789087654324567896543245678976543242567")
    c = a.add(b)
    print(c)


if __name__ == '__main__':
    main()