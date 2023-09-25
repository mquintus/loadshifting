""" 
@author mstuebs@lbl.gov
"""
from threading import Thread
from threading import Lock
import sys
import time
class Dot_Progress_Bar: 
    i = None
    percent = None
    percent_float = None
    last_output_time = None
    number_of_rounds = None
    sparse = 1
    lock = None
    
    @classmethod
    def __init__(self, number_of_rounds=None, sparse=1, char='.'):
        if Dot_Progress_Bar.lock is None:
          Dot_Progress_Bar.lock = Lock()
        if number_of_rounds is None:
            Dot_Progress_Bar.lock.acquire()
            Dot_Progress_Bar.i += 1
            Dot_Progress_Bar.lock.release()
            if (Dot_Progress_Bar.i % Dot_Progress_Bar.sparse == 0):
                print(char, end='')
            if time.time() - Dot_Progress_Bar.last_output_time > 2:
                if Dot_Progress_Bar.i % Dot_Progress_Bar.percent == 0 and int(Dot_Progress_Bar.i / Dot_Progress_Bar.percent) > 0 and int(Dot_Progress_Bar.i / Dot_Progress_Bar.percent) % 10 == 0:
                    print(str(int(Dot_Progress_Bar.i / Dot_Progress_Bar.percent_float / 10) * 10) + '%')
                    Dot_Progress_Bar.last_output_time = time.time()
            if Dot_Progress_Bar.i == Dot_Progress_Bar.number_of_rounds:
                print('100%')
        else:
            Dot_Progress_Bar.sparse = sparse
            if number_of_rounds == 0:
                print('[ERROR] Progress bar for length of zero') 
            Dot_Progress_Bar.number_of_rounds = number_of_rounds
            Dot_Progress_Bar.last_output_time = time.time()
            Dot_Progress_Bar.i = 0
            Dot_Progress_Bar.percent = max(1, int(number_of_rounds / 100))
            Dot_Progress_Bar.percent_float = number_of_rounds / 100
            if Dot_Progress_Bar.percent_float == 0:
                Dot_Progress_Bar.percent_float = 0.001