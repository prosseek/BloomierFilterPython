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
    if k > 32: raise Error("k should be less than 32")
    if k <= 1: raise Error("k should be more than 2")
    if k > m: raise Error("k should be less than m")

    result = []
    index = 0
    
    # make the non-overwrapping hash value below m
    while True:
        value = int(hashed_password[index:index+2], 16) % m
        index += 2
        
        # second loop for detecting the duplicate value
        while True:
            if value not in result:
                result.append(value)
                break
            # Try the next value
            value = int(hashed_password[index:index+2], 16) % m
            index += 2
        if len(result) == k: break
        
    return result
    
if __name__ == "__main__":
    res = getHash("abc", 1, 10, 5) # seed:1, m = 10, k = 5
    assert len(res) == 5
