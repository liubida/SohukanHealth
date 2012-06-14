import datetime

class SohukanException(Exception):
    time_format = "%Y.%m.%d %H:%M:%S"
    
    def __init__(self, msg=''):
        super(SohukanException, self).__init__()
        self.now = datetime.datetime.now().strftime(self.time_format)
        self.msg = msg

    def __str__(self):
        return '[%s|SohukanException]:%s' % (self.now, self.msg)
    
class StatisticsException(SohukanException):
    def __init__(self, msg=''):
        super(StatisticsException, self).__init__(msg)
        
    def __str__(self):
        return '[%s|StatisticsException]:%s' % (self.now, self.msg)
    
class MonitorException(SohukanException):
    def __init__(self, msg=''):
        super(MonitorException, self).__init__(msg)
        
    def __str__(self):
        return '[%s|MonitorException]:%s' % (self.now, self.msg)
    
class JobException(SohukanException):
    def __init__(self, msg=''):
        super(JobException, self).__init__(msg)
                
    def __str__(self):
        return '[%s|JobException]:%s' % (self.now, self.msg)
    
if __name__ == '__main__':
    try:
        1 / 0
    except Exception as e:
        a = SohukanException(e)
        print a
