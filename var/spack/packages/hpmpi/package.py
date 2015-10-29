from spack import *
import os
import spack
import sys

class Hpmpi(Package):
    """HP-MPI/PlatformMPI is a proprietary implementation of
       the Message Passing Interface (MPI) standard."""
    homepage = "http://www.ibm.com/systems/fr/platformcomputing/products/mpi/index.html"

    pkg_dir = spack.db.dirname_for_package_name("hpmpi")

    # fake tarball because we consider it is already installed
    version('9.1.0', '7b878b76545ef9ddb6f2b61d4c4be833',
            url = "file:"+join_path(pkg_dir, "empty.tar.gz"))

    provides('mpi@:2.2')

    def setup_dependent_environment(self, module, spec, dep_spec):
        """For dependencies, make mpicc's use spack wrapper."""
        os.environ['HPMPI_CC']  = 'cc'
        os.environ['HPMPI_CXX'] = 'c++'
        os.environ['HPMPI_F77'] = 'f77'
        os.environ['HPMPI_F90'] = 'f90'
        # mpicc/mpiCC/mpif77 option for using multithread MPI library
        os.environ['MPI_CC_OPTIONS']  = "-lmtmpi"
        os.environ['MPI_CXX_OPTIONS'] = "-lmtmpi"
        os.environ['MPI_F77_OPTIONS'] = "-lmtmpi"
        os.environ['MPI_F90_OPTIONS'] = "-lmtmpi"

    def install(self, spec, prefix):
        mpiroot='/opt/hpmpi/'
        if os.path.isdir(mpiroot):
            os.environ['MPI_ROOT'] = mpiroot
            os.symlink(mpiroot+"lib/linux_amd64/", prefix.lib)
            os.symlink(mpiroot+"etc/", prefix.etc)
            os.symlink(mpiroot+"share/", prefix.share)
            os.symlink(mpiroot+"bin/", prefix.bin)
            os.symlink(mpiroot+"include/", prefix.include)
        else:
            sys.exit(mpiroot+' directory does not exist.'+' Do you really have hpmpi installed in '+mpiroot+' ?')