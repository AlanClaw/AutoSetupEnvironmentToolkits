import logging, sys

import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "BuildupAtuoEnvirKits"))
sys.path.append(path)

from AbstratBuildWinEnvirMgr import BuildEnvTemplate
from SetupManager.wxPythonSetupMgr import wxPythonSetupMgr
from SetupManager.NotepadPlusPlusMgr import NotepadPlusPlusMgr
from SetupManager.JavaRuntimeSetupMgr import JavaRuntimeSetupMgr
from SetupManager.PyScripterSetupMgr import PyScripterSetupMgr
from SetupManager.FirefoxSetupMgr import FirefoxSetupMgr
from SetupManager.ChromeSetupMgr import ChromeSetupMgr
from SetupManager.VimSetupMgr import VimSetupMgr
from SetupManager.PipPackageSetupMgr import PipPackageSetupMgr 
from SetupManager.GitSetupMgr import GitSetupMgr

class AutoEnvBuilder(BuildEnvTemplate):
    
    def __init__(self):
        '''
        '''
        super(self.__class__, self).__init__('install.log')
        
        pip_mgr = PipPackageSetupMgr("pip", need_install=True, need_update=True)
        jre_mgr = JavaRuntimeSetupMgr(need_install=True)
        wx_python_mgr = wxPythonSetupMgr(need_install=True)
        pillow_mgr = PipPackageSetupMgr("pillow", need_install=True, need_update=True)
        
        robot_framework_mgr = PipPackageSetupMgr("robotframework", need_install=True, need_update=True)
        robot_ride_mgr = PipPackageSetupMgr("robotframework-ride", need_install=True, need_update=True)
        selenium_mgr = PipPackageSetupMgr("selenium", need_install=True, need_update=True)
        robot_selenium_mgr = PipPackageSetupMgr("robotframework-seleniumlibrary", need_install=True, need_update=True)
        robot_selenium2_mgr = PipPackageSetupMgr("robotframework-selenium2library", need_install=True, need_update=True)
        decorator_mgr = PipPackageSetupMgr("decorator", need_install=True, need_update=True)

        git_mgr = GitSetupMgr(need_download=False, need_install=True, need_update=False)
        
        firefox_mgr = FirefoxSetupMgr(need_download=True, need_install=True, need_update=True)
        chorome_mgr = ChromeSetupMgr(need_download=False, need_install=True, need_update=True)
        
        notepad_plus_plus_mgr = NotepadPlusPlusMgr(need_download=True, need_install=True)
        py_scripter = PyScripterSetupMgr(need_install=True)
        vim_setup_mgr = VimSetupMgr(need_download=False, need_install=True, need_update=False)
        
        robot_database_mgr = PipPackageSetupMgr("robotframework-databaselibrary", need_install=True, need_update=True)
        pymssql_mgr = PipPackageSetupMgr("pymssql", need_install=True, need_update=True)
        
        self.pkg_mgr_order = [jre_mgr, 
                              wx_python_mgr,
                              pillow_mgr,
                              robot_framework_mgr,
                              robot_ride_mgr,
                              selenium_mgr,
                              robot_selenium_mgr,
                              robot_selenium2_mgr,
                              decorator_mgr,
                              robot_database_mgr,
                              pymssql_mgr,
                              firefox_mgr,
                              chorome_mgr,
                              notepad_plus_plus_mgr,
                              git_mgr]


if __name__ == '__main__':
    '''
    '''
    auto_env_mgr = AutoEnvBuilder()
    auto_env_mgr.setup_environment(auto_env_mgr.pkg_mgr_order)