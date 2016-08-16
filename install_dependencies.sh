# Ensure we're in a virtualenv.
if [ "$VIRTUAL_ENV" == "" ]
then
    echo "ERROR: not in a virtual environment."
    exit -1
fi

# Setup variables.
CACHE="/tmp/install-pygtk-$$"

# Make temp directory.
mkdir -p $CACHE

# Test for py2cairo.
echo -e "\E[1m * Checking for cairo...\E[0m"
python -c "
try: import cairo; raise SystemExit(0)
except ImportError: raise SystemExit(-1)"

if [ $? == 255 ]
then
    echo -e "\E[1m * Installing cairo...\E[0m"
    # Fetch, build, and install py2cairo.
    (   cd $CACHE
        curl 'http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2' > "py2cairo.tar.bz2"
        tar -xvf py2cairo.tar.bz2
        (   cd py2cairo*
            autoreconf -ivf
            ./configure --prefix=$VIRTUAL_ENV --disable-dependency-tracking
            make
            make install
        )
    )
fi

# Test for gobject.
echo -e "\E[1m * Checking for gobject...\E[0m"
python -c "
try: import gobject; raise SystemExit(0)
except ImportError: raise SystemExit(-1)"

if [ $? == 255 ]
then
    echo -e "\E[1m * Installing gobject...\E[0m"
    # Fetch, build, and install gobject.
    (   cd $CACHE
        curl 'http://ftp.acc.umu.se/pub/GNOME/sources/pygobject/3.12/pygobject-3.12.2.tar.xz' > 'Pygobject.tar.xz'
        tar -xvf Pygobject.tar.xz
        (   cd pygobject*
            ./configure --prefix=$VIRTUAL_ENV --disable-introspection
            make
            make install
        )
    )
fi
