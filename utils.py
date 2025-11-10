def is_num(num):
    if len(num) == 0:
        return False
    for char in num:
        if not char.isdigit():
            return False
    return True

def is_valid_ip(ip):
    j = 0
    count = 0
    for i in range(len(ip)):
        if ip[i] == ".":
            count +=1
            if not is_num(ip[j:i]):
                return False
            j = i+1
    if not is_num(ip[j:]):
        return False
    if count != 3:
        return False
    return True

