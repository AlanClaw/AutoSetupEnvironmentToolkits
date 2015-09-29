import logging, sys

_logger = logging.getLogger(__name__)

import os, re
import subprocess

from WinGUI.autoit.LocWrapper import AutoitLocator, WindowLocator, ControlLocator
from WinGUI.OperatorAdapter import click_dialog_button, close_window
from AbstractPackageSetupManager import PackageManager
from PackageUtils.WinUtils import is_x86_platform


class JavaRuntimeSetupMgr(PackageManager):

    DEFAULT_INSTALL_PKG_NAME = 'JavaRuntimeEnvironment'
    
    def __init__(self, 
                 sft_name='JavaRuntimeEnvironment', 
                 need_download=False, 
                 need_install=False, 
                 need_update=False):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''
        super(self.__class__, self).__init__(sft_name, False, need_install, need_update)
        
        self._is_x86 = is_x86_platform()
        self.DEFAULT_INSTALL_PKG_NAME = "jre-8u51-windows-i586.exe" if self._is_x86 \
                                        else "jre-8u51-windows-x64.exe"
        
        self.install_pkg_search_ptn = '^(jre-)(.*)(-windows-i586\.exe)$' if self._is_x86 \
                                        else '^(jre-)(.*)(-windows-x64\.exe)$'
        

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
        possible_path = ['C:\\Program Files (x86)\\Java', 'C:\\Program Files\\Java']
        return super(self.__class__, self).is_installed(possible_path)

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        
        subprocess.Popen(self.get_install_pkg_path())
          
        page = AutoitLocator()
        page.window = WindowLocator("[CLASS:#32770; INSTANCE:1]")
        page.control = ControlLocator("Button3")
        click_dialog_button(loc=page, timeout=10, action_log='Click Next')
         
        click_dialog_button(loc=page, timeout=300, action_log='Click Close')
        
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
    
    inst = JavaRuntimeSetupMgr()
    print inst.get_install_pkg_path(search_folder='C:\\Users\\alan\\Desktop\\Automation Install Package\\Package')