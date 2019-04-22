"""Read bit stream."""
from collections import defaultdict
from collections import deque

from bitstring import ConstBitStream


from . import jvpm_dict, jvpm_methods, read_attribute, CPInfo  # import external opcode dictionary

# A deque of invokevirtual constants used for method calls from AddToo.class.
#     Eventually wee will acquire these values from the CP, but they are hardcoded for now.
INVOKEVIRTUAL_CONST = deque(["5", "5", "7"])

# ****************************************************************************************

class HeaderClass():

    """Class that parses the header data from .class file and assigns values to variables."""
    def __init__(self, name="jvpm/javafiles/test.class"):
        self.name = name
        self.bits = ConstBitStream(filename=name)
        add_one_byte = 1
        constant_pool_byte_size = 0
        with open(name, 'rb') as binary_file:
            self.data = binary_file.read()
            self.temp_2 = defaultdict(list)
            self.constant_pool = defaultdict(list)
            self.constant_pool_byte_size = 0
            self.constant_pool_total_size = 0
            self.constant_pool_indexes = []
            self.skips_in_constant_pool = 0
            self.add_one_byte = 1
            self.reader_location = 0
            self.integer_interface_count = 0
            self.integer_field_count = 0
            self.integer_method_count = 0
            self.methods_table =defaultdict(list)
            self.op_codes = []
            self.integer_attribute_count = 0
            self.field_count = 0
            self.field_dictionary = defaultdict(list)

    def get_magic(self):
        magic = self.bits.read('hex:32')
        return magic

    def get_minor(self):
        return self.bits.read('hex:16')

    def get_major(self):
        return self.bits.read('hex:16')

    def get_const_pool_count(self):
        return self.bits.read('uint:16')

    def get_const_pool(self):
        constants_pool = defaultdict(list)
        constants_pool[0].append("base")
        const_pool_count = self.get_const_pool_count()
        const_pool_count -= 1
        i = 1
        while i <= const_pool_count:
            constant = CPInfo.ConstInfo().read(self.bits)
            constants_pool[i]=(constant)
            if constant[0] == "06" or constant[0] == "05":
                self.skips_in_constant_pool += 1
                i += 1

            i += 1
        self.reader_location = self.bits.bytepos
        self.constant_pool = constants_pool

        return constants_pool



    def get_access_flags(self):
        access_flag_position = self.reader_location
        access_flag = [format((self.data[access_flag_position]) , "02x")]
        access_flag.append(format((self.data[access_flag_position + self.add_one_byte]), "02x"))
        self.reader_location += 2

        return access_flag

    def get_this_class(self):
        this_class = [format((self.data[self.reader_location]) , "02x")]
        this_class.append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
        self.reader_location += 2
        return this_class

    def get_super_class(self):
        super_class = [format((self.data[self.reader_location]) , "02x")]
        super_class.append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
        self.reader_location += 2
        return super_class

    def get_interfaces_count(self):
        interface_count = [format((self.data[self.reader_location]) , "02x")]
        interface_count.append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
        self.integer_interface_count = (self.data[self.reader_location]) + (self.data[self.reader_location + self.add_one_byte])
        self.reader_location += 2
        return interface_count

    def get_interface(self):
        if (self.integer_interface_count == 0):
            print ("interface table empty")


    def get_field_count(self):
        field_count = [format((self.data[self.reader_location]) , "02x")]
        field_count.append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
        self.integer_field_count = (self.data[self.reader_location]) + (self.data[self.reader_location + self.add_one_byte])
        self.reader_location += 2
        self.field_count = field_count
        return field_count


    def get_field(self):
        dictionary_index  = 0

        if (self.integer_field_count == 0):
            print("field table empty")

        else:
            x=0
            for i in range(self.field_count):
                field = []
                field.clear()






    def get_methods_count(self):
        method_count = [format((self.data[self.reader_location]) , "02x")]
        method_count.append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
        self.integer_method_count = (self.data[self.reader_location]) + (self.data[self.reader_location + self.add_one_byte])
        self.reader_location += 2
        return method_count

    def get_methods(self, pool):
        if (self.integer_method_count == 0):
            print("method table empty")

        method_index = 0
        while method_index <  self.integer_method_count:
            ################# access flags
            self.methods_table[method_index].append(format((self.data[self.reader_location]), "02x"))
            self.methods_table[method_index].append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
            self.reader_location += 2
            ################### name index
            self.methods_table[method_index].append(format((self.data[self.reader_location]), "02x"))
            self.methods_table[method_index].append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
            self.reader_location += 2
            ################# discriptor index
            self.methods_table[method_index].append(format((self.data[self.reader_location]), "02x"))
            self.methods_table[method_index].append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
            self.reader_location += 2
            ################## attribute count
            self.methods_table[method_index].append(format((self.data[self.reader_location]), "02x"))
            self.methods_table[method_index].append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
            attribute_count = (self.data[self.reader_location]) + (self.data[self.reader_location + self.add_one_byte])

            self.reader_location += 2
            attribute_index = 0

            while attribute_index < attribute_count:
                tag_location = (self.data[self.reader_location]) + (self.data[self.reader_location + self.add_one_byte])
                tag = pool[tag_location]
                atribute_reader = read_attribute.ReadAttribute()
                returned_vals = atribute_reader.get_attribute(tag, self.methods_table, self.reader_location, self.data, self.op_codes, method_index, pool)

                if (isinstance(returned_vals, int)):
                    self.reader_location = returned_vals
                else:
                    self.reader_location = int(returned_vals[0])
                    self.op_codes = returned_vals[1]

                attribute_index += 1


            method_index +=1
        return self.op_codes


    def get_attribute_count(self):
        attribute_count = [format((self.data[self.reader_location]) , "02x")]
        attribute_count.append(format((self.data[self.reader_location + self.add_one_byte]), "02x"))
        self.integer_attribute_count = (self.data[self.reader_location]) + (self.data[self.reader_location + self.add_one_byte])
        self.reader_location += 2
        return attribute_count

    def get_attribute_table(self):
        x = 3
        atribute_reader = read_attribute.ReadAttribute()






class OpCodes():

    """Parse Opcodes into an array from the .class file, search the external dictionary of
    opcodes, and implement the methods using the external dictionary of methods."""
    def __init__(self, opcode, constantpool):
        # Eventually we will acquire these values from the CP, but they are hardcoded for now.
        #self.opcodes = ['2a', '59', '4c', '2b', 'b6', '3d', 'b6', '3e', '1c', '1d', '60', 'b6']
        self.constantpool = constantpool
        self.opcodes = opcode

        """


        METHOD GOES HERE TO FIND OPCODES FROM ANY .CLASS FILE AND SAVE TO self.opcodes LIST.



        """

    def dict_search(self):
        """dictionary search method."""
        #print(self.opcodes, " = opcodes        ", self.constantpool, " = const pool")

        i = 0
        while i < len(self.opcodes):
            #print(self.opcodes[i], " &&&&&&&&&& op code i &&&&&&&&&")
        # opcode in self.opcodes:
            opcall = jvpm_dict.get_opcode(self.opcodes[i])
            #print(opcall, " = translated opcode")
            if opcall == "invokevirtual":
                op_location = int(self.opcodes[i+2])
                #print(op_location, "oplocation +2", type(op_location))
                jvpm_methods.OpCodeMethods().token_dict(opcall,op_location,self.constantpool)

            elif opcall != "Byte code not found!":
                jvpm_methods.OpCodeMethods().token_dict(opcall,self.opcodes,self.constantpool)
            i += 1

