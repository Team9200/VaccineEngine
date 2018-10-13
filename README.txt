Linear Vaccine - Open Threat Intelligence Project's Test Anti-Virus (Based Kicom Anti-Virus, Clam Anti-Virus Database)


How to make malware database

1. open notepadfile

2. write like this format
[pe section raw size]/[md5 hash]/[file name]
ex) 101888/07ed91c78767712201f25c7092534608/Notepad

3. tool/sigtool/sigtool_md5.py [database]

4. move result file to engine/modules/sigdb



Thank's to Kicom Anti-Virus (http://www.kicomav.com/)
Thank's to Clam Anti-Virus (http://www.clanav.net/)