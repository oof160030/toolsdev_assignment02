import logging

import pymel.core as pmc
import maya.cmds as cmds
import re
import os
from pymel.core.system import Path

log = logging.getLogger(__name__)

class SceneFile(object):
    """This class represents a DCC software scene file

    Predefine naming conventions when naming new methods.

    Attributes:
        dir (str, optional): Directory to scene file, defaults to ''
        descriptor (str, optional): Short descriptor of scene file, defaults to "main"
        version (int, optional): Version number, defaults to 1
        ext (str, optional): Extension. Defaults to "ma"
    """

    def __init__(self, dir='', descriptor='main',version=1, ext="ma"):
        """Defines class properties when created (like constructor)"""
        filePath = Path(os.path.normpath(cmds.file(query=True, sn=True, shortName=False, withoutCopyNumber=True)))
        filePathSplit = os.path.split(filePath)
        regex = r'([a-zA-Z]+)_v([0-9]+).([a-z]+)'
        if(re.match(regex,filePathSplit[1])):
            filePathDescriptor = filePathSplit[1].split("_")
            filePathVersion = filePathDescriptor[1].split(".")
            filePathNum = self._extractNum(filePathVersion[0])
            self._dir = Path(filePathSplit[0])
            self.descriptor = filePathDescriptor[0]
            self.version = filePathNum
            self.ext = filePathVersion[1]
        else:
            self._dir = dir
            self.descriptor = descriptor
            self.version = version
            self.ext = ext

    @property
    def dir(self):
        return Path(self._dir)

    @dir.setter
    def dir(self, arg):
        self._dir = Path(arg)

    def basename(self):
        """Returns a scene file name as a string
        e.g. ship_v001.ma"""
        name_pattern = "{descriptor}_v{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor,
                            version=self.version,
                            ext=self.ext)
        return name

    def path(self):
        """Returns a path to scene file"""
        return Path(self.dir) / self.basename()

    def _parseFile(self, fileNames, searchVal):
        """Returns highest number associated with matching search value"""
        highestValue = -1
        for file in fileNames:
            f_split = file.split(".")
            f_Version = f_split[0].split("_")
            if len(f_Version) < 2:
                pass
            elif searchVal in f_Version:
                for el in f_Version:
                    test = self._extractNum(el)
                    if test > highestValue:
                        highestValue = test
        print(highestValue)
        return highestValue


    def _extractNum(self, x):
        """Extracts all digits in a string, then returns as an integer"""
        str = ''.join(filter(lambda i: i.isdigit(), x))
        if str == '':
            str = '0'
        return int(str)

    def save(self):
        """Saves the scene file.
        Returns:
            :obj:'Path': Path to scene file, or None otherwise"""
        try:
            pmc.system.saveAs(self.path())
        except RuntimeError:
            log.warning("Directory missing. Generating new directory...")
            self._dir.makedirs_p()
            pmc.system.saveAs(self.path())
        pass

    def increment_and_save(self):
        """Detects any existing files, and determines the next version to save"""
        allFiles = os.listdir(self.dir)
        saveVersion = self._parseFile(allFiles, self.descriptor)
        if saveVersion == -1:
            self.version = 1
            self.save()
        else:
            print(self.version)
            saveVersion = saveVersion + 1
            self.version = saveVersion
            print(self.version)
            self.save()