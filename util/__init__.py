import os, logging, __main__, sys, yaml
import logging.handlers

# look for a config file in these directories, in this order:
directories = [ os.path.dirname(__main__.__file__) if hasattr(__main__, '__file__') else None,                      # directory of main (if exists)
                '.',                                                                                                # current working directory
                os.path.join(os.path.dirname(__file__)),                                                            # the directory of config.yaml
                os.path.join(os.path.dirname(__file__), ".."),                                                      # the directory above config.yaml
                os.path.join(os.path.dirname(__main__.__file__), "..") if hasattr(__main__, '__file__') else None   # the directory above main
                ]
directories = [directory for directory in directories if directory is not None]

class Config(dict):

    def __init__(self, conf=None):    
        self.conf = None
        i = 0
        while conf is None or not os.path.isfile(conf):
            conf = os.path.abspath(os.path.join(directories[i], "config.yaml"))
            smp = os.path.abspath(os.path.join(directories[i], "config.yaml.smp"))
            if not os.path.isfile(conf) and os.path.isfile(smp):
                shutil.copyfile(smp, conf)  
            i += 1
            if i == len(directories):
                # no config file
                dict.__init__(self)
                return
        self.conf = conf
        f = open(self.conf)                
        data = yaml.load(f)
        if data is not None:
            dict.__init__(self, data)
        f.close()
        
    def __missing__(self, key):
        raise ConfigError(key, self.conf)


class ConfigError(Exception):
    def __init__(self, key, conf):
        self.key = key
        self.conf = conf
    def __str__(self):
        return repr("No '%s' in config (%s)" % (self.key, self.conf))
        
            
config = Config()

try:
    name = os.path.basename(__main__.__file__).split('.')[0]    # log identifier/file will be the same as the file being run
    if name == "__main__":
        name = os.path.dirname(__main__.__file__).split('/')[-1]
except AttributeError:
    name = "main"                       ## custom
    
log = logging.getLogger(name)
log.setLevel(logging.DEBUG)
log.propagate = False

logpath = None
logdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
if not os.path.isdir(logdir):
    os.makedirs(logdir)
logpath = os.path.join(logdir, "%s.log" % name)
logfile = logging.handlers.TimedRotatingFileHandler(logpath, 'midnight', encoding="utf-8")
logfile.setLevel(logging.DEBUG)
log.addHandler(logfile)

formatter = logging.Formatter("%(asctime)s |%(levelname)s| %(message)s <%(filename)s:%(lineno)d>")            

logfile.setFormatter(formatter)

log.info("Loaded config from %s" % config.conf)
if logpath is not None:
    log.info("Writing logs to %s" % logpath)

def exc(e):
    return "%s <%s:%s> %s" % (sys.exc_info()[0].__name__, os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1], sys.exc_info()[2].tb_lineno, e)

log.exc = exc

