import sys
from typing import List


table = {
    'curr_mem': 16,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
}

for i in range(16):
    table['R' + str(i)] = i

jump_table = {
    #  jump
    'null': 0,
    'JGT': 1,
    'JEQ': 2,
    'JGE': 3,
    'JLT': 4,
    'JNE': 5,
    'JLE': 6,
    'JMP': 7,
}

dest_table = {
    #  dest
    'null': 0,
    'M': 1,
    'D': 2,
    'MD': 3,
    'A': 4,
    'AM': 5,
    'AD': 6,
    'AMD': 7,
}

comp_table = {
    #  comp
    '0': int('0101010', 2),
    '1': int('0111111', 2),
    '-1': int('0111010', 2),
    'D': int('0001100', 2),
    'A': int('0110000', 2),
    'M': int('1110000', 2),
    '!D': int('0001101', 2),
    '!A': int('0110001', 2),
    '!M': int('1110001', 2),
    '-D': int('0001111', 2),
    '-A': int('0110011', 2),
    '-M': int('1110011', 2),
    'D+1': int('0011111', 2),
    'A+1': int('0110111', 2),
    'M+1': int('1110111', 2),
    'D-1': int('0001110', 2),
    'A-1': int('0110010', 2),
    'M-1': int('1110010', 2),
    'D+A': int('0000010', 2),
    'D+M': int('1000010', 2),
    'D-A': int('0010011', 2),
    'D-M': int('1010011', 2),
    'A-D': int('0000111', 2),
    'M-D': int('1000111', 2),
    'D&A': int('0000000', 2),
    'D&M': int('1000000', 2),
    'D|A': int('0010101', 2),
    'D|M': int('1010101', 2),
}



def read_file(filename: str) -> List[str]:
    """
    params:
        filename: name of the Assembly file
    returns:
        list of all A and C instruction
    """
    lines = []
    line_no = 0
    with open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            ls = line.strip()

            # if the line is blank or comment ignore it
            if not ls or ls.startswith('//'):
                continue

            # if the line is a label also ignore it,
            # but keep the address in a symbol table
            if ls.startswith('('):
                label = ls[1:-1]
                table[label] = line_no
                continue

            # Check if a line contain trailing comment
            if (c_index := ls.find('/')) and c_index != -1:
                ls = ls[:c_index].strip()

            lines.append(ls)

            line_no += 1

    return lines


def int_to_bin(value: int, n: int) -> str:
    binary_value = bin(value)
    binary_value = binary_value[2:]  # ignore the 0b prefix
    if len(binary_value) > n:
        raise Exception('Value is greater than padding')
    return binary_value.zfill(n)


def decode_A_ins(ins: str) -> str:
    """
    params:
        ins: instruction string is '@value'
    returns:
        0 padded 16bit int in binary form
    """

    # ignore the '@' char
    ins = ins[1:]

    if ins[0].isdigit():  # numeric value
        return int_to_bin(int(ins), 16)
    else:  # either variable of label
        if ins in table:
            value = table[ins]
            return int_to_bin(value, 16)
        else:
            table[ins] = table['curr_mem']
            table['curr_mem'] += 1
            return int_to_bin(table[ins], 16)

    raise Exception('Undefined A instruction')


def decode_C_ins(ins: str) -> str:
    """
    The instruction is in this form
    dest = comp ; jmp
    """

    # try spliting on ';'
    parts = ins.split(';')
    if len(parts) == 1:  # no jump instruction
        jmp = int_to_bin(jump_table['null'], 3)
    else:
        jmp = int_to_bin(jump_table[parts[1]], 3)

    dest_cmp = parts[0].split('=')
    dest = int_to_bin(dest_table['null'], 3)
    if len(dest_cmp) == 1:
        cmp = int_to_bin(comp_table[dest_cmp[0]], 7)
    else:
        dest = int_to_bin(dest_table[dest_cmp[0]], 3)
        cmp = int_to_bin(comp_table[dest_cmp[1]], 7)

    return '111' + cmp + dest + jmp

data = read_file(sys.argv[1])

for ins in data:
    #  print(line_no, line)
    if ins.startswith('@'):
        print(decode_A_ins(ins))
    else:
        print(decode_C_ins(ins))
