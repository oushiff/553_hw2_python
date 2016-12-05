from fractions import Fraction


def matrix_check(matrix):
    if matrix == None or len(matrix) == 0:
        return False, 0, 0
    col_len = len(matrix[0])
    for row in matrix:
        if len(row) != col_len:
            return False, 0, 0
    return True, len(matrix), col_len

def multi_matrix_matrix(matrix1, matrix2):
    m1_bool, m1_raw_len, m1_col_len = matrix_check(matrix1)
    m2_bool, m2_raw_len, m2_col_len = matrix_check(matrix2)
    if m1_bool == False or m2_bool == False or m1_col_len != m2_raw_len:
        return False, [[]]
    res = []
    i = 0
    j = 0
    k = 0
    while i < m1_raw_len:
        j = 0
        new_row = []
        while j < m2_col_len:
            k = 0
            cur_sum = Fraction(0)
            while k < m1_col_len:
                cur_sum += (matrix1[i][k] * matrix2[k][j])
                k += 1
            new_row.append(cur_sum)
            j += 1
        res.append(new_row)
        i += 1
    return True, res

def multi_matrix_num(matrix, num):
    m_bool, m_raw_len, m_col_len = matrix_check(matrix)
    if m_bool == False:
        return False, [[]]
    res = []
    for row in matrix:
        new_row = []
        for elem in row:
            new_row.append(num * elem)
        res.append(new_row)
    return True, res

def plus_matrix(matrix1, matrix2):
    m1_bool, m1_raw_len, m1_col_len = matrix_check(matrix1)
    m2_bool, m2_raw_len, m2_col_len = matrix_check(matrix2)
    if m1_bool == False or m2_bool == False or m1_raw_len != m2_raw_len or m1_col_len !=m2_col_len:
        return False, [[]]
    res = []
    i = 0
    j = 0
    k = 0
    while i < m1_raw_len:
        j = 0
        new_row = []
        while j < m1_col_len:
            new_row.append(matrix1[i][j] + matrix2[i][j])
            j += 1
        res.append(new_row)
        i += 1
    return True, res

def matrix_print(matrix):
    stream = ""
    for row in matrix:
        for elem in row:
            stream += str(elem) + "   "
        stream += "\n"
    stream += "\n"
    print(stream)

def _main():
    M = [[Fraction(), Fraction(1, 2), Fraction(), Fraction()], [Fraction(1,3), Fraction(), Fraction(), Fraction(1,2)], [Fraction(1,3), Fraction(), Fraction(), Fraction(1,2)], [Fraction(1, 3), Fraction(1, 2), Fraction(), Fraction()]]
    v = [[Fraction(1,4)], [Fraction(1,4)], [Fraction(1,4)], [Fraction(1,4)]]
    res = [[Fraction(1,4)], [Fraction(1,4)], [Fraction(1,4)], [Fraction(1,4)]]
    belta = Fraction(8, 10)
    while True:
        a1_bool, a1_res = multi_matrix_num(res, belta)
        a2_bool, a2_res = multi_matrix_matrix(M, a1_res)
        a3_bool, a3_res = multi_matrix_num(v, Fraction(2, 10))
        isSucc, res = plus_matrix(a2_res, a3_res)
        matrix_print(res)


_main()