# http://docs.python.org/2/library/struct.html
# http://stackoverflow.com/questions/16818463/python-encode-decoder-for-serialization-deserialization-javas-kyro-equivalence
# http://stackoverflow.com/questions/11624190/python-convert-string-to-byte-array
# http://stackoverflow.com/questions/2611858/struct-error-unpack-requires-a-string-argument-of-length-4
import struct

def encode(value, width=1): 
    """
    We only take care of integer value
    width is the width of table in bytes: q = 8 --> width = 1
    """
    formString = ">i"
    
    result = []
    packed = struct.pack(formString, value)
    
    for i in packed:
        result.append(ord(i[0]))
        
    lastIndex = len(result)
    # value is always 4 bytes because of (>i) format
    if width < 4: # if widht is smaller than 4
        for i in range(3): # 
            if result[i] != 0: raise Exception("Serialization error: truncated value")
        return result[(lastIndex - width):lastIndex]
    else:
        return [0] * (width - 4) + result
    
def decode(value, formString = None):
    assert type(value) == list
    if formString == None: formString = '>i'
    
    result = ""
    for i in value:
        result += chr(i)
        
    unpacked = struct.unpack(formString, result)[0]
    
    return unpacked
        
# print len(struct.pack('>f', 1.23))

if __name__ == "__main__":
    res = encode(1234331245, 4)
    print res
    print decode(res)
    