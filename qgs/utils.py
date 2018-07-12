import platform


def wrapString(s):
    # 防止中文乱码
    sysstr = platform.system()
    if sysstr == "Windows":
        encoding = 'gbk'
        return s.encode(encoding).decode('utf-8')
    else:
        return s
