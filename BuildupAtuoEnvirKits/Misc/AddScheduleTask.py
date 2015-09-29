import logging
_logger = logging.getLogger(__name__)
import subprocess,re,sys

class Add_Controller_Schedule(object):
    """
    """
    python_path = r'C:\Python27\python.exe'
    scheduler_path = r'C:\auto\svn\tools\AutomationTestingSystem\Scheduler.py'
    delete_scheduler= False
    
    def __init__(self):
        """
        @args -d: delete run_scueduler    
        """
        args = sys.argv[1:]
        for option in args:
            if option =='-d':
                self.delete_scheduler = True
       
    def insert_schedule(self):
        """
        """
        if not (self.check_schedule_exist()):
            if  (self.check_windows_version()):
                subprocess.call(["schtasks","/create","/TN","run_scheduler","/TR",
                                 "%s %s"%(self.python_path,self.scheduler_path),
                                 "/SC","MINUTE","/MO","10","/RL","HIGHEST"],shell=True)
                                 
                # exception handle for XP and WinServer2003
            else:
                subprocess.call(["schtasks","/create","/TN","run_scheduler","/TR",
                                 "%s %s"%(self.python_path,self.scheduler_path),
                                 "/SC","MINUTE","/MO","10"],shell=True)  
                _logger.info("insert run_scheduler successful")
        else:
            _logger.info("run_scheduler already exists")
            
    def check_schedule_exist(self):
        
        query_result = subprocess.Popen("schtasks /query /fo TABLE", stdout=subprocess.PIPE)
        match = re.findall('run_scheduler', query_result.stdout.read())
        return False if len(match) == 0 else True

    def check_windows_version(self):
       
        version_result = subprocess.Popen(["ver"], stdout=subprocess.PIPE,shell=True)
        #check kernel version 
        match = ''.join(re.findall('[0-9][.][0-9]{1}', version_result.stdout.read()))
        return False if match =="5.1" or match =="5.2" else True
        
    def delete_run_scueduler(self):
        
        subprocess.call(["schtasks","/delete","/TN","run_scheduler","/F"],shell=True)
        _logger.info("run_scheduler delete successful")
    
    def execute(self):
        """
        """
        if self.delete_scheduler:
            self.delete_run_scueduler()
        else:    
            self.insert_schedule()  
           
def main():
    """
    """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s : %(message)s',
        level = logging.INFO,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
        

if __name__ == '__main__':
    
    main()
    schedule = Add_Controller_Schedule()
    schedule.execute()