CPU_IS = {
    "NOP": 0,
    "LRA": 1,
    "SRA": 2,
    "CALL": 3,
    "RET": 4,
    "JMP": 5,
    "JMPP": 6,
    "JMPZ": 7,
    "JMPN": 8,
    "JMPC": 9,
    "CCF": 10,
    "AND": 16,
    "OR": 17,
    "XOR": 18,
    "NOT": 19,
    "LSC": 20,
    "RSC": 21,
    "CMP": 22,
    "ADC": 32,
    "SBC": 33,
    "INC": 34,
    "DEC": 35,
    "ABS": 36,
    "UI": 48,
    "UO": 49,
    "PRW": 112,
    "PRR": 113,
    "HALT": 127
}
CPU_IS_O = {
    "NOP",
    "CCF",
    "HALT"
}
CPU_IS_D = {
    "NOT",
    "INC",
    "DEC",
    "ABS",
    "UI",
    "UO",
    "PRW",
    "PRR"
}
CPU_IS_T = {
    "SRA",
    "AND",
    "OR",
    "XOR",
    "LSC",
    "RSC",
    "CMP",
    "ADC",
    "SBC"
}
CPU_IS_FLAG_IGNORE = {
    "CALL",
    "RET",
    "SRA",
    "JMP",
    "JMPP",
    "JMPZ",
    "JMPN",
    "JMPC",
}


def decode(code: str) -> list[dict[str, int | list[str]]]:
    code = [
        {"idx": idx, "code": x.lstrip(" ").split(";")[0]} for idx, x in enumerate(code.split("\n"))]
    decoded = []

    for line in code:
        if line["code"]:
            d_line = {
                "ridx": line["idx"],            # real index
                "orig": line["code"],           # original line of code (inefficient)
                "struct": [y for y in [x.rstrip(",") for x in line["code"].split(" ")] if y]
            }

            decoded.append(d_line)

    return decoded


def precompile(code_struct: list[dict[str, int | list[str]]]):
    # Variables
    variable_pointers = {}
    variable_counter = 0

    # Jump pointers
    jump_pointers = {}

    # precompiled version
    precomp = []

    # Check for all jump pointers
    for idx, struct in enumerate(code_struct):
        # check if it's a jump pointer
        if struct["struct"][-1][-1] == ":":
            # add to jump pointers
            jump_pointers[struct["struct"][-1][:-1]] = 0

    # do all pointer checks
    for struct in code_struct:
        if struct["struct"][-1][-1] == ":":
            continue

        # check if it's a valid instruction
        if struct["struct"][0].upper() not in CPU_IS:
            raise NameError(f"Couldn't identify instruction '{struct['struct'][0]}' at {struct['ridx']};\n"
                            f"    {struct['orig']}")

        # check for variables
        for tag in struct["struct"]:
            if len(struct["struct"]) == 1:      # ex. NOP, HALT
                continue

            # if it's a pointer
            if tag[0] == "*":
                if not (tag[1:] in variable_pointers or tag[1:] in jump_pointers) \
                        and struct["struct"][0].upper() != "SRA":
                    raise NameError(f"Couldn't identify pointer '{tag[1:]}' at {struct['ridx']};\n"
                                    f"    {struct['orig']}")
                elif struct["struct"][0].upper() == "SRA":
                    variable_pointers[tag[1:]] = variable_counter
                    variable_counter += 1

    # convert to precompiled version
    for idx, struct in enumerate(code_struct):
        if struct["struct"][-1][-1] == ":":
            jump_pointers[struct["struct"][-1][:-1]] = len(precomp)
            continue

        # if there are 0 arguments, then just append the instruction
        if len(struct["struct"]) == 1:
            precomp.append({
                "ridx": struct["ridx"],
                "orig": struct["orig"],
                "comp": [struct["struct"][0].upper()]})

        # if there is 1 argument
        elif len(struct["struct"]) == 2:
            # check if instruction doesn't take any arguments
            if struct["struct"][0].upper() in CPU_IS_O:
                raise TypeError(f"Too many arguments! at {struct['ridx']};\n"
                                f"    {struct['orig']}")

            # if the instruction doesn't take an argument, the split instruction into 2
            if struct["struct"][0] in CPU_IS_D:
                precomp.append({
                    "ridx": struct["ridx"],
                    "orig": struct["orig"],
                    "comp": ["LRA", struct["struct"][1]]})
                precomp.append({
                    "ridx": struct["ridx"],
                    "orig": struct["orig"],
                    "comp": [struct["struct"][0].upper()]})

            # otherwise just add it as is
            else:
                precomp.append({
                    "ridx": struct["ridx"],
                    "orig": struct["orig"],
                    "comp": [struct["struct"][0].upper(), struct["struct"][1]]})

        # if there are 2 arguments
        elif len(struct["struct"]) == 3:
            # check if instruction can't take 2 arguments
            if struct["struct"][0].upper() not in CPU_IS_T:
                raise TypeError(f"Too many arguments! at {struct['ridx']};\n"
                                f"    {struct['orig']}")

            precomp.append({
                "ridx": struct["ridx"],
                "orig": struct["orig"],
                "comp": ["LRA", struct["struct"][1]]})
            precomp.append({
                "ridx": struct["ridx"],
                "orig": struct["orig"],
                "comp": [struct["struct"][0].upper(), struct["struct"][2]]})

    # convert all the pointers to values, and set flag bits
    for p_struct in precomp:
        # if there are no arguments
        if len(p_struct["comp"]) == 1:
            p_struct["comp"].append(0)
            p_struct["flag"] = 0
            continue

        for idx, tag in enumerate(p_struct["comp"][1:], start=1):
            # if tag is a pointer
            if tag[0] == "*":
                if tag[1:] in variable_pointers:
                    p_struct["comp"][idx] = variable_pointers[tag[1:]]
                elif tag[1:] in jump_pointers:
                    p_struct["comp"][idx] = jump_pointers[tag[1:]]
                else:
                    raise Exception("Something went wrong during compilation")

                if p_struct["comp"][0].upper() not in CPU_IS_FLAG_IGNORE:
                    p_struct["flag"] = 1
                else:
                    p_struct["flag"] = 0
            else:
                try:
                    if p_struct["comp"][idx][:2] == "0x":
                        p_struct["comp"][idx] = int(p_struct["comp"][idx][2:], 16) & 0xff
                    elif p_struct["comp"][idx][:2] == "0b":
                        p_struct["comp"][idx] = int(p_struct["comp"][idx][2:], 2) & 0xff
                    else:
                        p_struct["comp"][idx] = int(p_struct["comp"][idx], 10) & 0xff
                except ValueError:
                    raise TypeError(f"Unable to convert number at {p_struct['ridx']};\n"
                                    f"    {p_struct['orig']}")
                p_struct["flag"] = 0

    return precomp


def to_bytecode(precomp: list):
    output: list[list[int]] = []
    for p_struct in precomp:
        output.append(
            [
                p_struct["flag"],
                CPU_IS[p_struct["comp"][0]],
                p_struct["comp"][1]
            ]
        )

    return output


def precompile_code(code: str):
    return precompile(decode(code))


def test():
    code = """
_start:
    SRA 127, *y
loop_y:
    LRA *y
    DEC
    JMPZ *halt

    SRA 127, *x
loop_x:
    LRA *x
    DEC
    JMPZ *loop_y
    JMP *loop_x
    
    ; do something

halt:
    HALT
"""
    decoded = decode(code)
    for line in decoded:
        print(line)
    print()

    decoded = precompile(decoded)
    for line in decoded:
        print(line)
    print()

    for line in to_bytecode(decoded):
        print(f"{line[0]: ^3} | {bin(line[1])[2:]:0>7} | {bin(line[2])[2:]:0>8}")


if __name__ == '__main__':
    test()
