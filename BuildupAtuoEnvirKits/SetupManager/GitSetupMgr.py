import logging,subprocess,sys,os, time
_logger = logging.getLogger(__name__)

from AbstractPackageSetupManager import PackageManager as PackageManager
from PackageUtils.WinUtils import is_x86_platform

import time

class GitSetupMgr(PackageManager):
    
    DEFAULT_INSTALL_PKG_NAME = 'Git'
    
    def __init__(self, 
                 sft_name='Git', 
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
        self.DEFAULT_INSTALL_PKG_NAME = "Git-2.5.2.2-32-bit.exe" if self._is_x86 \
                                        else "Git-2.5.2.2-64-bit.exe"
        
        self.install_pkg_search_ptn = '^(Git-)(.*)(-32-bit\.exe)$' if self._is_x86 \
                                        else '^(Git-)(.*)(-64-bit\.exe)$'


    
    def is_installed_latest_ver(self):
        '''
        '''
        return False

    def is_installed(self):
        '''
        @note: assign a path list or a single path to  determine the program has been installed or not
        @type possible_install_paths: str or list
        '''
        possible_path = ['C:\\Program Files (x86)\\Git', 'C:\Program Files\Git']
        return super(self.__class__, self).is_installed(possible_path)

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        from WinGUI.OperatorAdapter import click_dialog_button
        from WinGUI.autoit import LocWrapper

        subprocess.Popen(self.get_install_pkg_path())
 
        locator = LocWrapper.AutoitLocator()
        # Welcome to the Git Setup Wizard
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton1")
        click_dialog_button(loc=locator, action_log='Click Next')
 
        # GNU General Public License
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton2")
        click_dialog_button(loc=locator, action_log='Click Next')
 
        # Select destination location
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton3")
        click_dialog_button(loc=locator, action_log='Click Next')
 
        # Select components
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton3")
        click_dialog_button(loc=locator, action_log='Click Next components')
 
        # Select start menu folder
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton4")
        click_dialog_button(loc=locator, action_log='Click Next folder')

        # Adjusting your PATH environment
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton4")
        click_dialog_button(loc=locator, action_log='Click Next')

        # Configuring the line ending conversions
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton4")
        click_dialog_button(loc=locator, action_log='Click Next')

        # Configuring the terminal emulator to use with Git Bash
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton4")
        click_dialog_button(loc=locator, action_log='Click Next')

        # Configuring experimental performance tweaks
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("TNewButton4")
        click_dialog_button(loc=locator, action_log='Click Next')

        time.sleep(80)
        # Completing the Git setup wizard
        locator.window = LocWrapper.WindowLocator("[CLASS:TWizardForm]")
        locator.control = LocWrapper.ControlLocator("[CLASS:TNewCheckListBox; INSTANCE:1]", "left", 1, 11, 11)
        click_dialog_button(loc=locator, timeout=10, action_log='Unclick view ReleaseNotes.html')
        locator.control = LocWrapper.ControlLocator("TNewButton4")
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
    git = GitSetupMgr("Git", False, True, False)
    if git.need_download:
        print git.download_pkg()

    print sys.path
    if git.need_install and not git.is_installed(None):
        git.do_install(git.get_install_pkg_path(None, "Git-"))
        print git.get_install_pkg_version()