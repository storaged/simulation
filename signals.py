import signal

signalled = False


def react_usr1(_signr, _stack):
    global signalled
    signalled = True

def react_usr2(_signr, _stack):
    emergency_save()


def setup():
    signal.signal(signal.SIGUSR1, react_usr1)
    signal.signal(signal.SIGUSR2, react_usr2)

def ef():
    pass

def setup_ignore():
    signal.signal(signal.SIGUSR1, ef)
    signal.signal(signal.SIGUSR2, ef)



def save_if_requested():
    global signalled
    if signalled:
	signalled = False
	from listeners import Listeners
	Listeners.flush_all()


def emergency_save():
    from listeners import Listeners
    Listeners.flush_all()



def get_run_name():
    from batchhelper import batchinfo
    import os
    import time
    name = time.asctime() + "-" + str(os.getpid())
    if(batchinfo.in_batch_run):
	name = "batch-run-" + str(batchinfo.batch_run_no) + "-" + name
    else:
	name = "single_run-" + name
    return name

