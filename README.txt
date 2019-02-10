NAME: Alejandro Sanchez	

ATTACKER VM: Ubuntu 12.04 (In description field of VM is "ATTACKER VM")

PROGRAM EXECUTION:

To excecute replicator_worm.py:
$cd /tmp/
$python replicator_worm.py one two

To excecute extorter_worm.py:
$cd /tmp/
$python extorter_worm.py one two
**NOTE: The ransom note is called "I_have_your_files.txt" and will be located in the victim VM's /home/cpsc/Desktop directory. The Victim's encrpyted Documents folder will be located in /home/cpsc/ directory. The instructions to decrpyt it are included in the ransom note. Refer to the note below, AFTER WORM EXECTUTION, to undo anything the extorter_worm does.


To excecute passwordthief_worm.py:
$cd /tmp/
$python passwordthief_worm.py one two

**NOTE: The password info for each of the victims will be located in /tmp/ on the Attacker VM. I am aware the passwordthief_worm.py will be left on each victim machine and will contain the login info for the Attacker VM. In the interest of time, I did not take steps to prevent this information from being left on the victims computer. 


AFTER WORM EXECUTION:
To revert victim VM back to original state, run the following commands on each of the victim VMs:

$cd /tmp/
$./cure.sh

This should remove infected.txt and anything else the worm left behind.
