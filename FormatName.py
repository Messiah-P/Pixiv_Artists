
def fileName(name):
    is_contain_ch="/" in name
    if is_contain_ch:
        nameList = name.split('/')
        name = nameList[0] +  '_' + nameList[1]
        format(name)
    return (name)
