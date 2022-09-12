#!/usr/bin/python

import os
import sys
import time
import winsound

SFTP_HOSTNAME = "myserver.mydomain.com" # Or you can specify IP address
SFTP_PORT = 22
SFTP_USER = "tony" 
SFTP_PASSWORD_FILE = r"C:\Users\tony\password.txt"
SFTP_PASSWORD = open(SFTP_PASSWORD_FILE, "r").readlines()[0].strip()
#os.remove(SFTP_PASSWORD_FILE)

# This points to transfer directory on remote Linux server - make sure it is the same as the one you specified in your l-script.
SFTP_DIR = "/home/tony/.transfer/" 


LOCAL_TEMP  = os.getenv("TEMP")
PID_FILE = os.path.join(LOCAL_TEMP, "sd_watchdog_pid.txt")

# This try-catch block tries to kill the previous instance of watchdog - if any.
try:
    last_pid = open(PID_FILE, "r").readlines()[0].strip()
    last_pid = int(last_pid)
    os.system(f"taskkill /f /pid {last_pid}")
except:
    pass

# Store PID of our process.
my_pid = os.getpid()
os.system(f"echo {my_pid} > {PID_FILE}")

def getFiles(dirName):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(dirName) if isfile(join(dirName, f))]
    for  file in onlyfiles:
        os.system("move %s\\%s %s" % (SD, file, LOCAL_TEMP))
    return onlyfiles

def getFilesSftp():
    try:
        import pysftp
        import paramiko
    except ImportError:
        print("pysftp module not installed.")
        print("Install with:")
        print("python -m pip install pysftp")
        exit()
    global sftp
    MAX_ATTEMPTS = 2
    for attempt in range(MAX_ATTEMPTS):
        if attempt > 0:
            sftp =  pysftp.Connection(SFTP_HOSTNAME, username=SFTP_USER, password=SFTP_PASSWORD, port=SFTP_PORT)
            #sftp.cd(SFTP_DIR)
        try:
            files = sftp.listdir(SFTP_DIR)
            for fname in files:
                remotepath=f"{SFTP_DIR}/{fname}"
                sftp.get(
                    remotepath=remotepath,
                    localpath=os.path.join(LOCAL_TEMP, fname)
                )
                sftp.remove(remotefile=remotepath)
            return files
        except (IOError, paramiko.ssh_exception.SSHException, NameError):
            if attempt + 1 == MAX_ATTEMPTS:
                raise
            pass

def     processFile(name, local_temp=LOCAL_TEMP):
    full_name = os.path.join(local_temp, name)
    os.system("notepad++ %s\\%s" % (LOCAL_TEMP, name))
    winsound.MessageBeep(winsound.MB_ICONASTERISK)

getFilesFunc = getFilesSftp

while True:
    time.sleep(.1)
    try:
        for file in getFilesFunc():
            processFile(file)
    except KeyboardInterrupt:
        break
