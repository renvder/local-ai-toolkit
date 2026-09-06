# =====================================================================
#  llama.cpp One-Click Launcher  (Windows / PowerShell)
#  Auto-detect GPU → choose backend → calculate parameters → start router mode → open browser
#  Usage: Right-click → "Run with PowerShell", or double-click the accompanying start.bat
# =====================================================================

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$PORT_PREF  = 8080                 # Preferred port; will auto-increment if occupied
$MODELS_DIR = Join-Path $PSScriptRoot "models"
# Maximum tokens to generate per response.
# Must be significantly smaller than ctx-size, otherwise context fills up first
# and this limit never takes effect.
$MAX_PREDICT = 8192

# Deep thinking mode (for models like Qwen3 / DeepSeek-R1 that use <think>)
#   off  = Disable thinking, answer directly (default, simplest for beginners, least likely to go wild)
#   on   = Enable thinking
#   auto = Do not intervene, use the model's own default behavior
# Note: When thinking is enabled you must raise the generation limit,
#       otherwise all tokens are spent inside <think> and the actual answer
#       is cut off (appears as blank / half-sentence replies).
$THINKING = "off"

# YaRN long-context extrapolation: 0 = disabled (recommended).
# Only set a target length when you really need to stuff long documents,
# e.g. 65536 / 131072.
# Three important notes:
#   1) llama.cpp YaRN is applied globally at startup; short-conversation quality also degrades;
#   2) It only changes positional encoding — KV cache still grows linearly with context;
#   3) Some GGUFs already bake YaRN into their metadata (check startup log for rope scaling).
#      In that case do not set it again manually or you may cause problems.
$YARN_CTX      = 0
$YARN_ORIG_CTX = 32768             # Model's native context length (Qwen3 series = 32768)

function Say($msg, $color = "White") { Write-Host $msg -ForegroundColor $color }

Say ""
Say "  llama.cpp One-Click Launcher" Cyan
Say "  ---------------------------------------------" DarkGray

# ---------------------------------------------------------------------
# 1. Hardware detection
# ---------------------------------------------------------------------
$gpuName   = "No discrete GPU"
$vramGB    = 0
$vendor    = "cpu"

# NVIDIA: nvidia-smi is the most accurate
if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    try {
        $line = (& nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null | Select-Object -First 1)
        if ($line) {
            $parts   = $line -split ","
            $gpuName = $parts[0].Trim()
            $vramGB  = [math]::Round([double]$parts[1].Trim() / 1024, 1)
            $vendor  = "cuda"
        }
    } catch { }
}

# AMD / Intel: read VRAM from registry
# (Win32_VideoController.AdapterRAM overflows above 4 GB, so we cannot use it)
if ($vendor -eq "cpu") {
    $cards = Get-CimInstance Win32_VideoController |
             Where-Object { $_.Name -notmatch "Basic Display|Remote|Meta|Parsec|Virtual" }
    foreach ($c in $cards) {
        $n = $c.Name
        if ($n -match "Radeon|AMD|Intel\s+Arc|Intel\(R\)\s+Arc") {
            $gpuName = $n
            $vendor  = "vulkan"   # Vulkan is the most reliable backend for AMD / Intel on Windows
            break
        }
    }
    if ($vendor -eq "vulkan") {
        $key = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
        Get-ChildItem $key -ErrorAction SilentlyContinue | ForEach-Object {
            $sz = (Get-ItemProperty $_.PSPath -Name "HardwareInformation.qwMemorySize" -ErrorAction SilentlyContinue)."HardwareInformation.qwMemorySize"
            if ($sz -and ($sz / 1GB) -gt $vramGB) { $vramGB = [math]::Round($sz / 1GB, 1) }
        }
    }
}

$ramGB    = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
$cores    = (Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum
if (-not $cores) { $cores = [Environment]::ProcessorCount / 2 }
$threads  = [math]::Max(4, [math]::Min($cores, 16))   # Use physical cores, hard-cap at 16 (diminishing returns beyond)

Say ""
Say "  GPU      : $gpuName" White
Say "  VRAM     : $(if ($vramGB -gt 0) { "$vramGB GB" } else { "—" })" White
Say "  RAM      : $ramGB GB" White
Say "  Cores    : $cores" White

# ---------------------------------------------------------------------
# 2. Choose port
#    On Windows, 8080 is frequently inside Hyper-V / WSL reserved ranges
#    (visible via netsh). Binding then fails with an obscure error,
#    so we probe first and fall back.
# ---------------------------------------------------------------------
$reserved = @()
try {
    $out = & netsh int ipv4 show excludedportrange protocol=tcp 2>$null
    foreach ($l in $out) {
        if ($l -match "^\s*(\d+)\s+(\d+)\s*$") { $reserved += ,@([int]$Matches[1], [int]$Matches[2]) }
    }
} catch { }

function Test-PortFree($p) {
    foreach ($r in $reserved) { if ($p -ge $r[0] -and $p -le $r[1]) { return $false } }
    if (Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue) { return $false }
    return $true
}

$PORT = $null
foreach ($cand in @($PORT_PREF, 8090, 8081, 8188, 11434, 18080)) {
    if (Test-PortFree $cand) { $PORT = $cand; break }
}
if (-not $PORT) { $PORT = 18080 }
if ($PORT -ne $PORT_PREF) { Say ""; Say "  Port $PORT_PREF is occupied or system-reserved, using $PORT instead" Yellow }

# ---------------------------------------------------------------------
# 3. Locate llama-server
#    Multiple versions may exist in the folder (CPU / older builds).
#    Prefer paths containing cuda / vulkan, then take the newest by date.
# ---------------------------------------------------------------------
$cands = @(Get-ChildItem $PSScriptRoot -Recurse -Filter "llama-server.exe" -ErrorAction SilentlyContinue)
if ($cands.Count -gt 0) {
    $exe = ($cands | Sort-Object `
        @{ Expression = { if ($_.FullName -match "cuda|cu1\d|vulkan|hip") { 0 } else { 1 } } }, `
        @{ Expression = { $_.LastWriteTime }; Descending = $true } |
        Select-Object -First 1).FullName
} else {
    $exe = (Get-Command llama-server -ErrorAction SilentlyContinue).Source
}

if (-not $exe) {
    Say ""
    Say "  llama-server not found, installing via winget…" Yellow
    try {
        winget install llama.cpp --accept-package-agreements --accept-source-agreements
    } catch {
        Say "  winget failed, falling back to official install script llama.app…" Yellow
        Invoke-RestMethod https://llama.app/install.ps1 | Invoke-Expression
    }
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
    $exe = (Get-Command llama-server -ErrorAction SilentlyContinue).Source
}
if (-not $exe) {
    Say "  Installation failed. Please download manually from https://github.com/ggml-org/llama.cpp/releases and retry." Red
    Read-Host "  Press Enter to exit"; exit 1
}
Say ""
Say "  Executable : $exe" DarkGray

# ---------------------------------------------------------------------
# 4. Probe which flags the current version supports
#    (flag names change between versions; probe first to avoid immediate crash)
# ---------------------------------------------------------------------
$help = (& $exe --help 2>&1) -join "`n"
function Has($flag) { return $help -match [regex]::Escape($flag) }

if (-not (Has "--models-dir")) {
    Say ""
    Say "  Your llama.cpp version is too old and does not support router mode (hot model switching)." Red
    Say "  Please upgrade: winget upgrade llama.cpp" Yellow
    Read-Host "  Press Enter to exit"; exit 1
}

# Flash Attention: new syntax is -fa on/off/auto, old syntax is a pure flag
$faMode = "none"
if (Has "--flash-attn") {
    if ($help -match "flash-attn.*\[on\|off\|auto\]") { $faMode = "value" } else { $faMode = "flag" }
}

# ---------------------------------------------------------------------
# 5. Calculate parameters according to VRAM tier
#    Note: -ngl / layer offloading is left to llama.cpp's own --fit,
#    which measures free VRAM before loading and automatically drops layers
#    / offloads MoE experts to system RAM. Far more accurate than manual -ngl.
#    Here we only decide the strategy: context length and whether to quantize KV.
# ---------------------------------------------------------------------
if ($vramGB -ge 32)     { $ctx = 32768; $kvq = $false; $maxModels = 2; $tier = "32G+ (5090 / pro cards)" }
elseif ($vramGB -ge 24) { $ctx = 32768; $kvq = $true;  $maxModels = 1; $tier = "24G tier (4090 / 3090)" }
elseif ($vramGB -ge 16) { $ctx = 32768; $kvq = $true;  $maxModels = 1; $tier = "16G tier (4080 / 5070Ti / 7900XT)" }
elseif ($vramGB -ge 11) { $ctx = 16384; $kvq = $true;  $maxModels = 1; $tier = "12G tier (3060 12G / 4070)" }
elseif ($vramGB -ge 7)  { $ctx = 8192;  $kvq = $true;  $maxModels = 1; $tier = "8G tier (3060Ti / 4060)" }
elseif ($vramGB -ge 4)  { $ctx = 4096;  $kvq = $true;  $maxModels = 1; $tier = "6G and below (entry / laptop)" }
else                    { $ctx = 4096;  $kvq = $true;  $maxModels = 1; $tier = "Pure CPU mode (will be slow)" }

# Cap context if system RAM is low
if ($ramGB -lt 16 -and $ctx -gt 8192) { $ctx = 8192 }

# V-cache quantization requires Flash Attention; without it we only quantize K
$kvqV = $kvq -and ($faMode -ne "none")

# YaRN: if enabled, override the tier-calculated ctx with the target length
$yarnOn = $false
if ($YARN_CTX -gt $YARN_ORIG_CTX) {
    if (Has "--rope-scaling") {
        $yarnOn = $true
        $ctx    = $YARN_CTX
        $yarnScale = [math]::Round($YARN_CTX / $YARN_ORIG_CTX, 2)
        Say ""
        Say "  YaRN enabled: $YARN_ORIG_CTX → $YARN_CTX (scale $yarnScale)" Yellow
        Say "  KV cache will grow proportionally; if VRAM is insufficient a large amount will spill to RAM and speed will drop noticeably." Yellow
        Say "  Short-conversation quality is also affected. Set YARN_CTX back to 0 when you do not need long context." Yellow
    } else {
        Say ""
        Say "  This version does not support --rope-scaling; YaRN setting ignored." Yellow
    }
}

# Thinking mode interaction: raise generation limit when thinking is on so <think> has room
if ($THINKING -ne "off" -and $MAX_PREDICT -lt 16384) { $MAX_PREDICT = 16384 }

Say ""
Say "  Matched tier : $tier" Green
Say "  Backend      : $vendor" Green
Say "  Port         : $PORT" Green
Say "  Thinking     : $(switch ($THINKING) { 'off' { 'off (answer directly)' } 'on' { 'on' } default { 'follow model default' } })" Green
Say "  Max predict  : $MAX_PREDICT tokens" Green

# ---------------------------------------------------------------------
# 6. Models directory
# ---------------------------------------------------------------------
if (-not (Test-Path $MODELS_DIR)) { New-Item -ItemType Directory -Path $MODELS_DIR | Out-Null }
$ggufs = Get-ChildItem $MODELS_DIR -Recurse -Filter "*.gguf" -ErrorAction SilentlyContinue

Say ""
if ($ggufs.Count -eq 0) {
    Say "  models folder is empty." Yellow
    Say "  Recommended models for your VRAM (place them into the models folder):" Yellow
    if     ($vramGB -ge 24) { Say "    · Qwen3 32B Instruct  Q4_K_M   (~20 GB)" }
    elseif ($vramGB -ge 16) { Say "    · Qwen3 14B Instruct  Q4_K_M   (~9 GB)" }
    elseif ($vramGB -ge 11) { Say "    · Qwen3 14B Instruct  Q4_K_M   (~9 GB)" }
    elseif ($vramGB -ge 7)  { Say "    · Qwen3 8B Instruct   Q4_K_M   (~5 GB)" }
    else                    { Say "    · Qwen3 4B Instruct   Q4_K_M   (~2.5 GB)" }
    Say ""
    Say "  Multi-part GGUFs or multimodal models with mmproj should each go into their own sub-folder." DarkGray
    Say "  After placing the files, re-run this script." DarkGray
    Read-Host "  Press Enter to exit"; exit 0
}

Say "  Found $($ggufs.Count) model(s):" Green
$ggufs | Select-Object -First 8 | ForEach-Object {
    Say ("    · {0}  ({1} GB)" -f $_.Name, [math]::Round($_.Length / 1GB, 1)) DarkGray
}
if ($ggufs.Count -gt 8) { Say "    · …and $($ggufs.Count - 8) more" DarkGray }

# ---------------------------------------------------------------------
# 7. Read presets.ini – check which keys the user already defined under [*]
#    Keys that are already set in the preset will NOT be passed on the CLI
#    to avoid conflicts (previously -c 32768 would override a 16384 in the ini).
# ---------------------------------------------------------------------
$presets    = Join-Path $PSScriptRoot "presets.ini"
$presetKeys = @()
$usePresets = (Test-Path $presets) -and (Has "--models-preset")

if ($usePresets) {
    $inStar = $false
    foreach ($l in (Get-Content $presets -Encoding UTF8)) {
        $t = $l.Trim()
        if ($t -match '^\[(.+)\]$') { $inStar = ($Matches[1] -eq '*'); continue }
        if ($inStar -and $t -match '^([A-Za-z0-9\-_]+)\s*=') { $presetKeys += $Matches[1].ToLower() }
    }
    Say ""
    Say "  presets.ini loaded (used only for per-model overrides; common parameters still come from the command line)" Green
    Say "  Note: section names must be exact model names; [*] wildcards are NOT supported." DarkGray
    Say "  After start, check the log for 'Loaded N custom model presets'. N=0 means the format did not match." DarkGray
} elseif (Test-Path $presets) {
    Say ""
    Say "  presets.ini detected, but this version does not support --models-preset; ignored." Yellow
}

function NotInPreset($k) { return -not ($presetKeys -contains $k.ToLower()) }

# ---------------------------------------------------------------------
# 8. Assemble launch arguments
# ---------------------------------------------------------------------
$srvArgs = @(
    "--models-dir", $MODELS_DIR
    "--host", "127.0.0.1"
    "--port", "$PORT"
    "-t", "$threads"
)
if (Has "--ctx-shift") { $srvArgs += "--ctx-shift" }

if ($usePresets) { $srvArgs += @("--models-preset", $presets) }

# When YaRN is enabled the CLI must own the context size,
# otherwise a short ctx in the ini will conflict with the extrapolated rope.
# -c is always passed from the command line.
# Older versions skipped -c when presets.ini contained ctx-size, but llama-server
# is very strict about section names in custom preset files ([*] wildcards are ignored
# and the log will show "Loaded 0 custom model presets"). If the preset is not loaded
# neither side sets the value and the built-in default is used. Command line is the
# only reliable path.
$srvArgs += @("-c", "$ctx")
if ($yarnOn) {
    $srvArgs += @("--rope-scaling", "yarn", "--rope-scale", "$yarnScale")
    if (Has "--yarn-orig-ctx") { $srvArgs += @("--yarn-orig-ctx", "$YARN_ORIG_CTX") }
    Say "  Context    : $ctx tokens (YaRN extrapolated)" Green
} else {
    Say "  Context    : $ctx tokens" Green
}

if (Has "--models-max") { $srvArgs += @("--models-max", "$maxModels") }

# ★ Generation limit: llama-server defaults to --predict -1 (unlimited).
#   Once the model starts repeating it will fill the entire context and hang at 0 remaining.
#   We therefore impose a hard ceiling.
#   Note that the max-tokens setting in the web UI overrides this; set both.
if     (Has "--predict")   { $srvArgs += @("-n", "$MAX_PREDICT") }
elseif (Has "--n-predict") { $srvArgs += @("--n-predict", "$MAX_PREDICT") }

# Flash Attention (also required for V-cache quantization to take effect)
if     ($faMode -eq "value") { $srvArgs += @("-fa", "on") }
elseif ($faMode -eq "flag")  { $srvArgs += "-fa" }

# KV quantization
if ($kvq -and (Has "--cache-type-k")) {
    $srvArgs += @("--cache-type-k", "q8_0")
    if ($kvqV) { $srvArgs += @("--cache-type-v", "q8_0") }
}
Say "  KV cache   : $(if ($kvq) { if ($kvqV) { 'K+V q8_0 quantized' } else { 'K only q8_0 (no FA, V stays f16)' } } else { 'f16 full precision' })" Green

if (Has "--jinja") { $srvArgs += "--jinja" }          # Correctly apply the model's built-in chat template + tool calling

# Thinking-mode switch. Different llama.cpp versions implement it differently; probe in priority order:
#   1) --reasoning-budget 0   most direct (newer versions)
#   2) --chat-template-kwargs via template variable enable_thinking
# If neither is available the only way is to append /no_think in the chat itself.
if ($THINKING -eq "off") {
    if (Has "--reasoning-budget") {
        $srvArgs += @("--reasoning-budget", "0")
    } elseif (Has "--chat-template-kwargs") {
        $srvArgs += @("--chat-template-kwargs", '{"enable_thinking":false}')
    } else {
        Say "  This version cannot disable thinking from the server side; append /no_think to your prompts" Yellow
    }
} elseif ($THINKING -eq "on") {
    if (Has "--reasoning-budget") { $srvArgs += @("--reasoning-budget", "-1") }
    # Put thinking content into a separate field so the web UI can collapse it
    if (Has "--reasoning-format") { $srvArgs += @("--reasoning-format", "auto") }
}

# Sampling defaults: Qwen3 officially recommends two different sets for the two modes; do not mix them
if ($THINKING -eq "on") {
    $sTemp = "0.6"; $sTopP = "0.95"; $sPresence = "0.5"   # In thinking mode a high presence penalty causes Chinese/English mixing
} else {
    $sTemp = "0.7"; $sTopP = "0.8";  $sPresence = "1.0"   # Non-thinking mode; presence mainly suppresses repetition
}
if (Has "--temp")             { $srvArgs += @("--temp", $sTemp) }
if (Has "--top-p")            { $srvArgs += @("--top-p", $sTopP) }
if (Has "--top-k")            { $srvArgs += @("--top-k", "20") }
if (Has "--min-p")            { $srvArgs += @("--min-p", "0") }
if (Has "--presence-penalty") { $srvArgs += @("--presence-penalty", $sPresence) }

# VRAM allocation: prefer --fit auto-calculation; fall back to full offload if the version lacks it
if (Has "--fit-target") {
    $srvArgs += @("--fit-target", $(if ($vramGB -ge 16) { "2048" } else { "1024" }))
} elseif ($vendor -ne "cpu") {
    $srvArgs += @("-ngl", "99")
    Say "  VRAM alloc : this version has no --fit, fell back to -ngl 99 (full offload)" Yellow
}

if ($vendor -eq "cpu" -and (Has "--no-warmup")) { $srvArgs += "--no-warmup" }

Say ""
Say "  Launch command:" DarkGray
Say "  $exe $($srvArgs -join ' ')" DarkGray
Say ""
Say "  Starting… Browser will open automatically at http://127.0.0.1:$PORT" Cyan
Say "  You can switch models any time from the drop-down in the top-left of the web UI; no restart needed." Cyan
Say "  Tip: also set max tokens to $MAX_PREDICT in the web UI settings (top-right); do not leave it at -1." Yellow
Say "  Closing this black window stops the server." DarkGray
Say ""

# Probe the TCP port directly instead of /health —
# in router mode /health returns 503 while no model is loaded,
# which makes Invoke-WebRequest throw and the browser never opens.
Start-Job -ScriptBlock {
    param($p)
    for ($i = 0; $i -lt 90; $i++) {
        Start-Sleep -Seconds 1
        try {
            $c = New-Object Net.Sockets.TcpClient
            $c.Connect("127.0.0.1", $p)
            $c.Close()
            Start-Process "http://127.0.0.1:$p"
            break
        } catch { }
    }
} -ArgumentList $PORT | Out-Null

# -----------------------------------------------------------------
# Minimize this console window so only the browser is visible
# -----------------------------------------------------------------
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();
}
"@
$consolePtr = [Win32]::GetConsoleWindow()
if ($consolePtr -ne [IntPtr]::Zero) {
    [Win32]::ShowWindow($consolePtr, 6)   # 6 = SW_MINIMIZE
}

& $exe @srvArgs