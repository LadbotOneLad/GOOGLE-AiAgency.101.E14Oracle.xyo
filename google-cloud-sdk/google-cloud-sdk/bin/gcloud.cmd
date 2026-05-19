@rem                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               goto lastline
@rem The weird-looking comment above is to workaround a bug when updating from older gcloud releases; see b/317793973#comment6 for details.
@rem DO NOT EDIT ABOVE THIS LINE.

@echo off
rem Copyright 2013 Google Inc. All Rights Reserved.

SETLOCAL

rem <cloud-sdk-cmd-preamble>
rem
rem  CLOUDSDK_ROOT_DIR            (a)  installation root dir
rem  CLOUDSDK_PYTHON              (u)  python interpreter path
rem  CLOUDSDK_GSUTIL_PYTHON       (u)  python interpreter path for gsutil
rem  CLOUDSDK_PYTHON_ARGS         (u)  python interpreter arguments
rem  CLOUDSDK_PYTHON_SITEPACKAGES (u)  use python site packages
rem  CLOUDSDK_ENCODING            (u)  python io encoding for gcloud
rem
rem (a) always defined by the preamble
rem (u) user definition overrides preamble

rem This command lives in google-cloud-sdk\bin or google-cloud-sdk\ so it or its
rem parent directory is the root. Don't enable DelayedExpansion yet or we
rem destroy PATHs that have exclamation marks. Quotes needed to support
rem ampersands.
IF "%CLOUDSDK_ROOT_DIR%"=="" (
  rem If sourced in install.bat ROOT_DIR is already defined. This case handles
  rem setting the ROOT_DIR for every other usecase.
  SET "CLOUDSDK_ROOT_DIR=%~dp0.."
)
SET "PATH=%CLOUDSDK_ROOT_DIR%\bin\sdk;%PATH%"

rem %PYTHONHOME% can interfere with gcloud. Users should use
rem CLOUDSDK_PYTHON to configure which python gcloud uses.
SET PYTHONHOME=


SETLOCAL EnableDelayedExpansion

IF "!CLOUDSDK_PYTHON!"=="" (
  SET BUNDLED_PYTHON=!CLOUDSDK_ROOT_DIR!\platform\bundledpython\python.exe
  IF EXIST "!BUNDLED_PYTHON!" (
    SET CLOUDSDK_PYTHON=!BUNDLED_PYTHON!
  )
)

for %%X in (where.exe) do (set WHERE_FOUND=%%~$PATH:X)

IF defined WHERE_FOUND (
  IF "!CLOUDSDK_PYTHON!"=="" (
    where /q python
    IF NOT ERRORLEVEL 1 (
      FOR /F "tokens=* USEBACKQ" %%F IN (`where python`) DO (
      SET PYTHON_CANDIDATE_PATH=%%F
        "!PYTHON_CANDIDATE_PATH!" -c "import sys; print(sys.version)" > tmpfile
      set PYTHON_CANDIDATE_VERSION=
      set /p PYTHON_CANDIDATE_VERSION= < tmpfile
      del tmpfile
      IF "!PYTHON_CANDIDATE_VERSION:~0,1!"=="3" (
        SET CLOUDSDK_PYTHON=%%F
      SET CLOUDSDK_PYTHON_VERSION="!PYTHON_CANDIDATE_VERSION!"
      )
      )
    )
  )

  IF "!CLOUDSDK_PYTHON!"=="" (
    where /q python3
    IF NOT ERRORLEVEL 1 (
      FOR /F "tokens=* USEBACKQ" %%F IN (`where python3`) DO (
      SET PYTHON_CANDIDATE_PATH=%%F
        "!PYTHON_CANDIDATE_PATH!" -c "import sys; print(sys.version)" > tmpfile
      set PYTHON_CANDIDATE_VERSION=
      set /p PYTHON_CANDIDATE_VERSION= < tmpfile
      del tmpfile
      IF "!PYTHON_CANDIDATE_VERSION:~0,1!"=="3" (
        SET CLOUDSDK_PYTHON=%%F
      SET CLOUDSDK_PYTHON_VERSION="!PYTHON_CANDIDATE_VERSION!"
      )
      )
    )
  )

  IF "!CLOUDSDK_PYTHON!"=="" (
    where /q python
    IF NOT ERRORLEVEL 1 (
      FOR /F "tokens=* USEBACKQ" %%F IN (`where python`) DO (
      SET PYTHON_CANDIDATE_PATH=%%F
        "!PYTHON_CANDIDATE_PATH!" -c "import sys; print(sys.version)" > tmpfile
      set PYTHON_CANDIDATE_VERSION=
      set /p PYTHON_CANDIDATE_VERSION= < tmpfile
      del tmpfile
      IF "!PYTHON_CANDIDATE_VERSION:~0,1!"=="2" (
        SET CLOUDSDK_PYTHON=%%F
      SET CLOUDSDK_PYTHON_VERSION="!PYTHON_CANDIDATE_VERSION!"
      )
      )
    )
  )
)

IF "!CLOUDSDK_PYTHON!"=="" (
  SET CLOUDSDK_PYTHON="python.exe"
)


SET NO_WORKING_PYTHON_FOUND="false"
rem We run sys.version to ensure it's not the Windows Store python.exe
"!CLOUDSDK_PYTHON!" -c "import sys; print(sys.version)" >nul 2>&1
IF NOT %ERRORLEVEL%==0 (
  SET NO_WORKING_PYTHON_FOUND="true"
)

IF "%CLOUDSDK_PYTHON_SITEPACKAGES%" == "" (
  IF "!VIRTUAL_ENV!" == "" (
    SET CLOUDSDK_PYTHON_SITEPACKAGES=
  ) ELSE (
    SET CLOUDSDK_PYTHON_SITEPACKAGES=1
  )
)
SET CLOUDSDK_PYTHON_ARGS_NO_S=!CLOUDSDK_PYTHON_ARGS:-S=!
IF "%CLOUDSDK_PYTHON_SITEPACKAGES%" == "" (
  IF "!CLOUDSDK_PYTHON_ARGS!" == "" (
    SET CLOUDSDK_PYTHON_ARGS=-S
  ) ELSE (
    SET CLOUDSDK_PYTHON_ARGS=!CLOUDSDK_PYTHON_ARGS_NO_S! -S
  )
) ELSE IF "!CLOUDSDK_PYTHON_ARGS!" == "" (
  SET CLOUDSDK_PYTHON_ARGS=
) ELSE (
  SET CLOUDSDK_PYTHON_ARGS=!CLOUDSDK_PYTHON_ARGS_NO_S!
)

IF "%CLOUDSDK_GSUTIL_PYTHON%" == "" (
  SET CLOUDSDK_GSUTIL_PYTHON=!CLOUDSDK_PYTHON!
)

IF NOT "%CLOUDSDK_ENCODING%" == "" (
  SET PYTHONIOENCODING=!CLOUDSDK_ENCODING!
)

SETLOCAL DisableDelayedExpansion

rem </cloud-sdk-cmd-preamble>

IF %NO_WORKING_PYTHON_FOUND%=="true" (
  echo.
  echo To use the Google Cloud CLI, you must have Python installed and on your PATH.
  echo As an alternative, you may also set the CLOUDSDK_PYTHON environment variable
  echo to the location of your Python executable.
  "%COMSPEC%" /C exit 1
  goto lastline
)

rem Important: the call to Python and goto ending the batch script must take place in the same line/block in case the script updates itself (see b/317793973).
"%CLOUDSDK_PYTHON%" %CLOUDSDK_PYTHON_ARGS% "%CLOUDSDK_ROOT_DIR%\lib\gcloud.py" %* & goto lastline 2>NUL || "%COMSPEC%" /C exit 0

rem DO NOT EDIT BELOW THIS LINE.
:lastline
"%COMSPEC%" /C exit %ERRORLEVEL%
