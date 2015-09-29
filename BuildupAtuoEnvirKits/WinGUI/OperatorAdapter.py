import logging, sys
_logger = logging.getLogger(__name__)

from win32com.client import Dispatch

def click_dialog_button(loc, timeout=5, retry=3, action_log=''):
    '''
    '''
    autoit = Dispatch("AutoItX3.Control") 
    
    autoit.WinWaitActive(loc.window.title, loc.window.text, timeout)
    
    for count in range(0, retry):
        autoit.WinWait(loc.window.title, loc.window.text, timeout)
        autoit.WinActivate(loc.window.title, loc.window.text)

        try:
            if loc.control.x is not None \
                and autoit.ControlClick(loc.window.title, 
                                        loc.window.text, 
                                        loc.control.id, 
                                        loc.control.button, 
                                        loc.control.clicks, 
                                        loc.control.x, 
                                        loc.control.y):
                    _logger.info("do '%s' with coords" %action_log)
                    return True
                
            elif autoit.ControlClick(loc.window.title, 
                                     loc.window.text, 
                                     loc.control.id, 
                                     loc.control.button, 
                                     loc.control.clicks, 
                                     ):
                    _logger.info("do '%s' with control ID" %action_log)
                    return True
            else:
                _logger.error("parameter error...(%s)" %action_log)
                return False

        except Exception:
            raise("Exception while ControlClick...(%s)" %action_log)

        _logger.debug("retry counter: %s...(%s)" %(str(count), action_log))
        time.sleep(2)

    _logger.error("do '%s' fail..." %action_log)
    return False

def close_window(loc, timeout=0, retry=3, action_log=''):
    '''
    '''
    autoit = Dispatch("AutoItX3.Control")
    
    if autoit.WinClose(loc.window.title, loc.window.text):
        _logger.debug(action_log)
        return True
    else:
        _logger.warn('do "{0}" fail.'.format(action_log))
        return False

def choose_dropdown_box(loc, timeout=0, retry=3, action_log=''):
    '''
    '''
    autoit = Dispatch("AutoItX3.Control")
    
    _logger.info("select '%s' in dropdown box" %(loc.control.sel_str))
    
    autoit.ControlCommand(loc.window.title, 
                          loc.window.text, 
                          loc.control.id,
                          "SelectString", loc.control.sel_str)
    
if __name__ == '__main__':
    '''
    '''
    logging.basicConfig(
        format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S',
    )
    pass