import os

def SetHostname(hostname):
    os.system('hostname %s' % hostname)