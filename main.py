# Project 2
# Eric Moravek
# 3/6/21

import PySimpleGUI as sg

# sg.theme('DarkBlack')  # Set the Color of the main_gui
sg.theme('Reddit')


# Read in the data from file, converts hex to bin
# and stores in then returns a binary list
def read_file():
    f = open('prog.asm')
    lines = f.readlines()
    f.close()

    bin_list = []
    for ln in lines:
        bin_list.append(hex_to_bin(ln))

    return bin_list


# Write past list to file called output.txt
def write_file(list_write):
    f = open('output.txt', 'w')

    for n in list_write:

        # Insert Label
        if n in label_dict.values():
            f.write("{}\n".format((reversed_label_dict[n] + ':')))

        f.write("{}: {}\n".format(n, list_write[n]))

    f.close()
    print("Output saved to 'output.txt'")


# Writs registers to file
def write_reg_file(list_write):
    f = open('reg_output.txt', 'w')

    for n in list_write:
        f.write("{}:{}\n".format(n, list_write[n]))

    f.close()
    print("Output saved to 'reg_output.txt'")


# Write Data memory to file
def write_dm_file(list_write):
    f = open('data_mem.txt', 'w')
    f.write("DM : Value\n")

    for n in list_write:
        f.write("{}:{}\n".format(n, list_write[n]))

    f.close()
    print("Output saved to 'data_mem.txt'")


# Takes a string in hex and returns a binary string
def hex_to_bin(c):
    b = ''
    # separating and converting each hex character into bin and adding it to the string b
    for i in range(8):  # i = 0, 1, ... , 7

        b += bin(int(c[i], base=16))[2:].zfill(4)

    return b


# covert binary sting to 2's complement binary string
def twos_comp(x):
    rightmost1_idx = -1
    for i in range(len(x) - 1, -1, -1):

        if x[i] == '1':
            rightmost1_idx = i
            break

    y_same = x[rightmost1_idx:]
    y_flip = ""
    for i in range(rightmost1_idx):
        y_flip += str(1 - int(x[i]))
    y = y_flip + y_same
    return y


# Converts Negative or positive binary numbers do decimal numbers
def bin_to_dec(bin_string):
    # if MSB is 1 its negative
    if bin_string[0:1] == "1":
        b = twos_comp(bin_string)
        d = int(b, 2)
        d = -1 * d
        return d
    # if MSB is 0 its positive
    else:
        d = int(bin_string, 2)
        return d


# convert int to a binary string of 5 bits
def int_to_5bin_string(i):
    if i >= 0:
        s = bin(i)[2:].zfill(5)
    else:  # neg number
        t = bin(0 - i)[2:].zfill(5)
        s = twos_comp(t)
    return s


# convert in to a binary string of 16 bits
def int_to_16bin_string(i):
    if i >= 0:
        s = bin(i)[2:].zfill(16)
    else:  # neg number
        t = bin(0 - i)[2:].zfill(16)
        s = twos_comp(t)
    return s


# Global Variable because python doesnt support pass by value or pointers
label_dict = {}
reversed_label_dict = {}


# Disassembles a passed list of binary instructions and stores them in a dictionary
# indexed by pc values.
def disassembler(lines):
    pc = 0
    lc = 0

    asm_inst = {}

    for ln in lines:

        op = ln[0:6]

        # parse the opcode
        if op == "000000":  # R type instruction
            func = ln[26:32]
            rs = str(int(ln[6:11], 2))
            rt = str(int(ln[11:16], 2))
            rd = str(int(ln[16:21], 2))
            sh = str(int(ln[21:26], 2))

            # if statements for each of the instructions
            if func == "100000":
                opcode = 'add'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            elif func == "100010":
                opcode = 'sub'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            elif func == "100100":
                opcode = 'and'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            elif func == "100101":
                opcode = 'or'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            elif func == "010111":
                opcode = 'nor'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            elif func == "100110":
                opcode = 'xor'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            elif func == "000000":
                opcode = 'sll'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rt + ", " + sh

            elif func == "000010":
                opcode = 'srl'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rt + ", " + sh

            elif func == "101010":
                opcode = 'slt'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt

            # Special Instruction
            elif func == '110111':
                opcode = 'comp'
                asm_inst[pc] = opcode + " $" + rd + ", $" + rs + ", $" + rt


        elif op == "000010":  # J type instruction
            opcode = 'j'

            imm = bin_to_dec(ln[16:32])
            addr = 4 * imm

            label = "label_" + str(lc)
            label_dict[label] = addr
            reversed_label_dict[addr] = label

            lc += 1

            asm_inst[pc] = opcode + " " + label

        else:
            rs = str(int(ln[6:11], 2))
            rt = str(int(ln[11:16], 2))
            imm = str(bin_to_dec(ln[16:32]))
            # print("imm: " + imm + " " + ln[16:32])

            # I type instruction
            if op == "001000":
                opcode = "addi"

                asm_inst[pc] = opcode + " $" + rt + ", $" + rs + ", " + imm
            elif op == "001100":
                opcode = "andi"
                asm_inst[pc] = opcode + " $" + rt + ", $" + rs + ", " + imm

            elif op == "001101":
                opcode = "ori"
                asm_inst[pc] = opcode + " $" + rt + ", $" + rs + ", " + imm

            elif op == "001110":
                opcode = "xori"
                asm_inst[pc] = opcode + " $" + rt + ", $" + rs + ", " + imm

            elif op == "000100":
                opcode = "beq"

                # Create label for label dict
                addr = pc + 4 + 4 * int(imm)

                label = "label_" + str(lc)
                lc += 1

                # Store the labels into two dictionaries
                label_dict[label] = addr
                reversed_label_dict[addr] = label

                asm_inst[pc] = opcode + " $" + rt + ", $" + rs + ", " + label


            elif op == "000101":
                opcode = "bne"

                # Create label for label dict
                addr = pc + 4 + 4 * int(imm)

                label = "label_" + str(lc)
                lc += 1
                label_dict[label] = addr
                reversed_label_dict[addr] = label

                asm_inst[pc] = opcode + " $" + rt + ", $" + rs + ", " + label

            elif op == "100011":
                opcode = "lw"
                asm_inst[pc] = opcode + " $" + rt + ", " + imm + "($" + rs + ")"

            elif op == "101011":
                opcode = "sw"
                asm_inst[pc] = opcode + " $" + rt + ", " + imm + "($" + rs + ")"

            elif op == "001111":
                opcode = "lui"
                asm_inst[pc] = opcode + " $" + rt + ", " + str(hex(int(imm)))

        pc += 4

    return asm_inst


def parser(i):
    i = i.replace(',', '')
    i = i.replace('$', '')
    i = i.replace('(', ' ')
    i = i.replace(')', '')
    i = i.split(' ')
    return i


def simulator(instr_mem, bin_instr):
    # Get Run Mode of the program
    step_flag = select_run_mode()

    pc = 0

    reg = {}
    for i_prime in range(0, 31):  # Initialize all registers to 0
        name = "$" + str(i_prime)
        reg[name] = 0
    reg["hi"] = 0
    reg["lo"] = 0

    data_mem = {}
    # Initialize all data memory address's in the range 0x2000 to 0x3000 to zero
    for addr_prime in range(0x2000, 0x3000, 4):
        data_mem[addr_prime] = 0

    # instruction type for the print statement
    instr_type = ''

    # instruction string for passing to print function
    instr_str = ''

    # Statistics Variable Array
    # stats_list = [instruction_count, alu_count, j_type, branch_count, memory_count, other_count]
    stats_list = [0, 0, 0, 0, 0, 0]

    # Last instruction used as a key for loop
    last_key = list(instr_mem)[-1]

    # register Key List
    reg_key = list(reg.keys())
    dm_key = list(data_mem.keys())

    reg_list = []
    t_list = []
    for i in reg_key:
        reg_list.append([i, reg[i]])

    for n in range(8192, 12288, 32):
        t_list.append([n, data_mem[int(n)], data_mem[int(n) + 4], data_mem[int(n) + 8], data_mem[int(n) + 12],
                       data_mem[int(n) + 16], data_mem[int(n) + 20], data_mem[int(n) + 24], data_mem[int(n) + 28]])

    # Main window code setup
    layout = [[sg.Text('Step by Step Mode Instructions', size=(30, 1), k='-T1-'),
               sg.T("Register", justification='r', k='-T2-')],
              [sg.Multiline(size=(66, 20), key='-OUTPUT-' + sg.WRITE_ONLY_KEY, write_only=True, autoscroll=True),
               sg.Table(values=reg_list, key='-REG-', headings=["Register", "Value"], vertical_scroll_only=True,
                        auto_size_columns=True, num_rows=30,alternating_row_color='light blue')],
              [sg.T("Data Memory", key='-T3-')],
              [sg.Table(values=t_list, headings=["Address", "Value(+0)", 'Value(+4)', 'Value(+8)', 'Value(+12)',
                                                 'Value(+16)', 'Value(+20)', 'Value(+24)', 'Value(+28)'], key='-DM-',
                        vertical_scroll_only=True,
                        )],
              [sg.Button('Exit'), sg.Button('Next', k='-NEXT-', bind_return_key=True, enable_events=True)]]

    window = sg.Window("Project 2: Mars Simulator - Eric Moravek", layout, finalize=True, resizable=True)
    window['-REG-'].expand(True, True, True)
    window['-DM-'].expand(True, True, True)
    window['-OUTPUT-' + sg.WRITE_ONLY_KEY].expand(True, True, True)
    window['-T1-'].expand(True, True, True)
    window['-T2-'].expand(True, True, True)
    window['-T3-'].expand(True, True, True)

    while pc < last_key + 4:  # While loop to step through the program instruction memory

        window.refresh()

        # parse out the current instruction to an easily accessible list
        instr = parser(instr_mem[pc])

        # Operation if statements
        # Immediate type
        if instr[0] == "addi":
            instr_type = 'i'
            stats_list[1] += 1
            rt = '$' + str(instr[1])
            reg[rt] = reg['$' + str(instr[2])] + int(instr[3])

        elif instr[0] == "andi":
            instr_type = 'i'
            stats_list[1] += 1
            rt = '$' + str(instr[1])
            reg[rt] = reg['$' + str(instr[2])] & int(instr[3])

        elif instr[0] == "xori":
            instr_type = 'i'
            stats_list[1] += 1
            rt = '$' + str(instr[1])
            reg[rt] = reg['$' + str(instr[2])] ^ int(instr[3])

        elif instr[0] == "ori":
            instr_type = 'i'
            stats_list[1] += 1
            rt = '$' + str(instr[1])
            if type(reg['$' + str(instr[2])]) == str:
                # noinspection PyTypeChecker
                reg[rt] = int(reg['$' + str(instr[2])], 16) | int(instr[3])
            else:
                reg[rt] = reg['$' + str(instr[2])] | int(instr[3])

        elif instr[0] == "lui":
            instr_type = 'i'
            stats_list[1] += 1

            rt = '$' + str(instr[1])
            reg[rt] = hex(int(instr[2] + "0000", 16))

        elif instr[0] == "beq":
            instr_type = 'i'
            stats_list[3] += 1

            # Compare and update pc if needed
            if reg['$' + str(instr[1])] == reg['$' + str(instr[2])]:
                pc = label_dict[instr[3]] - 4



        elif instr[0] == "bne":
            instr_type = 'i'
            stats_list[3] += 1

            # Compare and update pc if needed
            if reg['$' + str(instr[1])] != reg['$' + str(instr[2])]:
                pc = label_dict[instr[3]] - 4

        # Data memory instructions
        elif instr[0] == "lw":
            instr_type = 'i'
            stats_list[4] += 1

            rt = '$' + str(instr[1])
            # make sure not to overwrite register 0
            if rt != '$0':
                reg[rt] = data_mem[int(reg['$' + str(instr[3])] + int(instr[2]))]

        elif instr[0] == "sw":
            instr_type = 'i'
            stats_list[4] += 1

            rt = '$' + str(instr[1])
            # make sure not to overwrite register 0
            if rt != '$0':
                data_mem[int(reg['$' + str(instr[3])] + int(instr[2]))] = reg[rt]

        # R-Type instructions
        elif instr[0] == "add":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            # Rd = Rs + Rt
            reg[rd] = reg['$' + str(instr[2])] + reg['$' + str(instr[3])]

        elif instr[0] == "sub":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            # Rd = Rs - Rt
            reg[rd] = reg['$' + str(instr[2])] - reg['$' + str(instr[3])]

        elif instr[0] == "and":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            # Rd = Rs & Rt
            reg[rd] = reg['$' + str(instr[2])] & reg['$' + str(instr[3])]

        elif instr[0] == "or":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            # Rd = Rs | Rt
            reg[rd] = reg['$' + str(instr[2])] | reg['$' + str(instr[3])]

        elif instr[0] == "nor":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            # Rd = ~(Rs | Rt)
            reg[rd] = ~(reg['$' + str(instr[2])] | reg['$' + str(instr[3])])

        elif instr[0] == "xor":
            stats_list[1] += 1
            instr_type = 'r'
            rd = '$' + str(instr[1])
            # Rd = Rs ^ Rt
            reg[rd] = reg['$' + str(instr[2])] ^ reg['$' + str(instr[3])]

        elif instr[0] == "slt":
            stats_list[5] += 1
            instr_type = 'r'
            rd = '$' + str(instr[1])
            # Rd = Rs < Rt

            if reg['$' + str(instr[2])] < reg['$' + str(instr[3])]:
                reg[rd] = 1
            else:
                reg[rd] = 0

        elif instr[0] == "sll":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            reg[rd] = reg['$' + str(instr[2])] << int(instr[3])

        elif instr[0] == "srl":
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            reg[rd] = reg['$' + str(instr[2])] >> int(instr[3])


        # Jump instructions
        elif instr[0] == "j":
            stats_list[2] += 1
            instr_type = 'j'
            # Fetch the jump addr from the label in instr
            imm = label_dict[instr[1]]
            # Update PC with the immediate value
            pc = imm - 4

        # Special Instruction Type
        elif instr[0] == 'comp':
            instr_type = 'r'
            stats_list[1] += 1
            rd = '$' + str(instr[1])
            rt = reg['$' + str(instr[3])]
            rs = reg['$' + str(instr[2])]

            rt_bin = int_to_16bin_string(rt)
            rs_bin = int_to_16bin_string(rs)
            sim = 0

            # step through and find the similar bits
            for n in range(16):
                if rs_bin[n] == rt_bin[n]:
                    sim += 1

            # Store the number of similar bits
            reg[rd] = sim

        # if step flag is set then prepare the instruction strings to be printed
        if step_flag == 'step':

            # indexing adjustment variable
            x = int(pc / 4)

            # J-type instructions
            if instr_type == 'r':

                instr_str = ("opcode = " + str(bin_instr[x][0:6]) + ' rs = ' + str(bin_instr[x][6:11])
                             + ' rt = ' + str(bin_instr[x][11:16]) + ' rd = ' + str(bin_instr[x][16:21])
                             + ' sh = ' + bin_instr[x][21:26] + ' func = ' + str(bin_instr[x][26:32]))

            # I-type instructions
            elif instr_type == 'i':

                instr_str = ("opcode = " + str(bin_instr[x][0:6]) + ' rs = ' + str(bin_instr[x][6:11]) + " rt = "
                             + str(bin_instr[x][11:16]) + ' imm = ' + bin_instr[x][16:32])

            # J-type instructions
            elif instr_type == 'j':

                instr_str = ("opcode = " + str(bin_instr[x][0:6]) + ' imm = ' + str(bin_instr[x][6:32]))

        if step_flag == 'step':

            while True:  # Event Loop
                event, values = window.read()

                reg_string = ''
                dm_string = ''
                # If exit is pressed or window is closed close the window and break loop
                if event == sg.WIN_CLOSED or event == 'Exit':
                    window.close()
                    break

                if event == '-NEXT-':
                    # Print our Binary Instruction Information

                    window['-OUTPUT-' + sg.WRITE_ONLY_KEY].update(
                        window['-OUTPUT-' + sg.WRITE_ONLY_KEY].get() + "PC: " +
                        str(pc) + "\n" + instr_str + "\nASM: " + instr_mem[pc] + "\n")
                    for i in reg_key:
                        reg_string += (str(i) + ": " + str(reg[i]) + "\n")


                    reg_list.clear()
                    for i in reg_key:
                        reg_list.append([i, reg[i]])

                    window['-REG-'].update(values=reg_list)

                    # Reset the Table List
                    t_list.clear()
                    for n in range(8192, 12288, 32):
                        print("N: ", n)

                        t_list.append(
                            [n, data_mem[int(n)], data_mem[int(n) + 4], data_mem[int(n) + 8], data_mem[int(n) + 12],
                             data_mem[int(n) + 16], data_mem[int(n) + 20], data_mem[int(n) + 24],
                             data_mem[int(n) + 28]])

                    window['-DM-'].update(values=t_list)
                    window.refresh()
                    break

                if pc == last_key + 4:
                    window.close()
                    break

                window.refresh()


        stats_list[0] += 1
        # Update to the next instruction
        pc += 4

    # Non-stop mode, print register content with pc, dm content, and statistics
    if step_flag.lower() != 'step':
        print("Reg: ", reg)
        print("DM: ", data_mem)

    # Print the stats
    stats_window(stats_list)

    stats(stats_list)

    write_reg_file(reg)
    write_dm_file(data_mem)

    return 0


# Prints out the stats and instruction count Fixme Delete Later bec its Redundant
def stats(arr):
    print()  # Newline for break
    print("Total: ".rjust(8), str(arr[0]).center(5), " % Total".ljust(9))
    print("ALU: ".rjust(8), str(arr[1]).center(5), " %", str(round((arr[1] / arr[0]) * 100, 2)).ljust(8))
    print("Jump: ".rjust(8), str(arr[2]).center(5), " %", str(round((arr[2] / arr[0]) * 100, 2)).ljust(8))
    print("Branch: ".rjust(8), str(arr[3]).center(5), " %", str(round((arr[3] / arr[0]) * 100, 2)).ljust(8))
    print("Memory: ".rjust(8), str(arr[4]).center(5), " %", str(round((arr[4] / arr[0]) * 100, 2)).ljust(8))
    print("Other: ".rjust(8), str(arr[5]).center(5), " %", str(round((arr[5] / arr[0]) * 100, 2)).ljust(8))


# Prints out the stats and instruction count
def stats_window(arr):
    # Set up the layout for the Statistics Window
    left_col = [[sg.T("Total: " + str(arr[0]))], [sg.T("ALU: " + str(arr[1]))], [sg.T("Jump: " + str(arr[2]))],
                [sg.T("Branch: " + str(arr[3]))], [sg.T("Memory: " + str(arr[4]))], [sg.T("Other: " + str(arr[5]))]]
    right_col = [[sg.T("% of Total")], [sg.T(str(round((arr[1] / arr[0]) * 100)) + "%")],
                 [sg.T(str(round((arr[2] / arr[0]) * 100)) + "%")],
                 [sg.T(str(round((arr[3] / arr[0]) * 100)) + "%")],
                 [sg.T(str(round((arr[4] / arr[0]) * 100)) + "%")],
                 [sg.T(str(round((arr[5] / arr[0]) * 100)) + "%")]]

    layout2 = [[sg.T("Statistics")], [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
               [sg.Text('', pad=(0, 0), key='-EXPAND2-'),
                sg.Column(left_col, vertical_alignment='c', justification='l', key='-l-'),
                sg.Column(right_col, vertical_alignment='c', justification='r', key='-r-')],
               [sg.Button("Exit", bind_return_key=True)]]

    window = sg.Window('MARS Simulator - Statistics', layout2, element_justification='c',
                       resizable=True, finalize=True)
    window['-l-'].expand(True, True, True)
    window['-r-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)

    # One Shot main_gui Wait for exit to be called
    while True:
        event, values = window.read()

        # if user closes window or exit cancel and close window
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break


# Delete if not needed
def sign_extension(bin_str, length):
    # find MSB
    if bin_str[0] == 1:
        # Sign extend to length
        for i in range(length):
            bin_str = '1' + bin_str


    elif bin_str[0] == 0:
        for i in range(length):
            bin_str = '1' + bin_str

    return bin_str


# Selects Run Mode of the program with main_gui interface
def select_run_mode():
    # All the stuff inside your window.

    layout = [[sg.Text('Select Program Mode', k='expand1')],
              [sg.Radio("Step by Step Mode", "RADIO1", default=False, k='-RADIO1-')],
              [sg.Radio("Free Run Mode", "RADIO1", default=False, k='-RADIO2-')],
              [sg.Button('Exit', auto_size_button=True),
               sg.Button('Enter', auto_size_button=True, bind_return_key=True)]]

    # Create the Window
    window = sg.Window('MARS Simulator', layout, finalize=True, resizable=True, element_padding=(10, 5),
                       element_justification='c')
    window['expand1'].expand(True, True, True)
    window['-RADIO1-'].expand(True, True, True)
    window['-RADIO2-'].expand(True, True, True)

    run_mode = ''
    while True:
        event, values = window.read()

        # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            break
        if event == 'Enter':

            if values['-RADIO1-']:
                run_mode = 'step'
                window.close()

            elif values['-RADIO2-']:
                run_mode = 'free'
                window.close()

    return run_mode


def main():
    bin_list = read_file()
    asm_instr = disassembler(bin_list)
    write_file(asm_instr)

    simulator(asm_instr, bin_list)

    return 0


main()
