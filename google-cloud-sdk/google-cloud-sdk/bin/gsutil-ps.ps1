# Copyright 2013 Google Inc. All Rights Reserved.

# Override CLOUSDSDK_PYTHON_SITEPACKAGES for the current script only.
$cloudsdk_python_sitepackages = 1

# <cloud-sdk-ps1-preamble>
#
#  CLOUDSDK_ROOT_DIR            (a)  installation root dir
#  CLOUDSDK_PYTHON              (u)  python interpreter path
#  CLOUDSDK_GSUTIL_PYTHON       (u)  python interpreter path for gsutil
#  CLOUDSDK_PYTHON_ARGS         (u)  python interpreter arguments
#  CLOUDSDK_PYTHON_SITEPACKAGES (u)  use python site packages
#
# (a) always defined by the preamble
# (u) user definition overrides preamble


function Restore-Environment([System.Collections.DictionaryEntry[]] $origEnv) {
  # Remove any added variables.
  compare-object $origEnv $(get-childitem Env:) -property Key -passthru |
      where-object { $_.SideIndicator -eq "=>" } |
          foreach-object { remove-item -path ("Env:" + $_.Name); }
  # Revert any changed variables to original values.
  compare-object $origEnv $(get-childitem Env:) -property Value -passthru |
      where-object { $_.SideIndicator -eq "<=" } |
          foreach-object { set-item -path ("Env:" + $_.Name) -value $_.Value }
}

# Save the original environmental variables so we can restore them at the end.
$origEnv = get-childitem Env:

$current_dir = Split-Path $script:MyInvocation.MyCommand.Path
$cloudsdk_root_dir = (Resolve-Path (Join-Path $current_dir '..')).Path
$env:PATH = (Join-Path $cloudsdk_root_dir 'bin\sdk') + ';' + $env:PATH

if (-Not (Test-Path variable:cloudsdk_python)) {
  $cloudsdk_python = $env:CLOUDSDK_PYTHON
}
if (!$cloudsdk_python) {
  $bundled_python = Join-Path $cloudsdk_root_dir 'platform\bundledpython\python.exe'
  if (Test-Path $bundled_python) {
    $cloudsdk_python = $bundled_python
  }
}

function Find-Python {
  param ($BinName, $MinVersionTuple)
  $commands = (Get-Command $BinName -All -errorAction SilentlyContinue) | ForEach-Object Source
  foreach ($c in $commands) {
    if ($(& $c -c "import sys; vi = sys.version_info; print (vi >= $MinVersionTuple)") -eq 'True') {
      return $c
    }
  }
  return $null
}

# No Python yet? try python3 binary first
if (!$cloudsdk_python) {
  $cloudsdk_python = Find-Python -BinName python3 -MinVersionTuple "(3,5)"
}
# Then python binary with version >= 3.5
if (!$cloudsdk_python) {
  $cloudsdk_python = Find-Python -BinName python -MinVersionTuple "(3,5)"
}
# Then python binary with version >= 2.7.13
if (!$cloudsdk_python) {
  $cloudsdk_python = Find-Python -BinName python -MinVersionTuple "(2,7,13)"
}



if (-Not (Test-Path variable:cloudsdk_python_sitepackages)) {
  $cloudsdk_python_sitepackages = $env:CLOUDSDK_PYTHON_SITEPACKAGES
}
if (!$cloudsdk_python_sitepackages) {
  if (!(Test-Path env:\VIRTUAL_ENV)) {
    $cloudsdk_python_sitepackages = ''
  } else {
    $cloudsdk_python_sitepackages = 1
  }
}

if (-Not (Test-Path variable:cloudsdk_python_args)) {
  $cloudsdk_python_args = $env:CLOUDSDK_PYTHON_ARGS
}
if ($cloudsdk_python_args) {
  # Enclose with @() to ensure an array, even if pipeline returns 0 or 1 items.
  $args_array_no_s = @($cloudsdk_python_args.split(' ') | ? {$_ -cne '-S'})
} else {
  $args_array_no_s = @() # empty array
}
if (!$cloudsdk_python_sitepackages) {
  $cloudsdk_python_args_array = $args_array_no_s + '-S'
} else {
  $cloudsdk_python_args_array = $args_array_no_s
}
$cloudsdk_python_args = [string]::join(' ', $cloudsdk_python_args_array)

if (-Not (Test-Path variable:cloudsdk_gsutil_python)) {
  $cloudsdk_gsutil_python = $cloudsdk_python
}

$env:CLOUDSDK_ROOT_DIR = $cloudsdk_root_dir
$env:CLOUDSDK_PYTHON_ARGS = $cloudsdk_python_args
$env:CLOUDSDK_GSUTIL_PYTHON = $cloudsdk_gsutil_python

# </cloud-sdk-ps1-preamble>

# Powershell properly escapes arguments passed by array.
$run_args_array = $cloudsdk_python_args_array
$run_args_array += (Join-Path $cloudsdk_root_dir 'bin\bootstrapping\gsutil.py')
$run_args_array += $args

if ($MyInvocation.ExpectingInput) {
  $input | & "$cloudsdk_gsutil_python" $run_args_array
} else {
  & "$cloudsdk_gsutil_python" $run_args_array
}

Restore-Environment $origEnv

exit $LastExitCode
