import logging,subprocess,sys,os, time
_logger = logging.getLogger(__name__)

from AbstractPackageSetupManager import PackageManager as PackageManager
from PackageUtils.WinUtils import is_x86_platform

import time

class NotepadPlusPlusMgr(PackageManager):
    
    DEFAULT_INSTALL_PKG_NAME = 'Notepad++'
    
    def __init__(self, 
                 sft_name='Notepad++', 
                 need_download=False, 
                 need_install=False, 
                 need_update=False):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''
        super(self.__class__, self).__init__(sft_name, need_download, need_install, need_update)
        
        self.DEFAULT_INSTALL_PKG_NAME = "npp.6.8.Installer.exe"
        self.install_pkg_search_ptn = '^(npp.)(.*)(.Installer.exe)$'
    
    
    def is_installed_latest_ver(self):
        '''
        '''
        return False

    def is_installed(self):
        '''
        @note: assign a path list or a single path to  determine the program has been installed or not
        @type possible_install_paths: str or list
        '''
        possible_path = ['C:\\Program Files (x86)\\Notepad++', 'C:\Program Files\Notepad++']
        return super(self.__class__, self).is_installed(possible_path)

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        from WinGUI.OperatorAdapter import click_dialog_button
        from WinGUI.autoit import LocWrapper
        
        subprocess.Popen(self.get_install_pkg_path())
 
        locator = LocWrapper.AutoitLocator()
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("Button1")
        click_dialog_button(loc=locator, action_log='Click OK')
 
        # Welcome to the notepad setup
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("Button2")
        click_dialog_button(loc=locator, action_log='Click Next')
 
        # License agreement
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("Button2")
        click_dialog_button(loc=locator, action_log='Click I Agree')
 
        # Choose install location
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("Button2")
        click_dialog_button(loc=locator, action_log='Click Next')
 
        # Choose components
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("Button2")
        click_dialog_button(loc=locator, action_log='Click Next')
 
        # Choose components
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("Button2")
        click_dialog_button(loc=locator, action_log='Click Install')

        time.sleep(20)
        # Completing the notepad setup
        locator.window = LocWrapper.WindowLocator("[CLASS:#32770; INSTANCE:1]")
        locator.control = LocWrapper.ControlLocator("[CLASS:Button; INSTANCE:4]", "left", 1, 8, 8)
        click_dialog_button(loc=locator, timeout=10, action_log='Unclick Run Notepad++')
        locator.control = LocWrapper.ControlLocator("Button2")
        click_dialog_button(loc=locator, timeout=10, action_log='Click Finish')
        return
    
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
    notepad = NotepadPlusPlusManager("Notepad++", False, True, False)
    if notepad.need_download:
        print notepad.download_pkg()

    print sys.path
    if notepad.need_install and not notepad.is_installed(None):
        notepad.do_install(notepad.get_install_pkg_path(None, "npp."))
        print notepad.get_install_pkg_version()

