if "%1"=="h" goto begin
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
Connect2SchoolNet.exe --username ******* --password ******** --reconnect True --time 3600
