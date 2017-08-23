## larry ansible models
### 1. file_grep
    - name: check error in logfile
      file_grep:
        filename: /tmp/xxx.log
        regx: "error|lastchange"
        tailnum: 10
        ingorecase: True
