################################################################################
# Ganga Project. http://cern.ch/ganga
#
# $Id: OutputFile.py,v 0.1 2011-09-29 15:40:00 idzhunov Exp $
################################################################################

from Ganga.GPIDev.Base import GangaObject
from Ganga.GPIDev.Schema import *

class OutputFile(GangaObject):
    """OutputFile represents base class for output files, such as CompressedFile,
       ScratchFile, LHCbDataFile, CastorFile, etc 
    """
    _schema = Schema(Version(1,1), {'name': SimpleItem(defvalue="",doc='name of the file')})
    _category = 'outputfiles'
    _name = "OutputFile"

    def __init__(self,name='', **kwds):
        """ name is the name of the output file that is going to be processed
            in some way defined by the derived class
        """
        super(OutputFile, self).__init__()
        self.name = name 
    
    def __construct__(self,args):
        if len(args) == 1 and type(args[0]) == type(''):
            self.name = args[0]
        else:
            super(OutputFile,self).__construct__(args)
        
    def __repr__(self):
        """Get the representation of the file."""

        return "OutputFile(name='%s')"% self.name


from Ganga.GPIDev.Base.Filters import allComponentFilters
from CompressedFile import CompressedFile
from ScratchFile import ScratchFile
from LHCbDataFile import LHCbDataFile

from Ganga.Utility.Config import getConfig, ConfigError

outputfilesConfig = {}
keys = ['CompressedFile', 'ScratchFile', 'LHCbDataFile']

for key in keys:
    try:
        outputFileExtensions = []

        for configEntry in getConfig('Output')[key]:
            #get only the extension
            if configEntry.startswith('*.'):
                outputFileExtensions.append(configEntry[2:])
            else:
                outputFileExtensions.append(configEntry)
                
        outputfilesConfig[key] = outputFileExtensions

    except ConfigError:
        #todo:ivan throw some error here
        pass    

def findOutputFileTypeByFileName(filename):

    dotIndex = filename.find('.')       
    #get only the extension     
    if dotIndex > -1:
        filename = filename[dotIndex+1:]        

    for key in outputfilesConfig.keys():

        if filename in outputfilesConfig[key]:
            return key
 
    return None

def string_file_shortcut(v,item):
    if type(v) is type(''):
        # use proxy class to enable all user conversions on the value itself
        # but return the implementation object (not proxy)
        key = findOutputFileTypeByFileName(v)
        if key is not None:
            if key == 'CompressedFile':
                return CompressedFile._proxyClass(v)._impl
            elif key == 'ScratchFile':
                return ScratchFile._proxyClass(v)._impl         
            elif key == 'LHCbDataFile':
                return LHCbDataFile._proxyClass(v)._impl                                
        
        return OutputFile._proxyClass(v)._impl

    return None 
        
allComponentFilters['outputfiles'] = string_file_shortcut
