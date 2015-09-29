import logging, sys

_logger = logging.getLogger(__name__)

import os, re

DEFAULT_PKG_FOLDER  = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Package'))
PKG_DWNLOD_CFG_FILE = os.path.join(DEFAULT_PKG_FOLDER, 'software.ini')

class PackageManager(object):


    DEFAULT_INSTALL_PKG_NAME = ''

    def __init__(self, 
                 sft_name, 
                 need_download=False, 
                 need_install=False, 
                 need_update=False,
                 pkg_folder=None):
        '''
        @param sft_name: give a software(package) name for this package manager. 
                         If you need invoke download_pkg(),
                         you should ensure this name already define in the configure such as 'software.ini'
        '''
        
        pkg_folder = DEFAULT_PKG_FOLDER if pkg_folder is None else pkg_folder
        if not os.path.isdir(pkg_folder): os.mkdir(pkg_folder)
        self.sft_name = sft_name
        
        self.need_download  = need_download
        self.need_install   = need_install
        self.need_update    = need_update
        
        self.install_pkg_search_ptn = self.DEFAULT_INSTALL_PKG_NAME

        self._installed_prog_path = None
        
    def download_pkg(self, 
                     pkg_name=None, 
                     to_path=DEFAULT_PKG_FOLDER, 
                     dwnlod_cfg_file=PKG_DWNLOD_CFG_FILE):
        '''
        @note: for implement method to download latest package
        @param pkg_name: which is section(software) name in ini format such as 'software.ini'
                         for more information, please refer to PackageUtils.FileDownloadHelper.SoftwareSpider
        '''
        from PackageUtils.FileDownloadHelper import SoftwareSpider as SoftwareSpider
        
        pkg_name = self.sft_name if pkg_name is None else pkg_name
        
        try:
            sft_spider = SoftwareSpider(dwnlod_cfg_file, to_path)
            sft_spider.downlaod_pkg(pkg_name)
        except Exception, e:
            _logger.exception(e)
            _logger.error('download {0} fail!' %(pkg_name))
            return False
        
        return True
    
    def get_install_pkg_path(self, search_folder=DEFAULT_PKG_FOLDER, search_ptn=None):
        '''
        @note: this method aim to search the correct package from the specified search_folder
        @param search_folder: assign the search_folder which should contain the install package.
        @return: return a full search_folder of install package name from the specified folder, 
                 user may need to compare the install file between versions
        @rtype: str 
        '''
        search_ptn = self.install_pkg_search_ptn if search_ptn is None else search_ptn
        
        _logger.debug('search in "{0}", pattern:"{1}"'.format(search_folder, search_ptn))
        matched_files = []
        
        search_ptn = re.compile(search_ptn)
        # get all files in the search_folder
        for path in os.listdir(search_folder):
            if os.path.isfile(os.path.join(search_folder, path)):
                file_name = os.path.basename(path)
                if re.search(search_ptn, file_name): 
                    matched_files.append(path)
                    _logger.debug('file name matched: %s' %file_name)
                    continue 
        
        if len(matched_files) == 0: 
            _logger.debug('no pattern matched file.')
            install_pkg_name = self.DEFAULT_INSTALL_PKG_NAME
            
        elif len(matched_files) == 1:
            install_pkg_name = matched_files[0]
        else:
            # choose latest one from those choosen files
            choose_file = matched_files[0]
            for file in matched_files:
                choose_file = file if file > choose_file else choose_file
            install_pkg_name = choose_file
        
        install_pkg_path = os.path.join(search_folder, install_pkg_name)
        _logger.debug('Find install package: {0}'.format(install_pkg_path))
        return install_pkg_path
    
    @property
    def installed_prog_path(self):
        '''
        @note: 
        '''
        return self._installed_prog_path

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
        
    def is_installed(self, possible_install_paths):
        '''
        @note: assign a path list or a single path to  determine the program has been installed or not
        @type possible_install_paths: str or list
        '''
        installed_flag = False
        
        if type(possible_install_paths) is str:
            if os.path.exists(possible_install_paths):
                installed_flag = True
                self._installed_prog_path = possible_install_paths
            
        elif type(possible_install_paths) is list:
            
            for path in possible_install_paths:
                if os.path.exists(path):
                    self._installed_prog_path = path
                    installed_flag = True
                    _logger.debug('{0} exist!'.format(path))
                    break
                                
        return installed_flag
    
    def is_installed_latest(self):
        '''
        @note: return False if not up-to-date, need to implement this method after inherited this object.
        '''
        raise NotImplementedError('You need to define a compare method!')

    def do_install(self, pkg_path):
        '''
        @note: execute install process
        '''
        raise NotImplementedError('You need implement this function!')
    
    def do_update(self, pkg_path):
        '''
        @note: execute update process
        '''
        raise NotImplementedError('You need implement this function!')
    
if __name__ == '__main__':
    '''
    '''
    pass