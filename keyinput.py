import ctypes

keys = {
    "w":0x11,
    "a":0x1E,
    "s":0x1F,
    "d":0x20
}
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wvk", ctypes.c_ushort),
    ("wScan", ctypes.c_ushort),
    ("dwFlags", ctypes.c_ulong),
    ("time", ctypes.c_ulong),
    ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
    ("wParamL", ctypes.c_short),
    ("wParamh", ctypes.c_ushort)]

