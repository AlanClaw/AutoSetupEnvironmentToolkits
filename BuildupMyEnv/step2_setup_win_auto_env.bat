@rem get current folder
@SET CURDIR=%~dp0
@SET PKGDIR=%CURDIR%\Package\
@echo %CURDIR%

@if exist "C:\auto\robot" (@goto :end2)

@if /i "%PROCESSOR_ARCHITECTURE%%PROCESSOR_ARCHITEW6432%" == "x86" (@goto :x86) else (@goto :x64)

:x86
@echo :x86


@echo install python2.7
@msiexec /i "%PKGDIR%python-2.7.10.msi" /qr  ALLUSERS=1

@echo Install PyWin32
start "" "%PKGDIR%pywin32-219.win32-py2.7.exe"
"%PKGDIR%deployPyWin32.exe"

@echo install AutoIt library
cd "%PKGDIR%AutoItLibrary-1.1"
python setup.py install
cd %CURDIR%

@goto :OS

:x64
@echo :x64

@echo install python2.7
@msiexec /i "%PKGDIR%python-2.7.10.amd64.msi" /qr  ALLUSERS=1

@echo Install PyWin32
start "" "%PKGDIR%pywin32-219.win-amd64-py2.7.exe"
"%PKGDIR%deployPyWin32.exe"

@echo install AutoIt library
cd "%PKGDIR%AutoItLibrary-1.1_X64"
python setup.py install
cd %PKGDIR%

@goto :OS

:OS
ver | find "2003" > nul
if %ERRORLEVEL% == 0 goto ver_2003

ver | find "XP" > nul
if %ERRORLEVEL% == 0 goto ver_xp

goto :end1


:ver_2003
:ver_xp
@echo If mklink is not available, for example XP or Windows 2000, you can use Sysinternals Junctions as an alternative. "junction C:\sctm_run C:\auto\robot"
@copy "%PKGDIR%\Junction\junction.exe" "%systemroot%\System32"

:end1
@echo create folder...
@mkdir C:\auto\tools\firefox-profiles\default
@echo create folder finished...

:end2
cd %CURDIR%
"%CURDIR%CYBAutoEnvBuilder.py"
@echo Finish the automation environment installation...
@pause