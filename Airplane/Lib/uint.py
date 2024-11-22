def int32(x):
    if(x < 0):
        return x | 0X80000000
    else:
        return x
    
def uint7(val, bit):
    return val>>bit & 0X0000007F