import logging, sys

_logger = logging.getLogger(__name__)

import subprocess

from AbstractPackageSetupManager import PackageManager

class PipPackageSetupMgr(PackageManager):
    
    DEFAULT_INSTALL_PKG_NAME = ''
    
    def __init__(self, 
                 sft_name='', 
                 need_install=False, 
                 need_update=False):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''

        self.sft_name = sft_name
        self.need_download  = False
        self.need_install   = need_install
        self.need_update    = need_update
        
    def get_install_pkg_path(self):
        '''
        '''
        return None

    def get_installed_version(self):
        '''
        '''
        command = 'pip show {0}'.format(self.sft_name)
        output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        
        return (0,0,0,0) if output=='' else output.split('\r\n')[3].split(':')[1].strip()
    
    def is_installed(self):
        '''
        '''
        command = 'pip show {0}'.format(self.sft_name)
        return True if subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0] != '' else False

    def do_install(self, pkg_path=None):
        '''
        '''
        command = 'pip install {0}'.format(self.sft_name)
        subprocess.call(command, shell=True)

    def do_update(self, pkg_path=None):
        '''
        '''
        command = 'pip install -U {0}'.format(self.sft_name)
        subprocess.call(command, shell=True)

if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S',
    )