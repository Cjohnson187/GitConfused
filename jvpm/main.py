import sys
import packages
import argparse

# ****************************************************************************************

if '__main__' == __name__:                  #pragma: no cover
    
    #Temporarily removing thisline below to show we are running java class files in the command line
    #file_name = ("jvpm/javafiles/" + str(sys.argv[1]) + ".class")
    file_name = ("jvpm/javafiles/" + str(sys.argv[1]))
    header_class_object = packages.jvpm_opcodes.HeaderClass(name = file_name)
    header_class_object.get_magic()
    header_class_object.get_minor()
    header_class_object.get_major()
    get_cp = header_class_object.get_const_pool()
    p_translator = packages.pool_translate.PoolTranslate(get_cp, header_class_object.skips_in_constant_pool, name = file_name)
    pool = p_translator.translate_pool()
    access_flags = header_class_object.get_access_flags()
    this_class = header_class_object.get_this_class()
    super_class = header_class_object.get_super_class()
    get_ic = header_class_object.get_interfaces_count()
    header_class_object.get_interface() # no method built yet but should just be index in constant pool
    get_fc = header_class_object.get_field_count()
    header_class_object.get_field() # no method built yet but should just be variable table
    opcodes = header_class_object.get_methods_count()
    opcodes = header_class_object.get_methods(pool)

# ****************************************************************************************

    dict_search_object = packages.jvpm_opcodes.OpCodes(opcodes, pool)
    dict_search_object.dict_search()

# ****************************************************************************************
