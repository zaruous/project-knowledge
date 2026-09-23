param(
  [Parameter(Mandatory=$true)][string]$Name,
  [Parameter(Mandatory=$true)][string]$Code,
  [string]$Root = "."
)
$ConfigDir = Join-Path $Root "_config"
New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
$Content = @"
project:
  code: $Code
  name: $Name
  phase: proposal
  status: active
  owner: TBD
"@
Set-Content -Path (Join-Path $ConfigDir "project.yml") -Value $Content -Encoding UTF8
Write-Host "initialized: $ConfigDir/project.yml"
