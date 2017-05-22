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

import threading
import time


def main():

    main_thread = Test()
    main_thread.go()
    try:
        join_threads(main_thread.threads)
    except KeyboardInterrupt:
        print "\n KeyboardInterrupt catched."
        print "Terminate main thread."
        print "If only daemonic threads are left, terminate whole program."


class Test(object):
    def __init__(self):
        self.threads = []

    def __del__(self):
        del self.threads

    def func1(self):
        t_end = time.time() + 10  # make function run for 10 seconds
        while True:
            print "Func1 running...."
            time.sleep(2)
            if time.time() > t_end:
                break

    def func2(self):
        t_end = time.time() + 4  # make function run for 10 seconds
        while True:
            print "Func2 running...."
            time.sleep(2)
            if time.time() > t_end:
                break
        return

    def go(self):
        t1 = threading.Thread(target=self.func1)
        t2 = threading.Thread(target=self.func2)
        # Make threads daemonic, i.e. terminate them when main thread terminates
        t1.daemon = True
        t2.daemon = True
        t1.start()
        t2.start()
        self.threads.append(t1)
        self.threads.append(t2)


def join_threads(threads):
    for t in threads:
        t.join(5)  # the 5 is a time out in 5secs

if __name__ == "__main__":
    main()
