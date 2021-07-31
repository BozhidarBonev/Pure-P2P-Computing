import subprocess
def GetLocalIP():
    #Windows implementation
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wi-fi' in i:
            scan=1
        if scan:
            if 'ipv4' in i:
                return i.split(':')[1].strip()