# encoding: utf-8
import threading
import sys
import re
import os
import optparse
import base64
import stat
import fnmatch
import time
from hashlib import md5
import urllib2
import cgi
import datetime
from pluginsScan import *
from createHtml import createHtml
import client


absPath = ''

class PhpSerializer():

    @staticmethod
    def unserialize(s):
        return PhpSerializer._unserialize_var(s)[0]

    @staticmethod
    def _unserialize_var(s):
        return (
            {'i': PhpSerializer._unserialize_int
                , 'b': PhpSerializer._unserialize_bool
                , 'd': PhpSerializer._unserialize_double
                , 'n': PhpSerializer._unserialize_null
                , 's': PhpSerializer._unserialize_string
                , 'a': PhpSerializer._unserialize_array
            }[s[0].lower()](s[2:]))

    @staticmethod
    def _unserialize_int(s):
        x = s.partition(';')
        return (int(x[0]), x[2])

    @staticmethod
    def _unserialize_bool(s):
        x = s.partition(';')
        return (x[0] == '1', x[2])

    @staticmethod
    def _unserialize_double( s):
        x = s.partition(';')
        return (float(x[0]), x[2])

    @staticmethod
    def _unserialize_null(s):
        return (None, s)

    @staticmethod
    def _unserialize_string(s):
        (l, _, s) = s.partition(':')
        return (s[1:int(l) + 1], s[int(l) + 3:])

    @staticmethod
    def _unserialize_array(s):
        (l, _, s) = s.partition(':')
        a, k, s = {}, None, s[1:]
        for i in range(0, int(l) * 2):
            (v, s) = PhpSerializer._unserialize_var(s)

            if k:
                a[k] = v
                k = None
            else:
                k = v

        return (a, s[1:])


class ShellDetector():
    _extension = ["php", "asp", "txt"]

    _fileInfo = False
    #settings: show line number where suspicious function used
    _showlinenumbers = False
    #settings: used with access time & modified time
    _dateformat = "H:i:s d/m/Y"
    #settings: scan specific directory
    _directory = '.'
    #settings: scan hidden files & directories
    _report_format = 'shelldetector_%d-%m-%Y_%H%M%S.html'
    #settings: get shells signatures db by remote
    _remotefingerprint = False

    #default ouput
    _output = ""
    _badfiles = []
    _fingerprints = []
    _precomputed_fingerprints = []
    _filesCount = 0

    _resList = []
    _de = 0
    _se = 0
    #system: title
    _title = 'Shell Detector'
    #system: version of shell detector
    _version = '0.1'
    #system: regex for detect Suspicious behavior
    _regex = r"(?si)(preg_replace.*\/e|`.*?\$.*?`|\bpassthru\b|\bshell_exec\b|\bexec\b|\bbase64_decode\b|\beval\b|\bsystem\b|\bproc_open\b|\bpopen\b|\bcurl_exec\b|\bcurl_multi_exec\b|\bparse_ini_file\b|\bshow_source\b)"

    @staticmethod
    def end(options):
        ShellDetector.footer()

    @staticmethod
    def init(options):
        global absPath
        absPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        #set arguments
        if options.fileInfo is not None:
            ShellDetector._fileInfo = options.fileInfo

        ShellDetector._showlinenumbers = options.linenumbers

        if options.directory is not None:
            _directory = options.directory

        """if options.dateformat is not None:
            _dateformat = options.dateformat

        if options.format is not None:
            self._report_format = options.format"""

        ShellDetector._remotefingerprint = options.remote.lower() in ("yes", "true", "t", "1")


        if ShellDetector._remotefingerprint is True:
            ShellDetector.alert('Please note we are using remote shell database', 'yellow')
            url = 'http://10.1.128.159/hxdetectdetect.db'
            ShellDetector._fingerprints = urllib2.urlopen(url).read()
            try:
                ShellDetector._fingerprints = base64.decodestring(bytes(ShellDetector._fingerprints))
                ShellDetector._fingerprints = PhpSerializer.unserialize(str(ShellDetector._fingerprints))
            except IOError as e:
                print("({})".format(e))
        else:
            if os.path.isfile(absPath+"/config/hxdetect.db"):
                try:
                    ShellDetector._fingerprints = base64.decodestring(str(open(absPath+'/config/hxdetect.db', 'r').read()))
                    ShellDetector._fingerprints = PhpSerializer.unserialize(str(ShellDetector._fingerprints))
                except IOError as e:
                    print("({})".format(e))

        ShellDetector._get_precomputed_fingerprints()
        ShellDetector.header()

        loadPlus()

        ShellDetector._regex = re.compile(ShellDetector._regex)

    def start(self):
        self.header()

        #start
        self.remote()
        self.version()
#        self.filescan()
        self.anaylize()
        #end

        self.footer()
        return None


    @staticmethod
    def printResult():
#       +'d: '+str(ShellDetector._de)+'s:'+str(ShellDetector._se)
        ShellDetector.alert('Local Scaned Status: ' + str(ShellDetector._filesCount) + ' suspicious files and ' + str(len(ShellDetector._badfiles)) + ' shells', 'red')
        ShellDetector.getCloudResult();


    @staticmethod
    def getCloudResult():
        client.doGetCloud("WAIT");

    @staticmethod
    def outputResult(options):
        try:
            if options.output:
                fp = open(options.output + '.html', 'w')
            else:
                fp = open(absPath+'/output/report.html', 'w')
            html = createHtml(ShellDetector._resList)
            fp.write(html)
        finally:
            fp.close()

    @staticmethod
    def anaylize(files):
        if files is None:
            return True;
        _counter = 0

        _filename = files.replace("\\","/").replace("//","/")
        _content = open(_filename, 'rt', -1).read()
        _filename = re.sub('.#', '', _filename)

        pMatch = detectPlus(_content)

        if pMatch is not None:
            ShellDetector._de += 1
            _counter += 1
            ShellDetector._resList.append([_filename, pMatch])
            ShellDetector.alert('    ' + pMatch)
            ShellDetector.alert(_filename+'\n', 'yellow')
        else:
            rMatch = ShellDetector.fingerprint(_filename, _content)
            if rMatch is not None:
                 ShellDetector._se += 1
                 _counter += 1
                 ShellDetector._resList.append([_filename, rMatch])
                 ShellDetector.alert('    ' + rMatch)
                 ShellDetector.alert(_filename+'\n', 'yellow')
            else :
                tmatch = ShellDetector._regex.findall(_content)
                if tmatch:
#                    if ShellDetector._fileInfo:
#                        ShellDetector.getfileinfo(_filename)
#                    if ShellDetector._showlinenumbers is True:
#                        _lines = _content.split("\n")
#                        _linecounter = 1
#                        for _line in _lines:
#                            _match_line = ShellDetector._regex.findall(_line)
#                            if _match_line:
#                                ShellDetector.alert('   Suspicious function used: ' + _match_line.__str__() + '(line: ' + str( _linecounter) + ')')
#                            _linecounter += 1
#                    else:
                    ShellDetector.alert('   Suspicious functions used: ' + tmatch.__str__())
                    _counter += 1
                    ShellDetector._resList.append([_filename, 'Suspicious functions used,RULE:0_self'])
                    ShellDetector.alert(_filename+'\n', 'yellow')
        ShellDetector._filesCount += _counter
        if _counter > 0 :
            if ShellDetector._fileInfo:
                ShellDetector.getfileinfo(_filename)
            return False
        return True

    @staticmethod
    def _get_precomputed_fingerprints():
        if len(ShellDetector._precomputed_fingerprints)<1:
            for fingerprint, shellname in ShellDetector._fingerprints.iteritems():
                if fingerprint == "version":
                    continue
                if 'bb:' in fingerprint:
                    fingerprint = base64.decodestring(bytes(fingerprint.replace('bb:', '')))
                ShellDetector._precomputed_fingerprints.append((re.compile(re.escape(fingerprint)), shellname))

        return ShellDetector._precomputed_fingerprints

    @staticmethod
    def fingerprint(_filename, _content):
        for _regex, shellname in ShellDetector._get_precomputed_fingerprints():
            _match = _regex.findall(base64.b64encode(_content))
            if _match:
                ShellDetector._badfiles.append([_filename])
                _regex_shell = re.compile('^(.+?)\[(.+?)\]\[(.+?)\]\[(.+?)\]')
                _match_shell = list(_regex_shell.findall(shellname)[0])
                _shell_note = ''
                if _match_shell[2] == 1:
                    _shell_note = 'please note it`s a malicious file not a shell'
                elif _match_shell[2] == 2:
                    _shell_note = 'please note potentially dangerous file (legit file but may be used by hackers)'
                _shellflag = _match_shell[0] + '(' + _match_shell[3] + ')'
                tink = '   Fingerprint: Positive, it`s a ' + str(_shellflag) + ' ' + _shell_note
#                ShellDetector.alert(tink, 'red')
                return tink
        return None
    @staticmethod
    def unpack(self):
        """ Need to work on it"""

    @staticmethod
    def getfileinfo(_file):
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(_file)
        ShellDetector.alert('')
        ShellDetector.alert('=======================================================', 'yellow')
        ShellDetector.alert('')
        ShellDetector.alert('   Suspicious behavior found in: ' + _file)
        ShellDetector.alert('   Full path:     ' + os.path.abspath(_file))
        ShellDetector.alert('   Owner:         ' + str(uid) + ':' + str(gid))
        ShellDetector.alert('   Permission:    ' + oct(mode)[-3:])
        ShellDetector.alert('   Last accessed: ' + time.ctime(atime))
        ShellDetector.alert('   Last modified: ' + time.ctime(mtime))
        ShellDetector.alert('   Filesize:      ' + ShellDetector.sizeof_fmt(size))
        ShellDetector.alert('')

    @staticmethod
    def sizeof_fmt(num):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    @staticmethod
    def version():
        try:
            _version = ShellDetector._fingerprints['version']
        except ValueError:
            _version = 0
        try:
            _server_version = urllib2.urlopen('https://raw.github.com/emposha/PHP-Shell-Detector/master/version/db').read()
        except ValueError:
            _server_version = 0

        if _server_version == 0:
            ShellDetector.alert( 'Cant connect to server! Version check failed!', 'red')
        else:
            if _server_version < _version:
                ShellDetector.alert('New version of shells signature database found. Please update!', 'red')

        try:
            _app_server_version = urllib2.urlopen('https://raw.github.com/emposha/Shell-Detector/master/version/app').read()
        except urllib2.HTTPError:
            _app_server_version = 0

        if _app_server_version == 0:
            ShellDetector.alert('Cant connect to server! Application version check failed!', 'red')
        else:
            if _server_version < _version:
                ShellDetector.alert('New version of application found. Please update!', 'red')

    def filescan(self):
        ShellDetector.alert('Starting file scanner, please be patient file scanning can take some time.')
        ShellDetector.alert('Number of known shells in database is: ' + str(len(ShellDetector._fingerprints)))
        ShellDetector.listdir()
        ShellDetector.alert('File scan done, we have: ' + str(len(ShellDetector._files)) + ' files to analyze')

    def listdir(self):
        for root, dirnames, filenames in os.walk(ShellDetector._directory):
            for extension in ShellDetector._extension:
                for filename in fnmatch.filter(filenames, '*.' + extension):
                    ShellDetector._files.append(os.path.join(root, filename))
        return None

    @staticmethod
    def header():
        ShellDetector.alert('*************************************************************************************************')
        ShellDetector.alert('*                                                                                               *')
        ShellDetector.alert('*                                HongXin Detector                                               *')
        ShellDetector.alert('*                                      INNER                                                    *')
        ShellDetector.alert('*                                      V_0.1                                                    *')
        ShellDetector.alert('*                                                                                               *')
        ShellDetector.alert('*************************************************************************************************')
        ShellDetector.alert('')

    @staticmethod
    def footer():
        ShellDetector.alert('')
        ShellDetector.alert('*************************************************************************************************', 'green')
        ShellDetector.alert('*                                HongXin Detector                                                *')
        ShellDetector.alert('*                                      INNER                                                     *')
        ShellDetector.alert('*                                      V_0.1                                                     *')
        ShellDetector.alert('*                                                                                                *')
        ShellDetector.alert('*                                   GO ON the WAY                                                *', 'green')
        ShellDetector.alert('*                                                         author NI_GUOPING                      *', 'green')
        ShellDetector.alert('*************************************************************************************************', 'green')
        ShellDetector.alert('')

    @staticmethod
    def alert(_content, _color='', _class='info', _html=False, _flag=False):
        _color_result = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'purple': '\033[95m',
            'blue': '\033[94m',
            '': ''
        }[_color]

        if ShellDetector.supports_color() is True:
            print _color_result + _content + '\033[0m'
        else:
            print _content

        if _flag is True:
            ShellDetector.output(_content, _class, _html)

    @staticmethod
    def supports_color():
        """
        --- Taken from Django ---
        Returns True if the running system's terminal supports color, and False
        otherwise.
        """
        plat = sys.platform
        supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                      'ANSICON' in os.environ)
        # isatty is not always implemented, #6223.
        is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        if not supported_platform or not is_a_tty:
            return False
        return True
