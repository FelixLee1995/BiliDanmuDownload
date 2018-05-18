

def filterFilepath(filepath):
    res = []
    for x in filepath.strip():
        if x not in ['?', ':', '\\', '/', '*', '"', '<', '>', '|', '\t', '\r']:
            res.append(x)
        else:
            res.append('_')
    return "".join(res)


# print(filterFilepath('EP09 说出过去没\r能说出口\t的感谢，乃木坂时光机\t'))