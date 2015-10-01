import logging
_logger = logging.getLogger(__name__)

import os

logging.basicConfig(
    format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
    level = logging.DEBUG,
    datefmt = '%m/%d/%y %H:%M:%S'
)

JUCTION_EXE_FOLDER = os.path.join(os.curdir, "Package", "Junction", "junction.exe")


def get_file_version_number(filename):
    """
    @requires: pywin32 library should be installed for invoking win32api
    @return: tuple of Windows file version, ex:(5,7,0,2221)
    @rtype: tuple 
    """
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
    try:
        info = GetFileVersionInfo (filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
    except:
        _logger.error("get %s version fail."%filename)
        return 0,0,0,0
    

def get_desktop_path():
    """
    HKEY_CURRENT_USER
    """
    import _winreg

    desktop_path = ""

    aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
    aKey = _winreg.OpenKey(aReg, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")

    try:
        val= _winreg.QueryValueEx(aKey, "Desktop")            
        _logger.debug("reg key value:%s" %str(val))
        desktop_path = str(val[0])
        
    except EnvironmentError:
        print traceback.format_exc()
        print sys.exc_info()[0]       

    return desktop_path

def is_x86_platform():
    """
    @note:
    @rtype: bool
    """
    import os

    return not os.environ.has_key("PROGRAMFILES(X86)")

def set_softlink(source, target):
    """
    """
    import platform, subprocess
    
    release_version = platform.release()
    if ("XP" in release_version) or ("2003" in release_version):
        cmd = '"%s" "%s" "%s"' % (JUCTION_EXE_FOLDER, source, target)
        _logger.info(cmd)
        subprocess.Popen(cmd, shell = True)
        title = "Junction License Agreement"
        self._click_dialog_button(title = title,
                               text = "command-line switch to accept the EULA",
                               control_id = "Button1",
                               waiting_time = 60,
                               action_log = "Click Agree"
                               )
    else:
        cmd = 'MKLINK /J "%s" "%s"' % (source, target)
        _logger.info(cmd)
        subprocess.Popen(cmd, shell = True) 

def windows_version_should_in_range(min_ver = "0.0.0000", max_ver = "9.9.9999", need_return = False):
    """
    @param min_ver: minimum version
    @param max_ver: maxmum version
    @param need_return: True -> return boolean value, False -> raise Exception if condition not be satisfied  
    @note: 
    Windows7 SP0: 6.1.7600
    Windows7 SP1: 6.1.7601
    Windows8 SP0: 6.2.9200
    etc...
    @return: if need return boolean value, need_return=True must be assigned
    @example:  windows_version_should_in_range(min_ver = "6.1.7600", max_ver = "6.1.7600") # means Windows version should exactly equal to 6.1.7600
    """
    import re, platform
    
    assert cmp( platform.system(), 'Windows' ) == 0    
    # get current Windows version
    win_ver = platform.version()
    _logger.info("Windows version:%s, min_ver:%s, max_ver:%s" %(win_ver, min_ver, max_ver))
    # make sure the format match
    verion_regular_format = re.compile("[0-9]\.[0-9]\.[0-9]{4}$")
    min_regular_group = verion_regular_format.match(min_ver)
    max_regular_group = verion_regular_format.match(max_ver)
    win_ver_regular_group = verion_regular_format.match(win_ver)
    assert min_regular_group is not None, "min_ver format error, ex:6.1.7600"
    assert max_regular_group is not None, "max_ver format error, ex:6.1.7600"
    assert win_ver_regular_group is not None, "win_ver format error, ex:6.1.7601"
    assert max_ver >= min_ver, "max_ver must '>=' min_ver"
    # should in this range
    if win_ver < min_ver:
        if not need_return:
            raise Exception("Windows version too old")
        return False
    elif win_ver > max_ver:
        if not need_return:
            raise Exception("Windows version too new")
        return False
    elif (not cmp(win_ver, max_ver)) and (not cmp(win_ver, min_ver)):
        _logger.info("Windows version is %s" %platform.version())
    else:
        _logger.info("Windows version in target range.")
    if need_return:
        return True