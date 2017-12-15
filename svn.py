import re
import os
import subprocess

def runcmd(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)  
    return p.stdout.readlines()

class SVN:
    def __init__(self, path=None):
        self.info = {}

        self.info["workcopy"] = path
        self.info["repourl"] = None
        self.update()

    def set_repository(self, url):
        if not re.match(r'^https?:/{2}\w.+$', url):
            return False
        self.info["repourl"] = url

    def get_repository(self):
        return self.info["repourl"]

    def update(self):
        if self.info["workcopy"]:
            out = runcmd("svn info %s | grep ^URL: | awk '{print $2}'" % self.info["workcopy"])
            if len(out):
                self.info["repourl"] = out[0].split()

    def checkout(self):
        if self.info["repourl"] and self.info["workcopy"]:
            runcmd("svn co %s %s" % (self.info["repourl"], self.info["workcopy"]))