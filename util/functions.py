import re
def is_cidr(str_cidr):
    pattern='^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$'
    m=re.match(pattern,str_cidr)
    if m == None:
        return False
    else:
        return True
def is_ipv4(str_ipv4):
    pattern='^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    m=re.match(pattern,str_ipv4)
    if m == None:
        return False
    else:
        return True
if __name__ == "__main__":
    print is_cidr('192.168.0.0/24')
    print is_ipv4('192.167.1.333')
    
