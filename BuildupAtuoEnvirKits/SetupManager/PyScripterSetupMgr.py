import logging, sys

_logger = logging.getLogger(__name__)

import os, re
import subprocess

from WinGUI.autoit.LocWrapper import AutoitLocator, WindowLocator, ControlLocator
from WinGUI.OperatorAdapter import click_dialog_button, close_window
from AbstractPackageSetupManager import PackageManager
from PackageUtils.WinUtils import is_x86_platform


class PyScripterSetupMgr(PackageManager):

    DEFAULT_INSTALL_PKG_NAME = 'PyScripter'
    
    def __init__(self, 
                 sft_name='PyScripter', 
                 need_install=False, 
                 need_update=False):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''
        super(self.__class__, self).__init__(sft_name, False, need_install, need_update)
        
        self._is_x86 = is_x86_platform()
        self.DEFAULT_INSTALL_PKG_NAME = "PyScripter-v2.6.0-Setup.exe" if self._is_x86 \
                                        else "PyScripter-v2.6.0-x64-Setup.exe"
        
        self.install_pkg_search_ptn = '^(PyScripter-v)(.*)(-Setup\.exe)$' if self._is_x86 \
                                        else '^(PyScripter-v)(.*)(-x64-Setup\.exe)$'
        

    def get_installed_version(self):
        '''
        @return: return None if this package has not be installed, or the version of the installed package in tuple
        @rtype: tuple, (0,0,0,0)
        '''
        from PackageUtils.WinUtils import get_file_version_number as get_file_ver
        
        if not self.installed_prog_path:
            return None
        else:
            return get_file_ver(self.installed_prog_path)
        
    def is_installed(self):
        '''
        @note: assign a path list or a single path to  determine the program has been installed or not
        @type possible_install_paths: str or list
        '''
        possible_path = ['C:\\Program Files (x86)\\PyScripter', 'C:\\Program Files\\PyScripter']
        return super(self.__class__, self).is_installed(possible_path)


    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        
#         subprocess.Popen(self.get_install_pkg_path())
          
        page = AutoitLocator()
        page.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page.control = ControlLocator("TNewButton1")
        click_dialog_button(loc=page, timeout=10, action_log='Click Next')
         
        page.control = ControlLocator("TNewButton2") 
        click_dialog_button(loc=page, timeout=10, action_log='Click Next')
         
        page.control = ControlLocator("TNewButton3") 
        click_dialog_button(loc=page, timeout=10, action_log='Click Next (install path)')
         
        page.control = ControlLocator("TNewButton4") 
        click_dialog_button(loc=page, timeout=10, action_log='Click Next (folder name)')
         
        click_dialog_button(loc=page, timeout=10, action_log='Click Next (additional task)')
         
        click_dialog_button(loc=page, timeout=10, action_log='Click Install')
         
        click_dialog_button(loc=page, timeout=60, action_log='Click Next (Information)')
        
        page.control = ControlLocator("[CLASS:TNewCheckListBox; INSTANCE:1]", "left", 1, 10, 10) 
        click_dialog_button(loc=page, timeout=120, action_log='Unclick Launch PyScripter')
        
        page.control = ControlLocator("[CLASS:TNewButton; INSTANCE:4]") 
        click_dialog_button(loc=page, timeout=10, action_log='Click Finish')
        
    def do_update(self, pkg_path):
        '''
        @note: execute update process
        '''
        raise NotImplementedError('You need implement this function!')
    
if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S',
    )