#!/usr/bin/python

DOCUMENTATION = '''
---
module: file_grep
short_description: grep keywords from file
'''

EXAMPLES = '''
- name: check error in logfile
  file_grep:
    filename: /tmp/xxx.log
    regx: "error"
    tailnum: 10
    ingorecase: True
'''


from ansible.module_utils.basic import *
import os
import re

def find_keys(filename, regx, tailnum, ingorecase):
    is_error = False
    has_changed = False
    tailnum = int(tailnum)

    rr = re.compile(regx)

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            c = f.readlines()
            if len(c) < tailnum:
                sc = ''.join(c)
            else:
                sc = ''.join(c[-tailnum:])

            # ingore case
            w = []
            for line in sc:
                if ingorecase:
                    s = rr.findall(line, re.IGNORECASE)
                else:
                    s = rr.findall(line)

                if s:
                    w.append(''.join(s))

            print w

            # output
            if w:
                s = "find %s" %regx
                has_changed = True
                is_error = True
            else:
                s = "Not find %s" %regx

            result = { "data": s }

    else:
        result = { "data": "File not found!" }
        is_error = True

    return is_error, has_changed, result


def main():
    fields = {
        "filename": {"required": True, "type": "str"},
        "regx": {"required": True, "type": "str"},
        "tailnum": {"required": False, "default": 50, "type": "str"},
        "ignorecase": {"required": False, "default": False, "type": "bool"}
    }

    module = AnsibleModule(argument_spec=fields)
    filename = module.params["filename"]
    regx = module.params["regx"]
    tailnum = module.params["tailnum"]
    ignorecase = module.params["ignorecase"]

    is_error, has_changed, result = find_keys(filename, regx, tailnum, ignorecase)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg=result, meta=result)

if __name__ == '__main__':
    main()