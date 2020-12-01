#import snap7.client as c
from snap7.util import *
from snap7.snap7types import *


def get_process_outputs_bit(plc, byte, bit):
    result = plc.read_area(areas['PA'], 0, byte, S7WLBit)
    return get_bool(result, 0, bit)


def set_process_outputs_bit(plc, byte, bit, cmd):
    result = plc.read_area(areas['PA'], 0, byte, S7WLBit)
    set_bool(result, byte, bit, cmd)
    plc.write_area(areas['PA'], 0, byte, result)


def set_process_inputs_bit(plc, byte, bit, cmd):
    result = plc.read_area(areas['PE'], 0, byte, S7WLBit)
    set_bool(result, byte, bit, cmd)
    plc.write_area(areas['PE'], 0, byte, result)


def get_process_inputs_bit(plc, byte, bit):
    result = plc.read_area(areas['PE'], 0, byte, S7WLBit)
    return get_bool(result, 0, bit)


def get_merkers(plc, byte, bit, datatype):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        return get_bool(result, 0, bit)
    elif datatype == S7WLByte or datatype == S7WLWord:
        return get_int(result, 0)
    elif datatype == S7WLReal:
        return get_real(result, 0)
    elif datatype == S7WLDWord:
        return get_dword(result, 0)
    else:
        return None


def set_merkers(plc, byte, bit, datatype, value):
    result = plc.read_area(areas['MK'], 0, byte, datatype)
    if datatype == S7WLBit:
        set_bool(result, 0, bit, value)
    elif datatype == S7WLByte or datatype == S7WLWord:
        set_int(result, byte, value)
    elif datatype == S7WLReal:
        set_real(result, byte, value)
    elif datatype == S7WLDWord:
        set_dword(result, byte, value)
    plc.write_area(areas['MK'], 0, byte, result)
