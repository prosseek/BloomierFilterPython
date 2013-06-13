import hashlib, uuid
# http://stackoverflow.com/questions/209513/convert-hex-string-to-int-in-python

def getHash(key, hashseed, m, k):
    """
    We use sha256, and it generates 64 bytes of hash number, so k should be 2 <= k <= 32
    However, because of duplicity the real limit should be much lower.
    
    Todo: You can concatenate more sha256 values to get more k values
    """
    salt = str(hashseed)
    hashed_password = hashlib.sha256(key + salt).hexdigest()
    #print hashed_password
    if k > 32: raise Exception("k should be less than 32")
    if k <= 1: raise Exception("k should be more than 2")
    if k > m: raise Exception("k should be less than m")
    
    # it cuts 4 byte from the hashed_password, so the value is 0xFFFF
    assert(m < 0xFFFF)
    assert(len(hashed_password)/4 > k)

    result = []
    index = 0
    
    # make the non-overwrapping hash value below m
    while True:
        #print int(hashed_password[index:index+4], 16) 
        value = int(hashed_password[index:index+4], 16) % m
        index += 4
        
        # second loop for detecting the duplicate value
        while True:
            if value not in result:
                result.append(value)
                break
            # Try the next value
            value = int(hashed_password[index:index+4], 16) % m
            index += 4
        if len(result) == k: break
        
    return result
    
if __name__ == "__main__":
    res = getHash("abcd", 1, 10, 5) # seed:1, m = 10, k = 5
    print res
    assert len(res) == 5
