"""WARNING: intentionally writes a test text file to the mounted SD."""
import os
from sd_helpers import mount_sd

def main():
    sd,where=mount_sd()
    index=1
    while True:
        filename='%s/test_%03d.txt'%(where,index)
        try:
            os.stat(filename)
            index+=1
        except OSError:
            break
    with open(filename,'w') as file:
        file.write('RP2040-GEEK SD test\n')
    print('Wrote:',filename)

if __name__=='__main__':
    main()
