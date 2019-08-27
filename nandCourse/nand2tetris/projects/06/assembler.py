import re
import sys
import const

class Assembler:
    def __init__(self, asm_file):
        self.asm_file = asm_file
        self.output_file = self._get_out_file(asm_file)
        self.symbol_table = const.BASE_SYMBOLS
        self.symbol_address = const.ADDRESS_START
        self.comp_codes = const.COMP_CODES
        self.dest_codes = const.DEST_CODES
        self.jump_codes = const.JUMP_CODES
        self.cur_line = 0
    
    def read_file(self):
        with open(self.asm_file, 'r') as f:
            self.file_lines = f.readlines()
    
    @staticmethod
    def _get_out_file(in_file):
        if in_file.endswith('.asm'):
            return in_file.replace('.asm', '.hack')
        else:
            return in_file + '.hack'
    
    @staticmethod
    def _bits(num):
        return bin(int(num))[2:]
    
    def add_symbol_entry(self, symbol, address):
        self.symbol_table[symbol] = address

    def symbol_table_contains(self, symbol):
        return symbol in self.symbol_table

    def get_symbol_table_address(self, symbol):
        return self.symbol_table[symbol]
    
    def _get_address(self, symbol):
        """Return symbol address"""
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbol_table_contains(symbol):
                self.add_symbol_entry(symbol, self.symbol_address)
                self.symbol_address += 1
            return self.get_symbol_table_address(symbol)
    
    def get_command_type(self, command):
        if re.match(r'^@.*', command):
            return const.A_COMMAND
        elif re.match(r'^\(.*', command):
            return const.L_COMMAND
        else:
            return const.C_COMMAND
    
    def gen_a_code(self, address):
        return '0' + self._bits(address).zfill(15)

    def gen_c_code(self, comp, dest, jump):
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)

    def dest(self, dest):
        return self._bits(self.dest_codes.index(dest)).zfill(3)

    def comp(self, comp):
        return self.comp_codes[comp]

    def jump(self, jump):
        return self._bits(self.jump_codes.index(jump)).zfill(3)
    
    @staticmethod
    def get_symbol(command):
        matching = re.match(r'^[@\(](.*?)\)?$', command)
        symbol = matching.group(1)
        return symbol
    
    @staticmethod
    def get_dest(command):
        matching = re.match(r'^(.*?)=.*$', command)
        if not matching:
            dest = ''
        else:
            dest = matching.group(1)
        return dest
    
    @staticmethod
    def get_comp(command):
        comp = re.sub(r'^.*?=', '', command) # remove dest
        comp = re.sub(r';\w+$', '', comp) # remove jump
        return comp.strip()

    @staticmethod
    def get_jump(command):
        matching = re.match(r'^.*;(\w+)$', command)
        if not matching:
            jump = ''
        else:
            jump = matching.group(1)
        return jump
    
    def first_pass(self):
        """First pass to construct symbol table"""
        cur_address = 0
        for line_num, line in enumerate(self.file_lines):
            line = const.COMMENT.sub('', line)
            if line == '\n':
                continue
            command = line.strip()
            command_type = self.get_command_type(command)
            if command_type == const.A_COMMAND or \
                    command_type == const.C_COMMAND:
                cur_address += 1
            elif command_type == const.L_COMMAND:
                symbol = self.get_symbol(command)
                self.symbol_table[symbol] = cur_address
    
    def second_pass(self):
        output_file = open(self.output_file, 'w')
        for line_num, line in enumerate(self.file_lines):
            line = const.COMMENT.sub('', line)
            if line == '\n':
                continue
            command = line.strip()
            command_type = self.get_command_type(command)
            if command_type == const.A_COMMAND:
                symbol = self.get_symbol(command)
                address = self._get_address(symbol)
                output_file.write(self.gen_a_code(address) + '\n')
            elif command_type == const.C_COMMAND:
                cur_dest = self.get_dest(command)
                cur_comp = self.get_comp(command)
                cur_jump = self.get_jump(command)
                c_code = self.gen_c_code(cur_comp, cur_dest, cur_jump)
                output_file.write(c_code + '\n')
            elif command_type == const.L_COMMAND:
                pass
        output_file.close()
    
    def assemble(self):
        self.first_pass()
        self.second_pass()

def main():
    try:
        asm_file = sys.argv[1]
    except IndexError:
        print("Format to run: assembler.py file.asm")
    
    assembler = Assembler(asm_file)
    assembler.read_file()
    assembler.assemble()

main()
