import logging, sys

_logger = logging.getLogger(__name__)

import os, re
import subprocess

from WinGUI.autoit.LocWrapper import AutoitLocator, WindowLocator, ControlLocator
from WinGUI.OperatorAdapter import click_dialog_button, close_window
from AbstractPackageSetupManager import PackageManager
from PackageUtils.WinUtils import is_x86_platform, windows_version_should_in_range, set_softlink


DEFAULT_PROFILE_PATH = "C:\\auto\\tools\\chrome-profiles"

class ChromeSetupMgr(PackageManager):

    DEFAULT_INSTALL_PKG_NAME = 'Chrome'
    
    def __init__(self, 
                 sft_name='Chrome', 
                 need_download=False, 
                 need_install=False, 
                 need_update=False,
                 winXP=False):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''
        super(self.__class__, self).__init__(sft_name, need_download, need_install, need_update)
        
        self._is_x86 = is_x86_platform()
        self.DEFAULT_INSTALL_PKG_NAME = "ChromeSetup.exe"
        
        self.install_pkg_search_ptn = '^(ChromeSetup)(.*)(\.exe)$'

        self.chrome_user_data_dir = DEFAULT_PROFILE_PATH
        
        # setup profile path for chorme by different Windows version
        is_winXP = windows_version_should_in_range(max_ver="5.9.9999", need_return=True)
        if is_winXP:
            app_data_path = os.path.join(os.path.abspath(os.environ["USERPROFILE"]), "Local Settings", "Application Data")
        else:
            app_data_path = os.path.abspath(os.environ["LOCALAPPDATA"])
            
        self.chrome_user_data_dir_default = os.path.join(app_data_path, "Google", "Chrome", "User Data")
        self.chrome_exec = os.path.join(os.path.abspath(os.environ["PROGRAMFILES" if self._is_x86 else "PROGRAMFILES(X86)"]), 
                                        "Google", "Chrome", "Application", "chrome.exe")
        self.chrome_user_name = "Default"
        
        
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
        possible_path = ['C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                         'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe']
        return super(self.__class__, self).is_installed(possible_path)

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        cmd = '"{0}" /silent /install'.format(self.get_install_pkg_path())
        
        _logger.info("silent install chrome")
        subprocess.call(cmd, shell=True)
        
        if self.is_installed(): current_version = self.get_installed_version()        
        self.setup_chrome_profile_by_cmd()
        
    def do_update(self, pkg_path):
        '''
        @note: execute update process
        '''
        cmd = '"{0}" /silent /install'.format(self.get_install_pkg_path())
        
        _logger.info("silent install chrome")
        subprocess.call(cmd, shell=True)

        if self.is_installed(): current_version = self.get_installed_version()
        self.setup_chrome_profile_by_cmd()
    
    def setup_chrome_profile_by_cmd(self):
        """
        """
        #cmd = 'start "" "%s" --user-data-dir="C:\auto\tools\chrome-profiles" --profile-directory="default(selenium)" --no-first-run --no-default-browser-check' % self._package.chrome_exec
        import shutil
        shutil.rmtree(self.chrome_user_data_dir, ignore_errors=True)
        try:
            #os.makedirs(self._package.chrome_user_data_dir)
            os.makedirs(self.chrome_user_data_dir_default)
        except:
            pass
        _logger.info("set softlink from [%s] to [%s]" % (self.chrome_user_data_dir, self.chrome_user_data_dir_default))
        set_softlink(self.chrome_user_data_dir, self.chrome_user_data_dir_default)
        open(os.path.join(self.chrome_user_data_dir_default, "First Run"), "wb").close()
        cmd = 'start "" "%s" --profile-directory="%s"' % (self.chrome_exec, self.chrome_user_name)
        _logger.info(cmd)
        subprocess.call(cmd, shell = True)
    
    
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