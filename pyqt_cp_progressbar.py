"""MIT License
Copyright (c) 2017 Uka Osim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

__author__ = 'uosim'

from PyQt4 import QtGui, QtCore
import sys
import os
import shutil

# https://www.riverbankcomputing.com/software/pyqt/download
# https://wiki.qt.io/Signals_and_Slots_in_PySide
# Download working version of pyqt4 here for python27 - 34
# http://www.lfd.uci.edu/~gohlke/pythonlibs/ (has external non python libs bindings for python)

# This python program is used for copying directories from source to destination


# catching all qt(c++ error types )
def exception_handler(er_type, value, traceback):
    print 'Unhandled error:', er_type, value, traceback

sys.excepthook = exception_handler


class Window(QtGui.QWidget):

    """This python program is used for copying directories
    from 'f_src'(source) to 'f_dst'(destination) """
    progress = QtCore.pyqtSignal(int)  # setup a progress bar signal

    def __init__(self, f_src="", f_dst=""):
        super(Window, self).__init__()
        self.f_src = f_src
        self.f_dst = f_dst
        self._completed = 0
        self.setFixedSize(500, 300)  # automatically sets the Gui on the window centre screen
        self.setWindowTitle("Scarab Update")
        self.setWindowIcon(QtGui.QIcon())  # default icon value
        self.progressbar = QtGui.QProgressBar(self)
        self.progressbar.setGeometry(80, 100, 400, 25)
        self.progress.connect(self.get_value_set)
        self.thread = ProgressBar(func=[self.copy_dir])

    @QtCore.pyqtSlot(int)
    def copy_dir(self):
        file_count = Window.count_files(self.f_src)
        if file_count > 0:
            Window.make_dir(self.f_dst)
            # By default, the minimum step value is set to 0, and the maximum to 100, for the progressbar
            global num_copied
            num_copied = 0
        else:
            return
        for path, dirs, filenames in os.walk(self.f_src):
            dest_path = path.replace(self.f_src, self.f_dst)
            for d in dirs:
                # create all the directories
                dist_dir = dest_path + "/" + str(d)
                Window.make_dir(dist_dir)
            for fl in filenames:
                # when we have hidden files we skip them OS X ( .app files specifically)
                if fl.startswith("."):
                    num_copied += 1
                    continue
                src = path + "/" + str(fl)
                dst = path.replace(self.f_src, self.f_dst) + "/" + str(fl)
                try:
                    # copy from source to destination
                    shutil.copy2(src, dst)
                except IOError as e:
                    raise e
                except Exception as other_error:
                    raise other_error
                num_copied += 1
                self._completed = num_copied * 100 // file_count
                self.progress.emit(self._completed)
        self.close()
        return

    # running a QThread object
    def async(self):
        self.thread.start()

    # setting up a slot which retrieves the value returned from the signal.emit() in the copy_dir method
    @QtCore.pyqtSlot(int)
    def get_value_set(self, value):
        self.progressbar.setValue(value)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    # house keeping method which creates a directory
    @staticmethod
    def make_dir(path):
        # if the directory already exists we remove it and replace it with the new directory
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

    # house keeping method which counts all the files in a directory
    @staticmethod
    def count_files(directory):
        files = []
        if os.path.isdir(directory):
            for path, dirs, filenames, in os.walk(directory):
                files.extend(filenames)
        else:
            raise IOError("This is not a directory")
        return len(files)


class ProgressBar(QtCore.QThread):
    def __init__(self, func):
        QtCore.QThread.__init__(self)
        self.func = func

    def __del__(self):
        self.wait()

    def run(self):
        for f in self.func:
            print "in thread"
            f()
        print "finished all threads"


def main():
    app = QtGui.QApplication(sys.argv)
    try:
        source_fl = str(sys.argv[1])
        destination_fl = str(sys.argv[2])
        GUI = Window(f_src=source_fl, f_dst=destination_fl)
        # running the progress bar tread which updates the progress bar value
        GUI.async()
        # display the gui
        GUI.show()
    except Exception:
        raise
    finally:
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
