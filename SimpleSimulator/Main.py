import matplotlib.pyplot as plt

cycle_number = -1

def dumpMEM():
    for i in MEM:
        print(i)


def dumpPC_REG():
    y = convert8(PC)
    print(y, end=" ")
    for i in reg_encoding.keys():
        if(i!="111"):
            x = convert16(reg_encoding[i])
        else:
            x = reg_encoding[i]
        print(x, end=" ")


def convert8(val):
    y = int(val)
    x = bin(y).replace("0b", "")
    while len(x) < 8:
        x = "0" + x
    return x


def convert16(val):
    y = int(val)
    x = bin(y).replace("0b", "")
    while len(x) < 16:
        x = "0" + x
    return x

#made this function to get only last 16 bits values
def convert16bin(val):
    y = int(val)
    x = bin(y).replace("0b", "")
    z = x[-16:]
    return z

def parameter_based_on_type(instruction, type):
    # returning as strings
    if type == "A":
        r0 = instruction[7:10]
        r1 = instruction[10:13]
        r2 = instruction[13:]
        return r0, r1, r2
    elif type == "B":
        r0 = instruction[5:8]
        imm = instruction[8:]
        return r0, imm
    elif type == "C":
        r0 = instruction[10:13]
        r1 = instruction[13:]
        return r0, r1
    elif type == "D":
        r0 = instruction[5:8]
        mem_add = instruction[8:]
        return r0, mem_add
    elif type == "E":
        mem_add = instruction[8:]
        return mem_add
    else:
        return -1

# give full line as input
# will give based on type of instruction
def decode(instruction):
    op = instruction[0:5]
    opcode = op_table[op]
    if opcode == "add":
        type = "A"
        return type
    elif opcode == "sub":
        type = "A"
        return type
    elif opcode == "mov_im":
        type = "B"
        return type
    elif opcode == "mov":
        type = "C"
        return type
    elif opcode == "ld":
        type = "D"
        return type
    elif opcode == "st":
        type = "D"
        return type
    elif opcode == "mul":
        type = "A"
        return type
    elif opcode == "div":
        type = "C"
        return type
    elif opcode == "rs":
        type = "B"
        return type
    elif opcode == "ls":
        type = "B"
        return type
    elif opcode == "xor":
        type = "A"
        return type
    elif opcode == "or":
        type = "A"
        return type
    elif opcode == "and":
        type = "A"
        return type
    elif opcode == "not":
        type = "C"
        return type
    elif opcode == "cmp":
        type = "C"
        return type
    elif opcode == "jmp":
        type = "E"
        return type
    elif opcode == "jlt":
        type = "E"
        return type
    elif opcode == "jgt":
        type = "E"
        return type
    elif opcode == "je":
        type = "E"
        return type
    else:
        type = "F"
        return type


def checkOverflow(data):
    if data < 0 or data >= pow(2,16):
        # Overflow Bit set to 1
        reg_encoding["111"] = "000000000000" + "1000"
        return True
    return False


def execute():
    # Execute Stage
    halted = False
    global PC
    global cycle_number
    while not halted:
        instruction = MEM[PC]
        cycle_number = cycle_number+1;
        plotter.append([cycle_number,PC])
        type = decode(instruction)
        if type == "F":
            halted = True
            reg_encoding["111"] = flag_reset
            dumpPC_REG()
            print()
        elif type == "A":
            reg_encoding["111"] = flag_reset
            rD, r1, r2 = parameter_based_on_type(instruction, "A")
            op = op_table[instruction[:5]]
            ans = 0
            if op == "add":
                ans = reg_encoding[r1] + reg_encoding[r2]
            elif op == "sub":
                ans = reg_encoding[r1] - reg_encoding[r2]
            elif op == "mul":
                ans = reg_encoding[r1] * reg_encoding[r2]
            elif op == "xor":
                ans = reg_encoding[r1] ^ reg_encoding[r2]
            elif op == "and":
                ans = reg_encoding[r1] & reg_encoding[r2]
            elif op == "or":
                ans = reg_encoding[r1] | reg_encoding[r2]
            if checkOverflow(ans):
                #made these if and else statements
                if(op=="add" or op == "mul"):
                    binary = convert16bin(ans)
                    dec = int(binary,2)
                    reg_encoding[rD] = dec
                else:
                    reg_encoding[rD] = 0
            else:
                reg_encoding[rD] = ans
            dumpPC_REG()
            print()
            PC += 1

        elif type == "B":
            reg_encoding["111"] = flag_reset
            r1, imm = parameter_based_on_type(instruction, "B")
            imm = int(imm, 2)
            op = op_table[instruction[:5]]
            if op == "mov_im":
                reg_encoding[r1] = imm
            elif op == "rs":
                reg_encoding[r1] = reg_encoding[r1] >> imm
            elif op == "ls":
                reg_encoding[r1] = reg_encoding[r1] << imm
            dumpPC_REG()
            print()
            PC += 1

        elif type == "C":
            r3, r4 = parameter_based_on_type(instruction, "C")
            op = op_table[instruction[:5]]
            if op == "mov":
                if r4 == "111":
                    reg_encoding[r3] = int(reg_encoding[r4], 2)
                else:
                    reg_encoding[r3] = reg_encoding[r4]
            elif op == "div":
                temp = reg_encoding[r3]
                reg_encoding["000"] = int(reg_encoding[r3] / reg_encoding[r4])
                reg_encoding["001"] = int(temp % reg_encoding[r4])
            elif op == "not":
                reg_encoding[r3] = pow(2,16) - 1 - reg_encoding[r4]
            elif op == "cmp":
                if int(reg_encoding[r3]) > int(reg_encoding[r4]):
                    reg_encoding["111"] = "000000000000" + "0010"
                elif int(reg_encoding[r3]) < int(reg_encoding[r4]):
                    reg_encoding["111"] = "000000000000" + "0100"
                elif int(reg_encoding[r3]) == int(reg_encoding[r4]):
                    reg_encoding["111"] = "000000000000" + "0001"
            if op != "cmp":
                reg_encoding["111"] = flag_reset
            dumpPC_REG()
            print()
            PC += 1

        elif type == "D":
            reg_encoding["111"] = flag_reset
            r1, var = parameter_based_on_type(instruction, "D")
            op = op_table[instruction[:5]]
            if op == "ld":
                #added this for plotting
                plotter.append([cycle_number,int(var, 2)])
                reg_encoding[r1] = int(MEM[int(var, 2)], 2)
            elif op == "st":
                #added this for plotting
                plotter.append([cycle_number,int(var, 2)])
                MEM[int(var, 2)] = convert16(reg_encoding[r1])
            dumpPC_REG()
            print()
            PC += 1


        elif type == "E":
            label = parameter_based_on_type(instruction, "E")
            # getval will convert the 8 bit label address to decimal
            label_add = int(label,2)
            op = op_table[instruction[:5]]
            if op == "jmp":
                reg_encoding["111"] = flag_reset
                dumpPC_REG()
                print()
                PC = label_add
            elif op == "jlt":
                if reg_encoding["111"][-3] == "1":
                    reg_encoding["111"] = flag_reset
                    dumpPC_REG()
                    print()
                    PC = label_add
                else:
                    reg_encoding["111"] = flag_reset
                    dumpPC_REG()
                    print()
                    PC += 1
            elif op == "jgt":
                if reg_encoding["111"][-2] == "1":
                    reg_encoding["111"] = flag_reset
                    dumpPC_REG()
                    print()
                    PC = label_add
                else:
                    reg_encoding["111"] = flag_reset
                    dumpPC_REG()
                    print()
                    PC += 1
            elif op == "je":
                if reg_encoding["111"][-1] == "1":
                    reg_encoding["111"] = flag_reset
                    dumpPC_REG()
                    print()
                    PC = label_add
                else:
                    reg_encoding["111"] = flag_reset
                    dumpPC_REG()
                    print()
                    PC += 1


MEM = []
PC = 0
plotter = []
# changed slightly here
# reg = {"R0":0, "R1":0, "R2":0, "R3":0, "R4":0, "R5":0, "R6":0, "FLAGS":"0000000000000000"}
var_value = {}
reg_encoding = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": "0000000000000000"}

# I could've stored the type as well but I made a separate function for that reason this dictionary was getting larger incresed possibility of error in entering data

op_table = {"00000": "add", "00001": "sub", "00010": "mov_im", "00011": "mov", "00100": "ld", "00101": "st",
            "00110": "mul", "00111": "div", "01000": "rs", "01001": "ls", "01010": "xor", "01011": "or", "01100": "and",
            "01101": "not", "01110": "cmp", "01111": "jmp", "10000": "jlt", "10001": "jgt", "10010": "je",
            "10011": "hlt"}
flag_reset = "0000000000000000"


def main():
    while True:
        s = ""
        try:
            inp = input()
            #rstrip will remove /r from the end of file
            s = inp.rstrip()
            # change this
            if s != "":
                MEM.append(s)
        except EOFError:
            break
    for i in range(len(MEM), 256):
        MEM.append("0000000000000000")
    # be careful about divide instruction
    execute()
    dumpMEM()

    #plotting part:
    xs = [x[0] for x in plotter]
    ys = [x[1] for x in plotter]
    plt.xlabel("Cycles")
    plt.ylabel("Address")
    plt.title("Memory Address v/s Cycles")
    plt.scatter(xs, ys)
    plt.show()


if __name__ == "__main__":
    main()
