import re
import subprocess
import random
import sys
import os
import os.path

def reqadminwin():
	import ctypes, win32com.shell.shell, win32event, win32process
	outpath = r'%s\%s.out' % (os.environ["TEMP"], os.path.basename(__file__))
	if ctypes.windll.shell32.IsUserAnAdmin():
		if os.path.isfile(outpath):
			sys.stderr = sys.stdout = open(outpath, 'w', 0)
		return
	with open(outpath, 'w+', 0) as outfile:
		hProc = win32com.shell.shell.ShellExecuteEx(lpFile=sys.executable, \
			lpVerb='runas', lpParameters=' '.join(sys.argv), fMask=64, nShow=0)['hProcess']
		while True:
			hr = win32event.WaitForSingleObject(hProc, 40)
			while True:
				line = outfile.readline()
				if not line: break
				sys.stdout.write(line)
			if hr != 0x102: break
	os.remove(outpath)
	sys.stderr = ''
	sys.exit(win32process.GetExitCodeProcess(hProc))

	
def getcomname():
	res = subprocess.check_output(["systeminfo"], stderr=subprocess.STDOUT)
	res.decode('ascii')
	sm = re.search("(?<=Host Name:\\s)+(.*)", res)
	if hasattr(sm, "group") and sm.group(0) != None:
		return sm.group(0).strip()

reqadminwin()
print "getting computer name "
comname = getcomname()
newname = "PC-"+str(random.randrange(0000000000,9999999999))
print "changing computer name from \""+comname+"\" to \""+newname+"\""
print "running"
print "wmic computersystem where caption=\""+comname+"\" rename \""+newname+"\""
os.system("wmic computersystem where caption=\""+comname+"\" rename \""+newname+"\"")