import ftplib, logging, os, re, sys, traceback

class Downloader(object):
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def run(self):
        self.firefox()
        
    def firefox(self, 
                url = "ftp.mozilla.org", 
                path = "/pub/mozilla.org/firefox/releases/latest/win32/en-US/", 
                pattern = "^Firefox[\s]+(Setup[\s]+)?[0-9\.]+(.exe|.dmg)$"):
        ret = None
        try:
            ftp = ftplib.FTP(url)
            ftp.login()
            ftp.cwd(path)
            ret = self.get_file_from_ftp(ftp, pattern)
            ftp.quit()
        except:
            ret = None
            self.logger.debug(traceback.format_exc())
        finally:
            return ret
    
    def get_file_from_ftp(self, ftp, pattern):
        path = None
        try:
            files = self.get_list_from_ftp(ftp)
            compile = re.compile(pattern)
            for temp in files:
                if re.match(pattern, temp):
                    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), temp)
                    if os.path.exists(path):
                        os.remove(path)
                    with open(path, "wb") as output:
                        print "%(name)s is downloading..." % dict(name=temp)
                        ftp.retrbinary("RETR %(name)s" % dict(name=temp), output.write)
                    break
        except:
            path = None
            self.logger.debug(traceback.format_exc())
        finally:
            return path
    
    def get_list_from_ftp(self, ftp):
        files = list()
        try:
            files = ftp.nlst()
        except ftplib.error_perm, resp:
            files = list()
            if str(resp) == "550 No files found":
                print "No files in %(path)s" % dict(path=ftp.pwd()) 
        finally:
            return files
        
if __name__ == "__main__":
    downloader = Downloader()
    downloader.run()