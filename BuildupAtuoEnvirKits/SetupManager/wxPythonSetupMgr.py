import logging, sys

_logger = logging.getLogger(__name__)

import os, re
import subprocess, time

from WinGUI.autoit.LocWrapper import AutoitLocator, WindowLocator, ControlLocator
from WinGUI.OperatorAdapter import click_dialog_button, close_window
from AbstractPackageSetupManager import PackageManager
from PackageUtils.WinUtils import is_x86_platform


class wxPythonSetupMgr(PackageManager):

    DEFAULT_INSTALL_PKG_NAME = 'wxPython'
    
    def __init__(self, 
                 sft_name='wxPython', 
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
        self.DEFAULT_INSTALL_PKG_NAME = "wxPython2.8-win32-unicode-2.8.12.1-py27.exe" if self._is_x86 \
                                        else "wxPython2.8-win64-unicode-2.8.12.1-py27.exe"
        
        self.install_pkg_search_ptn = '^(wxPython)(.*)(win32)(.*)(\.exe)$' if self._is_x86 \
                                        else '^(wxPython)(.*)(win64)(.*)(\.exe)$'
        

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
        installed_flag = False
        
        try:
            import wx
            _logger.debug("wxPython has been installed!")
            installed_flag = True
        except:
            pass
        
        '''
        python_path = None
        for path in os.listdir("C:\\"):
            if path.startwith('Python'): python_path = path
            else: continue 
            
        if python_path is not None:
            py_lib_path = os.path.join(python_path, 'Lib\\site-packages')
            for path in os.listdir(py_lib_path):
                if path.startwith('wx-'): installed_flag = True
        '''
        
        return installed_flag

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        
        subprocess.Popen(self.get_install_pkg_path())
          
        page1 = AutoitLocator()
        page1.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page1.control = ControlLocator("TNewButton1")
        click_dialog_button(loc=page1, timeout=5, action_log='Click Next')
         
        page2 = AutoitLocator()
        page2.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page2.control = ControlLocator("TNewRadioButton1")
        click_dialog_button(loc=page2, timeout=5, action_log='Click "I accept..."')
 
        page3 = AutoitLocator()
        page3.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page3.control = ControlLocator("TNewButton2")
        click_dialog_button(loc=page3, timeout=5, action_log='Click Next')
 
        page4 = AutoitLocator()
        page4.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page4.control = ControlLocator("TNewButton3")
        click_dialog_button(loc=page4, timeout=5, action_log='Click Next')
 
        page5 = AutoitLocator()
        page5.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page5.control = ControlLocator("TNewButton3", "")
        click_dialog_button(loc=page5, timeout=5, action_log='Click Next')

        time.sleep(15)
        page6 = AutoitLocator()
        page6.window = WindowLocator("[CLASS:TWizardForm; INSTANCE:1]")
        page6.control = ControlLocator("[CLASS:TNewCheckListBox; INSTANCE:1]", "left", 1, 9, 9)
        click_dialog_button(loc=page6, timeout=5*60, action_log='unclick View README...')
        
        page6.control = ControlLocator("TNewButton3")
        click_dialog_button(loc=page6, timeout=3*60, action_log='Click Finish...')
        
        
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
    
    inst = wxPythonSetupMgr()
    print inst.get_install_pkg_path(search_folder='C:\\Users\\alan\\Desktop\\Automation Install Package\\Package')
    