import json
import subprocess
import sys
import unittest

class CliContractTests(unittest.TestCase):
    def test_cli(self):
        cases=[(["--version"],0),([],2),(["--test"],2),(["--wat","1"],2),(["--test","t2-indep","--test","x"],2),(["oops"],2),(["--test","t2-indep","--mode","post-hoc","--tails","1","--d",".5","--alpha",".05","--n1","88","--n2","88"],0)]
        for args,status in cases:
            r=subprocess.run([sys.executable,"-m","gpower_clone",*args],capture_output=True,text=True)
            self.assertEqual(r.returncode,status,r.stdout+r.stderr)
            self.assertEqual(len(r.stdout.splitlines()),1)
            self.assertEqual(r.stderr,"")
            self.assertIsInstance(json.loads(r.stdout),dict)

if __name__ == "__main__": unittest.main()
