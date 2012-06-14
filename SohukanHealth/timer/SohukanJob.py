'''
Created on Jun 13, 2012

@author: liubida
'''
from monitor.system.s3.check_s3_connectivity import check_s3

class SohukanJob():
    def __init__(self, name, exec_time, comments):
        self.name = name
        self.exec_time = exec_time
        self.comments = comments
    
    def execute(self):
        pass

class S3Job(SohukanJob):
    def __init__(self, name, exec_time, comments):
        super(S3Job, self).__init__(name, exec_time, comments)
        
    def execute(self):
        super(S3Job, self).execute()
        check_s3()
