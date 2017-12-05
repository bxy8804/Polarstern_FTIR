#!/usr/bin/python
''' Python Opus Reader  --  Version 0.2  --  2014-01-22

Python class to interact with Bruker's Opus files. Provides header information and data access to spectra and interferograms

If you encounter errors, please contact Matthias Buschmann <m_buschmann@iup.physik.uni-bremen.de>

Dependencies:
Python 2.7
NumPy - http://www.numpy.org/
    using basic array operations to create spectrum and interferogram data - nothing fancy
matplotlib - http://matplotlib.org/
    only needed if run as main to plot interferogram and spectrum of a test file
'''

import struct, sys
import numpy as np

class opus:
    ''' Python class to interact with Bruker's Opus files. Provides header information and data access to spectra and interferograms.
    
    Provides:
        opus.header         opus header info
        opus.spc, opus.wvn   yields spectrum data array and corresponding wavenumber array
        opus.ifg            yields interferogram data array
    '''
    def getparamsfromblock(self, f, offset, length):
        c = 0
        params = {}
        i=0
        test = True
        #pdb.set_trace()
        while test:
            f.seek(offset+i)
            pn, mtype, leng = struct.unpack('4s2H', f.read(8))
            #print pn, mtype, leng
            i+=8
            if pn[-1]=='\x00': #get null terminated string
                pn=pn[:-1]
            else: pass
            #print 'Found parameter ', pn
            if pn[:3] != 'END':
                f.seek(offset+i)
                dat = f.read(2*leng)
                i+=2*leng
                try:
                    if mtype == 0:
                        val = struct.unpack(str(len(dat)/4)+'i', dat)[0]
                        params[pn]=val
                    elif mtype == 1:
                        val = struct.unpack(str(len(dat)/8)+'d', dat)[0]
                        params[pn]=val
                    elif mtype >= 2 and mtype <=4:
                        t = struct.unpack(str(2*leng)+'s', dat)[0]
                        t2 = ''
                        for j in t:
                            if j!='\x00' and type(j)==str:
                                t2 += j
                            else:
                                break
                        val=t2
                        params[pn]=val
                    else:
                        params[pn]= '[read error]'
                    #print '     with value ', params[pn]
                except Exception, e:
                    print e
            else:
                test = False
        return params

    def save_header(self, outfilename):
        with open(outfilename, 'a') as of:
            for i in self.header.keys():
                of.write(i+'\n')
                for j in self.header[i].keys():
                    of.write('  '+str(j)+': '+str(header[i][j])+'\n')

    def print_header(self):
        for i in self.header.keys():
            print i
            for j in self.header[i].keys():
                print '  '+str(j)+': '+str(self.header[i][j])

    def get_spc(self, f, pointer):
        #print pointer
        f.seek(pointer)
        #print self.datablocks
        self.spc = struct.unpack(str(self.datablocks['Data Block SpSm'][1])+'f', f.read(self.datablocks['Data Block SpSm'][1]*4))
        #print self.header['Data Parameters SpSm']['FXV'], self.header['Data Parameters SpSm']['LXV'], self.datablocks['Data Block SpSm'][1]
        self.spcwvn = np.linspace(self.header['Data Parameters SpSm']['FXV'], self.header['Data Parameters SpSm']['LXV'], self.datablocks['Data Block SpSm'][1])
        pass

    def get_trm(self, f, pointer):
        f.seek(pointer)
        self.trm = struct.unpack(str(self.datablocks['Data Block TrSm'][1])+'f', f.read(self.datablocks['Data Block TrSm'][1]*4))
        self.trmwvn = np.linspace(self.header['Data Parameters TrSm']['FXV'], self.header['Data Parameters TrSm']['LXV'], self.datablocks['Data Block TrSm'][1])
        pass

    def get_ifg(self, f, pointer):
        #print pointer
        f.seek(pointer)
        self.ifg = struct.unpack(str(self.datablocks['Data Block IgSm'][1])+'f', f.read(self.datablocks['Data Block IgSm'][1]*4))
        self.ifgopd = np.linspace(0,2*0.9/float(self.header['Acquisition Parameters']['RES']), len(self.ifg))

    def __init__(self, filename):
        #print 'Initializing ...'
        if filename.rfind('/')>0:
            self.folder = filename[:filename.rfind('/')]
            self.filename = filename[filename.rfind('/')+1:]
        else:
            self.folder = './'
            self.filename = filename
        magicval = '\n\n\xfe\xfe'
        hdrtype = {
        '160': 'Sample Parameters', 
        '96': 'Optic Parameters', 
        '64': 'FT Parameters', 
        '48': 'Acquisition Parameters', 
        '32': 'Instrument Parameters', 
        '31': 'Data Parameters',
        '23': 'Data Parameters', 
        '15': 'Data Block',
        '7': 'Data Block', 
        '0': 'Type 0'}
        needsubtype = {
        '160': False, 
        '96': False, 
        '64': False, 
        '48': False, 
        '32': False,
        '31': True,
        '23': True,
        '15': True, 
        '7': True, 
        '0': True}
        subtypes = {
        '4': 'SpSm', 
        '8': 'IgSm', 
        '20': 'TrSm',
        '52': '[unknown subtype 52]', 
        '\x84': 'SpSm/2.Chn.', 
        '\x88': 'IgSm/2.Chn.'}
        subtypesuffix = {
        '8': '', 
        '\x88': ' 2'}
        self.datablocks = {}
        try:
            #print 'Opening file ', filename, ' ...'
            f = open(filename, 'rb')
            f.seek(0)
            (magic, undef, undef, dof, tdb, ndb) = struct.unpack('6i', f.read(struct.calcsize('6i')))
            f.seek(0)
            if f.read(4)==magicval:
                #print 'Identified ', filename, ' as Opus file ...'
                f.seek(dof)
                dirs = {'type': [], 'subtype': [], 'length': [], 'offset': [] }
                while ndb > 0:
                    (mytype, subtype, undef, length, offset) = struct.unpack('2BH2i',f.read(struct.calcsize('2BH2i')))
                    dirs['type'].append(mytype)
                    dirs['subtype'].append(subtype)
                    dirs['length'].append(length)
                    dirs['offset'].append(offset)
                    ndb-=1
                self.header = {}
                #print 'Identified blocks ...'
                #for i in range(len(dirs['type'])):
                    #print dirs['type'][i], dirs['subtype'][i], dirs['length'][i], dirs['offset'][i]
                #print 'Fetching header parameters ...'
                for i in range(len(dirs['type'])):
                    subtype = ''
                    suffix = ''
                    if str(dirs['type'][i]) in hdrtype.keys():
                        hdrtext = hdrtype[str(dirs['type'][i])]
                        if needsubtype[str(dirs['type'][i])]:
                            try:
                                subtype = ' '+subtypes[str(dirs['subtype'][i])]
                            except:
                                subtype = ' [unknown subtype:'+str(dirs['subtype'][i])+']'
                            try:
                                suffix = subtypesuffix[str(dirs['subtype'][i])]
                            except:
                                suffix = ''
                        elif dirs['subtype'][i]!=0:
                            subtype = dirs['subtype'][i]
                            print 'Unexpected subtype '+str(dirs['subtype'][i])+' for block type '+str(dirs['type'][i])+'\n'
                        hdrtext+=subtype+suffix
                        #print 'Now fetching values for ', hdrtext
                        self.datablocks[hdrtext]=(dirs['offset'][i], dirs['length'][i])
                        if dirs['type'][i] not in [0,7,15]:
                            self.header[hdrtext] = self.getparamsfromblock(f, dirs['offset'][i], dirs['length'][i])
                        #elif len(subtype)==0 and dirs['type'][i] not in [0,7]:
                        #self.header[hdrtext] = self.getparamsfromblock(f, dirs['offset'][i], dirs['length'][i])
                        else: pass
                    else:
                        print 'Unknown block type ', dirs['type'][i], ' with subtype: ', dirs['subtype'][i], ', length: ', dirs['length'][i],', offset:',dirs['offset'][i]
                #pdb.set_trace()
                if 'Data Block SpSm' in self.datablocks.keys():
                    #print 'Creating SpSm ...'
                    self.get_spc(f, self.datablocks['Data Block SpSm'][0])
                if 'Data Block IgSm' in self.datablocks.keys():
                    #print 'Creating IgSm ...'
                    self.get_ifg(f, self.datablocks['Data Block IgSm'][0])
                if 'Data Block TrSm' in self.datablocks.keys():
                    #print 'Creating TrSm ...'
                    self.get_trm(f, self.datablocks['Data Block TrSm'][0])
                #else:
                    #print 'Unable to read Data blocks Interferogram or Spectrum data block!'
                f.close()
            else:
                print 'Bad Magic in '+filename+'\n'
                #sys.exit('Bad Magic in '+filename+'\n')
        except:#Exception, e:
            #print e
            print 'General error while processing '+filename
            #sys.exit('Unable to read file '+filename)
        

if __name__ == '__main__':
    import pdb
    #test = opus('../CELL_N2O_Loep/131213_46m4_RT_498mb2_av.0')#test.opus')
    test = opus("/home/philippr/testcali/calibrated/Emission_20170703_0939.0_97.5_7.kali")
    test.print_header()
    import matplotlib.pyplot as plt
    #plt.figure()
    plt.plot(test.spcwvn, test.spc, 'k-')
    #plt.figure()
    #plt.plot(test.trmwvn, test.trm, 'r-')
    #plt.figure()
    #plt.plot(test.s, 'k-')
    plt.show()
