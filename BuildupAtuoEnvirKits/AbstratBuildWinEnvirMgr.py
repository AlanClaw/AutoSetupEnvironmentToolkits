import logging, sys

_logger = logging.getLogger(__name__)

import traceback

from PackageUtils.WinUtils import is_x86_platform


class BuildEnvTemplate(object):
    
    _is_x86 = None
    _root_logger = None
    _pkg_mgr_dict = None
    
    def __init__(self, log_filename='install.log'):
        '''
        '''
        self._setup_log(log_filename)
        self._pkg_mgr_dict = {}
        self._is_x86 = is_x86_platform()
        
    
    def _setup_log(self, filename=None):
        '''
        '''
        log_formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]",
                                 datefmt = '%y-%m-%d %H:%M:%S')
        
        self._root_logger = logging.getLogger()

        if filename is not None:
        
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(log_formatter)
            self._root_logger.addHandler(file_handler)
        
#         console_handler = logging.StreamHandler(sys.stdout)
#         console_handler.setFormatter(log_formatter)
#         self._root_logger.addHandler(console_handler)
        
        self._root_logger.setLevel(logging.DEBUG)

    def add_pkg_mgr(self, pkg_mgr_obj, pkg_name):
        '''
        '''
        self._pkg_mgr_dict[reg_name] = pkg_mgr_obj

    def setup_environment(self, pkg_mgr_order):
        '''
        @param pkg_mgr_order: give a order list of pkg_mgr_obj(PackageManager)
        @type pkg_mgr_order: []
        '''
        for pkg_mgr in pkg_mgr_order:
            
            try:
                if pkg_mgr.need_download:
                    pkg_mgr.download_pkg()
    
                if pkg_mgr.need_install and not pkg_mgr.is_installed():
                    pkg_mgr.do_install( pkg_mgr.get_install_pkg_path() )
    
                elif pkg_mgr.need_update:
                    if not pkg_mgr.is_installed():
                        pkg_mgr.do_install( pkg_mgr.get_install_pkg_path() )
                    pkg_mgr.do_update( pkg_mgr.get_install_pkg_path() )
                else:
                    pass

            except:
                _logger.error('!!! install {0} fail'.format(pkg_mgr.sft_name))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                _logger.error('!!!'.join(line for line in lines))
                continue

    @property
    def pkg_mgr_dict(self):
        '''
        @note: return the package object dict 
        '''
        return self._pkg_mgr_dict



if __name__ == '__main__':
    '''
    '''
    inst = BuildEnvTemplate('install.log')
    print inst._is_x86
#     inst = BuildEnvTemplate()