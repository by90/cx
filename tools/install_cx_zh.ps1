# This file installs the Chinese cx skills and refreshes the global Codex AGENTS.md file.
# It intentionally has no param block, so callers cannot change behavior with command-line arguments.

# Stop immediately when a command fails, which keeps a partial install from looking successful.
$ErrorActionPreference = "Stop"

# The cx repository is always read from the SSH remote used by this project.
$repositoryUrl = "git@github.com:by90/cx.git"
# The language package is fixed to Chinese for this installer.
$languageSubpath = "zh"
# The temporary clone always reads the repository default branch by name.
$mainBranch = "main"

# Use CODEX_HOME when the user has configured it.
if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
    # Store the configured Codex home path.
    $codexHome = $env:CODEX_HOME
}
else {
    # Fall back to the standard Codex home under the current Windows user profile.
    $codexHome = Join-Path -Path $env:USERPROFILE -ChildPath ".codex"
}

# Skills always live under the skills child directory of Codex home.
$skillsDirectory = Join-Path -Path $codexHome -ChildPath "skills"
# The global AGENTS.md file lives directly under Codex home.
$globalAgentsPath = Join-Path -Path $codexHome -ChildPath "AGENTS.md"
# A unique temporary directory keeps concurrent installs from colliding.
$temporaryRoot = Join-Path -Path ([System.IO.Path]::GetTempPath()) -ChildPath ("cx-install-" + [System.Guid]::NewGuid().ToString("N"))
# The source AGENTS.md path inside the temporary clone mirrors the repository package layout.
$sourceAgentsPath = Join-Path -Path $temporaryRoot -ChildPath "packages\zh\AGENTS.md"

# The try/finally block guarantees temporary files are removed after success or failure.
try {
    # Verify shskills is available before doing any filesystem work.
    Get-Command -Name "shskills" -ErrorAction Stop | Out-Null
    # Verify git is available because AGENTS.md is copied from a main-branch clone.
    Get-Command -Name "git" -ErrorAction Stop | Out-Null

    # Ensure Codex home exists before copying the global AGENTS.md file.
    New-Item -ItemType Directory -Force -Path $codexHome | Out-Null
    # Ensure the skills directory exists before shskills writes into it.
    New-Item -ItemType Directory -Force -Path $skillsDirectory | Out-Null

    # Install or update only the Chinese cx skills from the repository default main branch.
    & shskills install --url $repositoryUrl --agent custom --dest $skillsDirectory --subpath $languageSubpath --force --clean

    # Clone a shallow copy of main so AGENTS.md comes from the same source policy as the skills.
    & git clone --depth 1 --branch $mainBranch $repositoryUrl $temporaryRoot

    # Replace the global Codex AGENTS.md with the Chinese package template.
    Copy-Item -LiteralPath $sourceAgentsPath -Destination $globalAgentsPath -Force

    # Read the source hash so the final verification compares exact file bytes.
    $sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $sourceAgentsPath).Hash
    # Read the installed hash from the global Codex AGENTS.md file.
    $installedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $globalAgentsPath).Hash
    # Fail clearly if the copied file does not match the main-branch template.
    if ($sourceHash -ne $installedHash) {
        # Throwing here makes the install result visibly unsuccessful.
        throw "Global AGENTS.md hash does not match the Chinese cx package template."
    }

    # Tell the user which files were updated.
    Write-Host "Updated Chinese cx skills under $skillsDirectory"
    # Tell the user that global AGENTS.md was overwritten intentionally.
    Write-Host "Overwrote global AGENTS.md at $globalAgentsPath"
    # Remind the user that Codex needs a restart to load updated skill instructions.
    Write-Host "Restart Codex to pick up updated skills and AGENTS.md."
}
finally {
    # Remove the temporary clone when it exists.
    if (Test-Path -LiteralPath $temporaryRoot) {
        # Delete only the temporary directory created by this script.
        Remove-Item -LiteralPath $temporaryRoot -Recurse -Force
    }
}
