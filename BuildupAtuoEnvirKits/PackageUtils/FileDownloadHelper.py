import logging, sys
_logger = logging.getLogger(__name__)

import os, ConfigParser, re, shutil
import urlparse, urllib, urllib2

# add for ssl certificate verification error
if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

from HTMLParser import HTMLParser

"""
@attention: Please have the following dependence module to execute this program
pip html5lib
pip BeautifulSoup4
pip install requests 
"""

def main():
    """
    """
    logging.basicConfig(
        format = '[%(asctime)s][%(levelname)s][%(funcName)s] - %(message)s [%(filename)s:%(lineno)d]',
        level = logging.DEBUG,
        datefmt = '%m/%d/%y %H:%M:%S'
    )
    
    fld_path = os.path.join(os.environ['userprofile'], 'Desktop', 'test_dir')
    
    sft_spider = SoftwareSpider('software.ini', fld_path)
#     sft_spider.downlaod_pkg('Notepad++')
    sft_spider.downlaod_pkg()
    

class MyHTMLParser(HTMLParser):
    _links = list()
    
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, print it.
                if name == "href":
                    self._links.append(value)

class SoftwareSpider(object):
    """
    @note: This class is aim to auto get software by a defined software pattern
    """
    
    _sft_ini = None
    _sft_dir = None
    _config = None
    
    def __init__(self, sft_ini, sft_dir = None):
        """
        """
        self._sft_ini = sft_ini
        self._sft_dir = sft_dir
        
        self._sft_name_dict = dict()
        
        if self._sft_dir is None:
            self._sft_dir = os.getcwd()

    def downlaod_pkg(self, sft_specified = None, cur_pkg_name = None):
        """
        @param sft_specified: assign a target software name which has been defined in ini file 
                              or 'None' to download all packages as ini define
        @param cur_pkg_name: assign to determine does it need to download a new version package.
        """
        # check all the softwares from base folder to see if need download or not
        # download all the software from list and show the status 
        
        for sft_name in self.get_ini_reader.sections():
            if sft_specified and sft_specified.lower() not in sft_name.lower():
                continue
            
            # from page to find out target download link
            # create thread to download the software to '_sft_dir'
            url = self.get_ini_reader.get(sft_name, "download_page")
            url_ptn = self.get_ini_reader.get(sft_name, "download_link_ptn")
            download_link = self.get_download_link(sft_name, url, url_ptn)
            
            _logger.debug("dwonload_link: %s, cur_pkg_name: %s" %(download_link, cur_pkg_name))
            file_name = self._download_file(download_link, cur_pkg_name)
            self._sft_name_dict[sft_specified if sft_specified else sft_name] = str(file_name)
                
        return self._sft_name_dict.get(sft_specified) if sft_specified else self._sft_name_dict
            
    @property
    def get_ini_reader(self):
        
        if self._config is None:
            self._config = ConfigParser.SafeConfigParser()
            self._config.optionxform = str
            self._config.read(self._sft_ini)
        
        return self._config
        
    def get_download_link(self, sft, url, link_ptn):
        """
        """
        _logger.debug("url:%s\nsearch download pattern:%s" %(url, link_ptn))
        
        # get content from page and filter links
        matchs = self._parse_link(url, link_ptn)
        if len(matchs) != 1:
            _logger.debug("match links:")
            _logger.debug(matchs)
            print "Multiple links found!! Choose the first one..."
            
        download_link = matchs[0]

        if self.get_ini_reader.has_option(sft, "dwonload_link_host"):
            download_link = self.get_ini_reader.get(sft, "dwonload_link_host") + download_link
        
        if self.get_ini_reader.has_option(sft, "redirect_link_ptn"):
            
            redirect_ptn = self.get_ini_reader.get(sft, "redirect_link_ptn")
            _logger.debug('search for link to match: {0}'.format(redirect_ptn))
            matchs = self._parse_link(download_link, redirect_ptn)
            sub_link = matchs
            
            if len(sub_link) > 1 and self.get_ini_reader.has_option(sft, "download_link_after_redirect_ptn"):
                match_redirect_pth = self.get_ini_reader.get(sft, "download_link_after_redirect_ptn")
                _logger.debug('match_redirect_pth: {0}'.format(match_redirect_pth))
                re_format = re.compile(match_redirect_pth)
                matchs = [link for link in matchs if re_format.match(link) is not None]
                _logger.debug("match: {0}".format(matchs))
                sub_link = self._get_unique_link(matchs) if len(matchs) > 1 else matchs[0] 
            
            download_link = self.get_ini_reader.get(sft, "dwonload_link_host") + sub_link
            
        return download_link
    
    def _parse_link(self, url, ptn):
        all_links = list()
        page = urllib2.urlopen(url)
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(page.read(), 'html5lib')
            links = soup.findAll('a')
            for link in links:
                try:
                    _logger.debug("link string:%s" %link.string)
                    _logger.debug(link['href'])
                    all_links.append(link['href'])
                except:
                    logging.exception('_parse_link fail')
        except:
            parser = MyHTMLParser()
            parser.feed(page.read())
            all_links = parser._links
                
        # find target link from all links
        re_format = re.compile(ptn)
        matchs = [link for link in all_links if re_format.match(link) is not None]
        
        _logger.debug("Match links:")
        _logger.debug(matchs)

        return matchs
    
    def _get_unique_link(self, links):
        '''
        '''
        choosed_link = ''
        
        for link in links:
            choosed_link = link if link > choosed_link else choosed_link
        
        return choosed_link
    
    def _download_file(self, url, file_name = None, to_cmp_file_name = None):
        """
        @note: Used to download file from url link
        @param to_cmp_file_name: used to decide whether this file should be downloaded or not.
        @param file_name: assign the file name
        """
        # check folder exist or not
        if not os.path.isdir(self._sft_dir):
            os.makedirs(self._sft_dir)
        
        request_url = urllib2.urlopen(urllib2.Request(url))
        download_file = urllib2.urlopen(url)
        
        try:
            file_name = file_name or self._get_file_name(url, request_url)
            
            if self.compare_pkg_ver_by_name(file_name, to_cmp_file_name):
                file_path = os.path.join(self._sft_dir, file_name)
                _logger.debug("download to path = %s" %file_path)
                with open(file_path, 'wb') as fout:
                    shutil.copyfileobj(request_url, fout)
            else:
                _logger.warning("ignore to download file = %s" % file_name)
        finally:
            request_url.close()
            return file_name

    def _get_file_name(self, url, openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from it
            cd = dict(map(
                lambda x: x.strip().split('=') if '=' in x else (x.strip(), ''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: return filename
        
        # if no filename was found above, parse it out of the final URL.
        name = os.path.basename(urlparse.urlsplit(openUrl.url)[2])
        return urllib.unquote(name).decode('utf8')

    def _get_redirected_url(self, url):
        import requests
        
        response = requests.get(url)
        if response.history:
            _logger.debug("Request was redirected")
            for resp in response.history:
                _logger.debug(resp.status_code, resp.url)
            _logger.debug("Final destination:")
            _logger.debug(response.status_code, response.url)
        else:
            _logger.debug("Request was not redirected")

    def compare_pkg_ver_by_name(self, sft_name1, sft_name2=None):
        """
        @note: if sft_name2 not given, this function will always return True.
        @return: return True if sft_name1 > sft_name2
        """
        if not sft_name2:
            return True
        
        version1 = re.findall(r"([0-9]+[0-9\.]+[0-9]+)+", sft_name1)[0]
        version2 = re.findall(r"([0-9]+[0-9\.]+[0-9]+)+", sft_name2)[0]
        return True if str(version1) > str(version2) else False

if __name__ == "__main__":
    '''
    '''
    main()
    