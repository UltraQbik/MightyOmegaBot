import os
import ctypes


dll = ctypes.CDLL(os.path.join(os.path.dirname(os.path.realpath(__file__)), "MQ8B solution/x64/Release/MQ8B.dll"))

dll.emulate_mq8b.argtypes = [ctypes.POINTER(ctypes.c_uint16)]
dll.emulate_mq8b.restype = ctypes.POINTER(ctypes.c_char)

dll.delete_buffer.argtypes = [ctypes.c_char_p]
dll.delete_buffer.restype = None


def emulate_mq8b(insts: list[int]) -> bytes:
    # convert python array to ctype array
    arr = (ctypes.c_uint16 * len(insts))(*insts)

    # emulate the given instructions
    ret = dll.emulate_mq8b(arr)

    # convert the output to pythons string
    output = ctypes.cast(ret, ctypes.c_char_p).value

    # clear the buffer
    dll.delete_buffer(ret)

    return output


def test():
    insts = [
        0b0000000101000101,
        0b0000001000000000,
        0b0011000100000000,
        0b0111111100000000
    ]

    print(emulate_mq8b(insts))


if __name__ == '__main__':
    test()
