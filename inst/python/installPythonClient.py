import sys   
import pip
import os
import urllib.request
import gzip
import tarfile
import shutil
import distutils.core
import distutils.log
import platform
from setuptools.command.install import install
import tempfile
import time
import importlib
import pkg_resources
import glob
import zipfile
import inspect
import subprocess
from patchStdoutStdErr import patch_stdout_stderr

def localSitePackageFolder(root):
    if os.name=='nt':
        # Windows
        return root+os.sep+"Lib"+os.sep+"site-packages"
    else:
        # Mac, Linux
        return root+os.sep+"lib"+os.sep+"python3.6"+os.sep+"site-packages"
    
def addLocalSitePackageToPythonPath(root):
    # clean up sys.path to ensure that synapser does not use user's installed packages
    sys.path = [x for x in sys.path if x.startswith(root) or "PythonEmbedInR" in x]

    sitePackages = localSitePackageFolder(root)
    # PYTHONPATH sets the search path for importing python modules
    if os.environ.get('PYTHONPATH') is not None:
      os.environ['PYTHONPATH'] += os.pathsep+sitePackages
    else:
      os.environ['PYTHONPATH'] = os.pathsep+sitePackages
    sys.path.append(sitePackages)
    # modules with .egg extensions (such as future and synapseClient) need to be explicitly added to the sys.path
    for eggpath in glob.glob(sitePackages+os.sep+'*.egg'):
        os.environ['PYTHONPATH'] += os.pathsep+eggpath
        sys.path.append(eggpath)


def _find_python_interpreter():
    # helper heuristic to find the bundled python interpreter binary associated
    # with PythonEmbedInR. we need it in order to be able to invoke pip via
    # a subprocess. it's not in the same place because of how we build
    # PythonEmbedInR differently the OSes.

    possible_interpreter_filenames = [
        'python',
        'python{}'.format(sys.version_info.major),
        'python{}.{}'.format(sys.version_info.major, sys.version_info.minor),
    ]
    possible_interpreter_filenames.extend(['{}.exe'.format(f) for f in possible_interpreter_filenames])
    possible_interpreter_filenames.extend([os.path.join('bin', f).format(f) for f in possible_interpreter_filenames])

    last_path = None
    path = inspect.getfile(os)
    while(path and path != last_path):
        for f in possible_interpreter_filenames:
            file_path = os.path.join(path, f)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                return file_path

        last_path = path
        path = os.path.dirname(path)

    # if we didn't find anything we'll hope there is any 'python3' interpreter on the path.
    # we're just going to use it to install some modules into a specific directory
    # so it doesn't actually even have to be the one bundled with PythonEmbedInR
    return 'python{}'.format(sys.version_info.major)


def main(path):
    patch_stdout_stderr()

    path = pkg_resources.normalize_path(path)
    moduleInstallationPrefix=path+os.sep+"inst"

    localSitePackages=localSitePackageFolder(moduleInstallationPrefix)

    addLocalSitePackageToPythonPath(moduleInstallationPrefix)

    os.makedirs(localSitePackages)

    # the least error prone way to install packages at runtime is by invoking
    # pip via a subprocess, although it's not straightforward to do so here.
    pip_packages = [
        'pandas==0.22',
        'synapseclient==2.0.0',
    ]

    if platform.system() != 'Windows':
        # on linux and mac we can install these via a pip subprocess...
        pip_packages.extend([
           "MarkupSafe==1.0",
           "Jinja2==2.8.1",
        ])

    else:
        # ...but on windows installing via a subprocess breaks seemingly with the wheel install,
        # so we use the creative sideloading as below.

        # Jinja2 depends on MarkupSafe
        packageName = "MarkupSafe-1.0"
        linkPrefix = "https://pypi.python.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/"
        installedPackageFolderName="markupsafe"
        simplePackageInstall(packageName, installedPackageFolderName, linkPrefix, path, localSitePackages)
        addLocalSitePackageToPythonPath(moduleInstallationPrefix)
        #import markupsafe  # This fails intermittently
    
        packageName = "Jinja2-2.8.1"
        linkPrefix = "https://pypi.python.org/packages/5f/bd/5815d4d925a2b8cbbb4b4960f018441b0c65f24ba29f3bdcfb3c8218a307/"
        installedPackageFolderName="jinja2"
        simplePackageInstall(packageName, installedPackageFolderName, linkPrefix, path, localSitePackages)
        addLocalSitePackageToPythonPath(moduleInstallationPrefix)
        #import jinja2 # This fails intermittently

    # the recommended way to call pip at runtime is by invoking a subprocess,
    # but that's complicated by the fact that we don't know where the python
    # interpreter is. usually you can do sys.executable but in the embedded
    # context sys.executable is R, not python. So we do a heuristic that to
    # find the interpreter. this seems to work better here than calling main
    # on pip directly which doesn't work for some of these packages (separately
    # from the other issues above...)
    interpreter = _find_python_interpreter()
    for package in pip_packages:
        rc = subprocess.call([interpreter, "-m", "pip", "install", package, "--upgrade", "--quiet", "--target", localSitePackages])
        if rc != 0:
            raise Exception("pip.main returned {} when installing {}".format(rc, package))

    addLocalSitePackageToPythonPath(moduleInstallationPrefix) 

# unzip directly into localSitePackages/installedPackageFolderName
# This is a workaround for the cases in which 'pip' and 'setup.py' fail.
# (They fail for MarkupSafe and Jinja2, without providing any info about what went wrong.)
def simplePackageInstall(packageName, installedPackageFolderName, linkPrefix, path, localSitePackages):
    # download 
    zipFileName = packageName + ".tar.gz"
    localZipFile = path+os.sep+zipFileName
    x = urllib.request.urlopen(linkPrefix+zipFileName)
    saveFile = open(localZipFile,'wb')
    saveFile.write(x.read())
    saveFile.close()
    
    tar = tarfile.open(localZipFile)
    tar.extractall(path=path)
    tar.close()
    os.remove(localZipFile)

    packageDir = path+os.sep+packageName
    os.chdir(packageDir)
    
    # inside 'packageDir' there's a folder to move to localSitePackages
    shutil.move(packageDir+os.sep+installedPackageFolderName, localSitePackages)
        
    os.chdir(path)
    shutil.rmtree(packageDir)
    
    sys.path.append(localSitePackages+os.sep+installedPackageFolderName)
