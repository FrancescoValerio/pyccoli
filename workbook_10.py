from input_gen import example5
# We need to put this in a function to allow python multiprocessing
# to work.

def make_files():
    """
        Make all the files that we'll need for PYCCOLI
    """

    example5()

#Now that we have the files we can run PYCCOLI

from pyccoli import pyccoli
def run_pyccoli():
    pyccoli('ixdow_5y_close')

#Uncomment to run pyccoli

if __name__ == "__main__":
    make_files()
    run_pyccoli()

