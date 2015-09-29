import logging, sys

_logger = logging.getLogger(__name__)

import os, re
import subprocess, time

from WinGUI.autoit.LocWrapper import AutoitLocator, WindowLocator, ControlLocator
from WinGUI.OperatorAdapter import click_dialog_button, close_window
from AbstractPackageSetupManager import PackageManager
from PackageUtils.WinUtils import is_x86_platform


class FirefoxSetupMgr(PackageManager):

    DEFAULT_INSTALL_PKG_NAME = 'Mozilla Firefox'
    
    def __init__(self, 
                 sft_name='Mozilla Firefox', 
                 need_download=False, 
                 need_install=False, 
                 need_update=False):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''
        super(self.__class__, self).__init__(sft_name, need_download, need_install, need_update)
        
        self._is_x86 = is_x86_platform()
        self.DEFAULT_INSTALL_PKG_NAME = "Firefox Setup 39.0.exe"
        
        self.install_pkg_search_ptn = '^(Firefox Setup)(.*)(\.exe)$'
        
    
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
        possible_path = ['C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe']
        return super(self.__class__, self).is_installed(possible_path) 

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        
        subprocess.Popen(self.get_install_pkg_path())
          
        time.sleep(20) # waiting for extraction
        
        page = AutoitLocator()
        page.window = WindowLocator("[CLASS:#32770; INSTANCE:1]")
        page.control = ControlLocator("[CLASS:Button; INSTANCE:2]")
        click_dialog_button(loc=page, timeout=5, action_log='Click Next (Welcome)')
        
        click_dialog_button(loc=page, timeout=5, action_log='Click Next (Setup Type)')
        
        click_dialog_button(loc=page, timeout=5, action_log='Click Install (Summary)')
        time.sleep(60) # waiting for installation
        
        page.control = ControlLocator("[CLASS:Button; INSTANCE:4]", "left", 1, 5, 5)
        click_dialog_button(loc=page, timeout=300, action_log='Unclick Launch... (Completing)')
        
        page.control = ControlLocator("[CLASS:Button; INSTANCE:2]")
        click_dialog_button(loc=page, timeout=5, action_log='Click Finish... (Completing)')
        
        self.setup_firefox_profile_by_cmd()
        
    def do_update(self, pkg_path):
        '''
        @note: execute update process
        '''
        subprocess.Popen(self.get_install_pkg_path())
          
        time.sleep(20) # waiting for extraction
        
        page = AutoitLocator()
        page.window = WindowLocator("[CLASS:#32770; INSTANCE:1]")
        page.control = ControlLocator("[CLASS:Button; INSTANCE:2]")
        click_dialog_button(loc=page, timeout=5, action_log='Click Next (Welcome)')
        
        click_dialog_button(loc=page, timeout=5, action_log='Click Next (Setup Type)')
        
        click_dialog_button(loc=page, timeout=5, action_log='Click Install (Summary)')
        time.sleep(60) # waiting for installation
        
        page.control = ControlLocator("[CLASS:Button; INSTANCE:4]", "left", 1, 5, 5)
        click_dialog_button(loc=page, timeout=300, action_log='Unclick Launch... (Completing)')
        
        page.control = ControlLocator("[CLASS:Button; INSTANCE:2]")
        click_dialog_button(loc=page, timeout=5, action_log='Click Finish... (Completing)')
        
        self.setup_firefox_profile_by_cmd()
    
    def setup_firefox_profile_by_cmd(self):
        """
        """
        if self.is_installed():
            # optional: firefox -CreateProfile "JoelUser c:\internet\moz-profile"
            _logger.debug("firefox path:{0}".format(self.installed_prog_path))
            cmd = 'start "" "%s" -CreateProfile "default(selenium) C:\\auto\\tools\\firefox-profiles\\default"' \
                    % self.installed_prog_path
            _logger.info(cmd)
            subprocess.call(cmd, shell = True)
    
        else:
            _logger.warning("Can't find firefox path")
    
if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S',
    )
    
    inst = FirefoxSetupMgr()
    print inst.get_install_pkg_path(search_folder='C:\\Users\\alan\\Desktop\\Automation Install Package\\Package')