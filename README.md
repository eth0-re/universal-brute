# Universal Brute
Universal brute forcing tool for when everything else fails.


## Others
* Medusa: https://github.com/jmk-foofus/medusa
* Hydra: https://github.com/vanhauser-thc/thc-hydra
* Crowbar: https://www.kali.org/tools/crowbar/

## Goal
To streamline the brute forcing of custom command line applications where credentials can be passed directly on the console.

## Help
```
usage: universal-brute.py [-h] [-u USERNAMES] [-U [USERNAME FILE]] [-p PASSWORDS] [-P [PASSWORD FILE]] [-t TARGETS] [-T [TARGETS FILE]] -c COMMAND_TEMPLATE [-f FAILURE_STRING] [-s SUCCESS_STRING] [-q]

Universal Brute Forcer, brute forcer of last resort

options:
  -h, --help           show this help message and exit
  -u USERNAMES         Individual or comma-separated list of usernames
  -U [USERNAME FILE]   Path to usernames file
  -p PASSWORDS         Individual or comma-separated list of usernames
  -P [PASSWORD FILE]   Path to passwords file
  -t TARGETS           Individual or comma-separated list of targets
  -T [TARGETS FILE]    Path to targets file
  -c COMMAND_TEMPLATE  The command to be executed. eg: 'mysql -h {TARGET} -u {USER} -p{PASS}'
  -f FAILURE_STRING    Output string of the command which signifies failure
  -s SUCCESS_STRING    Output string of the command which signifies success
  -q                   If set, suppress any failure messages and only show successes
```
 

## Examples
`./universal-brute.py -u root -P passwords.txt -t 192.168.105.74 -c 'mysql -u {USER} -p{PASS} -h {TARGET} -e \\"select @@version;\\"' -s Unknown -f denied`
#### Output:
```
[c] mysql -u root -ptest123 -h 192.168.1.1 -e \\"select @@version;\\"
[❌] |ERROR 1045 (28000): Access denied for user 'root'@'192.168.1.1' (using password: YES)
[c] mysql -u root -ptoor -h 192.168.1.1 -e \\"select @@version;\\"
[❌] |ERROR 1045 (28000): Access denied for user 'root'@'192.168.1.1' (using password: YES)
[c] mysql -u root -proot -h 192.168.1.1 -e \\"select @@version;\\"
[✅] |ERROR 1049 (42000): Unknown database '@@version;\\"'
```

## Todo
- [ ] Controllable threading
- [ ] Automatic pulling and caching wordlists from sources by alias similar to KiteRunner
- [ ] Reasonable performance when handling huge files (stream instead of trying to pull the whole thing into RAM)