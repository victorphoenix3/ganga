from Ganga.Core.exceptions import *
from Ganga.GPIDev.Adapters.ISplitter import ISplitter, GangaObject
from Ganga.GPIDev.Adapters.IBackend import IBackend
from Ganga.GPIDev.Adapters.IApplication import IApplication
from Ganga.GPIDev.Adapters.IRuntimeHandler import IRuntimeHandler
from Ganga.GPIDev.Adapters.ApplicationRuntimeHandlers import allHandlers
from Ganga.GPIDev.Schema import *
import sys

import Ganga.Utility.logging
logger = Ganga.Utility.logging.getLogger()

class CrashType(GangaObject):
    _schema = Schema(Version(1,0), {'expr':SimpleItem(defvalue=''), 'method':SimpleItem(defvalue=''),'condition':SimpleItem(defvalue='')})
    _category = 'testerrortype'
    _name = "CrashType"

    def trigger(self,val=None):
        """ The error is trigger if the caller's method name matches, condition is defined and evaluates to True the value is specified and the condition evaluates to True.
        """
        if sys._getframe(1).f_code.co_name == self.method:
            if val is None or not self.condition or eval(self.condition):
                print "triggering error at <method=%s, condition=%s, val=%s>, error expr=%s"%(repr(self.method),repr(self.condition),repr(val),repr(self.expr))
                exec(self.expr)
    
class CrashTestApplication(IApplication):
    _schema = Schema(Version(1,0), {'application_error':ComponentItem("testerrortype"),'rthandler_error':ComponentItem("testerrortype")})

    _category = 'applications'
    _name = 'CrashTestApplication'

    def configure(self, masterappconfig):
        #if self.application_error.method == 'configure':
        self.application_error.trigger()
        return (1,self.rthandler_error)

    def master_configure(self):
        #if self.application_error.method == 'master_configure':
        self.application_error.trigger()
        return (1,self.rthandler_error)
    

class CrashTestSplitter(ISplitter):
    _schema = Schema(Version(1,0), {'n':SimpleItem(defvalue=5), 'error':ComponentItem("testerrortype") } )

    _category = 'splitters'
    _name = 'CrashTestSplitter'

    def split(self,job):
        from Ganga.GPIDev.Lib.Job import Job
        subjobs = []
        for i in range(self.n):
            print 'Create subjob',i
            j = self.createSubjob(job)
            self.error.trigger(i)
            subjobs.append(j)
        return subjobs

# This backend just stores to job config objects.

class CrashTestBackend(IBackend):
    _schema = Schema(Version(1,0), {'error':ComponentItem("testerrortype")
                                    })

    _category = 'backends'
    _name = 'CrashTestBackend'

    def master_submit(self,rjobs,subjobconfigs,masterjobconfig):
        #if self.error.method == 'master_submit':
        self.error.trigger()
        return IBackend.master_submit(self,rjobs,subjobconfigs,masterjobconfig)
            
    def submit(self,jobconfig,master_input_sandbox):
        #if self.error.method == 'submit':
        self.error.trigger(self._getParent().id)
        return True

    def kill(self):
        #if self.error.method == 'kill':
        self.error.trigger()
        return True

    def updateMonitoringInformation(jobs):
        for j in jobs:
            j.backend.error.trigger()
    
    updateMonitoringInformation = staticmethod(updateMonitoringInformation)


class CrashRuntimeHandler(IRuntimeHandler):
    def master_prepare(self, app, appmasterconfig):
        #if appmasterconfig.method == 'master_prepare':
        appmasterconfig.trigger()
        return None

    def prepare(self,app,appsubconfig,appmasterconfig,jobmasterconfig):
        #if appsubconfig.method == 'prepare':
        appsubconfig.trigger()
        return None

allHandlers.add('CrashTestApplication','CrashTestBackend',CrashRuntimeHandler)
