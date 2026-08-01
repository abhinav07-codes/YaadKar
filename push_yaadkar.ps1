param(
    [string]$RepoUrl = "https://github.com/abhinav07-codes/YaadKar.git"
)

Write-Host "Preparing to push repository to $RepoUrl"

function Exec-Git([string]$args) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "git"
    $psi.Arguments = $args
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $p = [System.Diagnostics.Process]::Start($psi)
    $out = $p.StandardOutput.ReadToEnd()
    $err = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    return @{ ExitCode = $p.ExitCode; Out = $out; Err = $err }
}

$g = Exec-Git("--version")
if ($g.ExitCode -ne 0) {
    Write-Error "git not found. Please install Git and run this script again."
    exit 1
}

# init repo if missing
$isRepo = Exec-Git("rev-parse --is-inside-work-tree")
if ($isRepo.ExitCode -ne 0) {
    Write-Host "Initializing new git repository..."
    Exec-Git("init") | Out-Null
}

Write-Host "Configuring remote..."
if ($env:GITHUB_TOKEN) {
    $tokenRemote = $RepoUrl -replace 'https://', "https://$($env:GITHUB_TOKEN)@"
    Exec-Git("remote remove origin") | Out-Null 2>$null
    Exec-Git("remote add origin $tokenRemote") | Out-Null
    $usingToken = $true
} else {
    Exec-Git("remote remove origin") | Out-Null 2>$null
    Exec-Git("remote add origin $RepoUrl") | Out-Null
    $usingToken = $false
}

Write-Host "Staging changes..."
Exec-Git("add -A") | Out-Null

$commit = Exec-Git("commit -m ""Rename LearnLens to YaadKar; add .gitignore and update extension/docs""")
if ($commit.ExitCode -ne 0) {
    Write-Host "No new changes to commit or commit failed: $($commit.Err)"
} else {
    Write-Host "Committed changes."
}

Exec-Git("branch -M main") | Out-Null

Write-Host "Pushing to origin main (this may prompt for credentials if no token provided)..."
if ($usingToken) {
    $push = Exec-Git("push -u origin main")
} else {
    $push = Exec-Git("push -u origin main")
}

if ($push.ExitCode -ne 0) {
    Write-Error "Push failed: $($push.Err)"
    exit $push.ExitCode
}

Write-Host "Push successful. Repository is available at: $RepoUrl"
