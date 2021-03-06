#!/usr/bin/env python

###############################################################################
#
# make_archive_tar.py - Create a tar file from a run directory.
#
# ARGS:
#   All: Run directories.
#
# SWITCHES:
#
# OUTPUT:
#   <STDOUT>:
#
# ASSUMPTIONS:
#
# AUTHOR:
#   Keith Bettinger
#
###############################################################################

#####
#
# IMPORTS
#
#####
from optparse import OptionParser
import os
import os.path
import sys

from rundir import RunDir
import rundir_utils

#####
#
# CONSTANTS
#
#####

#####
#
# FUNCTIONS
#
#####

#####
#
# SCRIPT BODY
#
#####

usage = "%prog [options] run_dir+"
parser = OptionParser(usage=usage)

parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  default=False,
                  help='Verbose mode [default = false]')
parser.add_option("-g", "--debug", dest="debug", action="store_true",
                  default=False,
                  help='Debug mode [default = false]')
parser.add_option("-a", "--deleteAfter", dest="deleteAfter", action="store_true",
                  default=False,
                  help='Delete the run directory after making the tar file [default = false]')
parser.add_option("-f", "--skipFileCheck", dest="skipFileCheck", action="store_true",
                  default=False,
                  help='Skip the check of the tar file for run dir files [default = false]')
parser.add_option("-d", "--destDir", dest="destDir", type="string",
                  default=None,
                  help='Where should the resulting tar file go? [default = root dirs of run directories]')
parser.add_option("-c", "--cif", dest="cif", action="store_true",
                  default=False,
                  help='Tar the intensity files (.cif) [default = false]')
parser.add_option("-s", "--ssh_socket", dest="ssh_socket", type="string",
                  default=None,
                  help="SSH Control Master socket to run all ssh commands through")


(opts, args) = parser.parse_args()

if (len(args) == 0):
    print >> sys.stderr, os.path.basename(__file__), ": No run directories given"
    sys.exit(1)

error_rundirs = 0
for arg in args:
    (root, dir) = os.path.split(os.path.abspath(arg))

    rundir = RunDir(root,dir)

    if rundir_utils.make_archive_tar(rundir, destDir=opts.destDir, verbose=opts.verbose, debug=opts.debug,
                                     fileCheck=not opts.skipFileCheck, deleteAfter=opts.deleteAfter,
                                     cif=opts.cif, sshSocket=opts.ssh_socket):
        print >> sys.stderr, "make_archive_tar.py: %s failed" % rundir.get_dir()
        error_rundirs += 1

sys.exit(error_rundirs)

