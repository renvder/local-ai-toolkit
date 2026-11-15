import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import os
import ctypes
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import base64
import tempfile
import webbrowser
import re
import socket
import sys

# High DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

def _get_root_dir():
    """
    Determine ComfyUI root directory:
    - If packaged as exe (e.g. via PyInstaller build.bat), use the directory containing the exe;
    - If running as a .pyw script, use the directory containing the script.
    Convention: the launcher file itself must be placed in the ComfyUI root directory
    (same level as run_nvidia_gpu.bat).
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

# Paths
COMFYUI_ROOT = _get_root_dir()
RUN_BAT      = os.path.join(COMFYUI_ROOT, "run_nvidia_gpu.bat")
UPDATE_BAT   = os.path.join(COMFYUI_ROOT, "update", "update_comfyui.bat")
NODES_DIR    = os.path.join(COMFYUI_ROOT, "ComfyUI", "custom_nodes")
PYTHON_EXE   = os.path.join(COMFYUI_ROOT, "python_embeded", "python.exe")
RUN_BAT_ADV  = os.path.join(COMFYUI_ROOT, "advanced", "run_nvidia_gpu_disable_api_nodes.bat")
COMFY_MAIN   = os.path.join(COMFYUI_ROOT, "ComfyUI", "main.py")

# Icon
_ICON_B64 = "AAABAAEAAAAAAAEAIAD9DAAAFgAAAIlQTkcNChoKAAAADUlIRFIAAAEAAAABAAgGAAAAXHKoZgAAAAFvck5UAc+id5oAAAy3SURBVHja7Z3pV1XXGYf9xL/QJrVtTKqkNkZNUxsjhIqKS3CKE6KCQzTaiK0TQXGAilVDFCNRExUVFacYq0KsDBLrLIrgCKiIU20WIQ6JXV2a1u7efdfNWoaiHDzh3nP2+7xrPd8T2b9nv+e+++zTrBlFURRFURRFURRFURRFURRFURRFURRFURRFURRFURRFUZQ76kdtKoI8tPAQDOBbC0EkQ07Awz0UeagE8K2FcARhTtgbCni1hwceFIBvLVQ3UhBIwSGhry/sBByaWhCPSgEZBDD0hB0CLQVk4IfgE3pwkwwQwQ8cfEIPbpIBIiD4gAgQQWPDH0LwARHI3fUPEnwwXAQhSIBdH+SK4KD4boBdH+gGhHYD7PoA3+sG5EjgkfCz6wNIkgDhBxAqAcIPIFQChB9AqAQIP4BQCRB+AKESIPwAgiXgO+RTRPgBhEnAt/uH+w758IcEsCcBvZG2oPUHkEm1b0MNovUH4FGA1h+ARwFafwAeBWj9AegCaP0B6ALY/QHoAtj9AegC2P0B6AKaUgD6c0iV/FEAhHUBtP8AgrsA2n+AgKI772B2fwAeA9j9AXgM4Mc/AB4DaP8BeAyg/QfgMYD2H4DHAAQAgAAQAAC/A/ADIAC/A/ADIACPAbT/AAgAAQAgAAQgkF90LFUtO510PS90LEMACACeRNiAQjXrgyUqr3icKr/ZX9Xcj1B3VWdj0P8/ZVcGq/SsP6sug/MQAAKAZ9qWq9hJm9WhcyOMCntD3PlvuFqXO021DjuOABCA3B3/aEWsqODX5fS1QapN+DHOAnAGQA4/frlcpWSkq9pvu4oO/3eUVMWon716hrMAnAEwn5+0O69W/2UGwa/DjPQMHgNo/82m+SvnVO7h8QS+Hq5/E6l++uuzCAABmMuKbbMI+xPoNWoXAkAAZjJ1/keEvAFSly9EAAjAPNp2O6K++Fd3Qt4ASzelIAAEYB5bCycTcAus/HQmAkAA5s36Cbc1Fq2dhwAQgFlkZM8h3BZ5e3oWAkAABo392p9TV+70ItwWCe23FwEgAHPQYy2CbY1LtX28JyQRAAIwhoVr5hFui6zdmcRJQARgFscvDiPcFhkxNRsBIABz0G+46VdeCXfD3HrYRbUKOYkAEIA5xCdnEm6LFJWO5k4ABMDhH6noV6MRAAIw6pVf/XYb4bZGeHQ+AkAA5hA1IpdgW6T6dm/vtWgIAAEYQ1rmfMJtkaycaVwMigDM4lhlLOG2yKiEDQgAATD+kzr+Cw4tQQAIwBzemb2acFtk36lRfBsAARg2/iuYQrgtMmdpOgJAAObwbNvz6trdKMJtEb4OhACMInL4ZwSb8R8CkHv5Ryrhtoj+LJiQdYEAJNCp7+dc/NkIRieuRwAIwDk81+H0U332+tUeB9Wk1BXq8q3eBLsR478XQ08gAAQQGF7qXOwd1+lf7MuuRrNz+5n9Z0ZKWm8IwCmEvFmksnIS1Vf/6UIQA8hcMz8AggCcygsdy1Tm9hmc0HMI3WL2IAAE4B96jsxRFf/oR/Acgn7kMvTyTwTgNGInbVY19yMInoOYuXiJtHWIAALBxNSV6vZDWn4ncfOfPVTrsOMIAAE0Lf3e3sEPfQ4kadGHEtcjAvAnHaIOcB2XAympGuL9UhICQABNSs6heALnMP5+r4f3pKTQNYkA/PmjH4FzFvpRbMDY7ZLXJQLwFycuDSV0DqLmfncVM2Gr9HWJAPyBPlxC6JzD1Ts9VWRcLo+lCMA/LN+aTPAcwqdFE73vWxB+BOAX9MmyCzVvEr4Ao29Djpu0idAjAP8SNqCQAAaI619Hqc15U1X0+G3SjvgiAKcw64Mlrg2QfkEpv3is9zah91fPdzzvrVqgEhYsUyMTslXEkD3ez6ARcgQQUPaeHO3K8N+4F+m9R5CQIAAE8JS0fL3Utcd+fz9rDQFBAAjADsOnbHTt6bjmr5wjIAgAAdhhzY4kVwrgk8JJhAMBIAC747+LX/Z1pQDikzMJBwJAAHboPLDAtb/+t4s4QjgQAAKwQ/KSxa4Mf/GFYQQDASAAuxSVjnGlAPQ8nWAgAARgZ/zX6aRrx3/6olKCgQAQgA1GTM127/ivPeM/BIAAbLF2pzvHf1sLJxMKBIAApI7/xievJhQIAAHYGv8NKnDtiz8vdzlKKBAAArBDSka6a9+XJxAIAAHYHv+58+2/tEzGfwgAAYgd/0WN4I48BIAAbKEvomD8BwhAqACydk135/ivYAphQAAIQOr4753ZjP8QAAKwRXh0PuM/QABSBfCnD905/jtawfgPASAA23xe9pYrBaBv0iUICAABCB3/cfMvAkAANhmVsMG1V38z/kMACMDu+C9nmisFsCWf8R8CQABix3/c/Y8AEIDg8V+b8GOEAAEgAInjvyMVcQQAEIDU8d/8lWkEABCA3fHfrYcuHf/FMf4DBCBy/Hf96yg+nQ0IQOr4b3PeVBY/IAA7PNO2XFV91duVAhg3k/EfIABbdBmcx/gPEIBUAcxZ6tLxXznjP0AAttl3apQrBTBvBeM/QAC2aBXi3vFfj9jdLHxAAHZ4613Gf4AAxAogKyfRlQLYuCeBRQ8IQOr4b2xSFoseEIAdusa4d/z3q98dZ9EDApA4/iu+MIwFDwhA6vhv5/4JLHhAAHYIDi1x7fjv7I2B3tuLWPSAAISN//gREBCA4PHfd3z5oJtKWpShWr5eyuIHBNDY8d/lW71dLYDvHQr6JtJ7MKix+Ou/r+Z+hCq/2d9745K+vajzwAICiwAY/0lmx9/+oNp3P0xwEYD/SV22iBA6gGt3o9Qb/fcSXgTgX3IOxRNAh6BPYraLOEKAEYD/uFTbh/DxXgMCkCiA518rI3QOPNocNqCQECOApufnvzlD6BxISkY6IUYATc+zbc97dxxC5yzyiscRYgTgH0qqhhA6h1FSFUOIEYB/yMieQ+gcxpnrgwgxAvAP3WL2EDqHcfwirzgjAD+iv6hD8JzD+s8SCTEC8B/6JRp9rz7hcwb6xSZCjAD8youhJ1RR6RgC6ADCo/MJMQLwP/pijfjkTFV2NZogBvA4sH5DkxAjgIAS2m+vmpCS6X1ZaPmWZLVi2yzL7DoQr2q/7UqgnwL9ZWYCjABcz2+j9qtT1+gkGou+nYn1gwCMQF92wUlD6+h7GfX9jKwdBGAMJy4NJdwW0Tczs2YQgFEUlY4m3BbRv7ewZhCAMegPduo7+gi3NfT1bKwbBGAMkXG5BNsi1bcZ/yEAw1iw6j3CbXn8x/FfBGAYRyo4Xsz4DwGI5KXOxYwALXL7Ybj65Rt84RgBGMS4mWsIt0X2nxnJmkEAZrFpD68YW2Xu8oWsGQRgDvquwat3ehJui+hLWVg3CMAYesTuJtgWuXKnF+M/BGAW81akEW5u/0EAUjl8fjjhtsiYaetYMwjAHPQ4S4+1CLe18V/rMMZ/CMAgxiZlEW6LHDjL+A8BGEb2XxMIt9Xx30fvs2YQgFlUftGPcFukU999rBkEYA6tQk4SbIvoexJYMwiA+b9QRieuZ80gAAQg9eovfQU7awYBGIX+oAUBb/jiTz78gQCM5PnXylTtv/kewJNITFvGWkEA5qLbW4L+mFt/dk1njSAAs5mYupKw18O63GmqeftzrBFDBNDCQ5GHB/xj//9NwCVVMYT+ERavm8uPfoYJIMhDuIdq/rHr+SLQoAJ14x7XgV+q7aOG/nELa8I0AfAYYG0kePlWb5HBr7kf4f2gKp/5CggPfN15CwTggJOBH38y2xOI7iKCf/raIJWWOd97ISp//4BR7evOgxCAQ3iuw2kVN3mj9+WXVdtnqi35U1zDht3vPvYz6Ms2p6g5S9O9F6DqryHztxbS/iMAAASAAAAQAP/oABIFwFkAAMEC4CwAgMQRII8BAIJHgAgAQHD7jwAAEAA/BAJIff7nh0AAwc//PAYACG7/eQwAENz+8xgAILz95zEAQHD7z2MAgOD2n8cAAOHtP10AgODdny4AQPjuTxcAIHj3pwsAEL770wUACN796QIAhO/+dAEAgnf/Ol1AiIeDSADgBw3/QV+2gpo5uZAAgLDWn98DAAS3/vweACC89edRAIDwIwEAwo8EAMSHHwkACA8/EgAQHn4kACA8/EgAQHj4kQCA8PDXI4Ei34lBRACSgl/tW/vywl9HAi18x4bpBkDSrh/uW/syw083AOz61OO6AUQAJgafXR8RAMGnEAEQfOqpRFCJDIDgyxVBMDIABwW+0gfBd4AMEAL4O/DBPgi+A2RQnxDqgiDAasgrCbz7hVCXhgQBcqkb8mACL08QIBdCTlEURVEURVEURVEURVEURVEURVEURVEURVEURVEURVGUG+p/bhrZ+/OH2A0AAAAASUVORK5CYII="

BG = "#0d1117"; PANEL = "#161b22"; BORDER = "#30363d"; ACCENT = "#58a6ff"; ACCENT2 = "#39c5bb"
GREEN = "#3fb950"; RED = "#f85149"; AMBER = "#f0b72f"; TEXT = "#c9d1d9"; TEXT_DIM = "#8b949e"
SANS = "Segoe UI"; MONO = "Consolas"

# Bilingual UI strings: {"key": {"en": English, "zh": 正體中文}}
T = {
    "title_a": {"en": "⬡ ComfyUI", "zh": "⬡ ComfyUI"},
    "title_b": {"en": " Launcher", "zh": "啓動器"},
    "lang": {"en": "漢", "zh": "EN"},
    "st_not": {"en": " Not running", "zh": "未在運行"},
    "st_run": {"en": " Running", "zh": "運行中"},
    "st_run_adv": {"en": " Running (API disabled)", "zh": "運行中（禁用API）"},
    "btn_start": {"en": "▶  Start", "zh": "▶  標準啓動"},
    "btn_noapi": {"en": "▶  No API", "zh": "▶  禁用API啓動"},
    "btn_stop": {"en": "■  Stop", "zh": "■  停止"},
    "btn_upd_comfy": {"en": "↑  Update ComfyUI", "zh": "↑  更新 ComfyUI"},
    "btn_upd_ext": {"en": "↑  Update Extensions", "zh": "↑  更新擴展"},
    "btn_browser": {"en": "🌐  Open UI", "zh": "🌐  打開界面"},
    "btn_install": {"en": "⬇  Install", "zh": "⬇  安裝"},
    "btn_clear": {"en": "Clear", "zh": "清空"},
    "inst_label": {"en": "Install Extension (Git URL)", "zh": "安裝擴展（Git URL）"},
    "log_title": {"en": "OUTPUT LOG", "zh": "輸出日志"},
    "ready": {"en": "✦  ComfyUI Launcher is ready", "zh": "✦  ComfyUI 啓動器就緒"},
    "ls_std": {"en": "Launch script (standard)", "zh": "啓動脚本（標準）"},
    "ls_adv": {"en": "Launch script (disable API)", "zh": "啓動脚本（禁用API）"},
    "up_bat": {"en": "Update script", "zh": "更新脚本"},
    "cn_dir": {"en": "custom_nodes", "zh": "custom_nodes"},
    "py_dir": {"en": "python_embeded", "zh": "python_embeded"},
    "already_running": {"en": "Already running (port 8188 is in use)", "zh": "已在運行（端口 8188 已被占用）"},
    "not_found": {"en": "Launch script not found: {path}", "zh": "找不到啓動脚本：{path}"},
    "starting": {"en": "▶  Starting ComfyUI …", "zh": "▶  正在啓動 ComfyUI …"},
    "starting_adv": {"en": "▶  Starting with API nodes disabled …", "zh": "▶  啓動中（已禁用 API 節點）…"},
    "start_fail": {"en": "Failed to start: {e}", "zh": "啓動失敗：{e}"},
    "stream_err": {"en": "Log read error: {e}", "zh": "日志读取錯誤：{e}"},
    "ready_opened": {"en": "🌐  Port 8188 ready – launcher opened the browser", "zh": "🌐  端口 8188 就緒，啓動器已打開瀏覽器"},
    "ready_explorer": {"en": "🌐  Port 8188 ready – opened via explorer", "zh": "🌐  端口 8188 就緒，已通過系統浏览器打開"},
    "timeout": {"en": "⚠  Timed out waiting for ComfyUI to start", "zh": "⚠  等待 ComfyUI 啓動超時"},
    "attached": {"en": "⚠  Port 8188 in use – external ComfyUI detected, status set to Running", "zh": "⚠  端口 8188 已被占用——检测到外部运行的 ComfyUI，状态已设为运行中"},
    "exited": {"en": "■  ComfyUI process has exited", "zh": "■  ComfyUI 進程已退出"},
    "confirm_stop_title": {"en": "Confirm Stop", "zh": "確認停止"},
    "confirm_stop_text": {"en": "ComfyUI is running. Are you sure you want to stop it?\n\nThis will interrupt ComfyUI.", "zh": "ComfyUI 正在運行。確定要停止嗎？\n\n這將中斷 ComfyUI。"},
    "stopping": {"en": "■  Stopping ComfyUI …", "zh": "■  正在停止 ComfyUI …"},
    "stopped": {"en": "■  Stopped", "zh": "■  已停止"},
    "opened_ui": {"en": "🌐  Opened UI", "zh": "🌐  已打開界面"},
    "confirm_exit_title": {"en": "Confirm Exit", "zh": "確認退出"},
    "confirm_exit_text": {"en": "ComfyUI is running. Are you sure you want to stop it and exit?\n\nThis will interrupt ComfyUI.", "zh": "ComfyUI 正在運行。確定要停止并退出嗎？\n\n這將中斷 ComfyUI。"},
    "updating_comfy": {"en": "↑  Updating ComfyUI …", "zh": "↑  正在更新 ComfyUI …"},
    "upd_done": {"en": "✔ Update complete", "zh": "✔ 更新完成"},
    "upd_fail": {"en": "✘ Update failed {code}", "zh": "✘ 更新失敗 {code}"},
    "upd_err": {"en": "Update error: {e}", "zh": "更新出錯：{e}"},
    "upd_not": {"en": "Update script not found", "zh": "找不到更新脚本"},
    "no_nodes": {"en": "custom_nodes directory not found", "zh": "找不到 custom_nodes 目錄"},
    "no_git_ext": {"en": "No git extensions found", "zh": "未找到 Git 擴展"},
    "checking_ext": {"en": "↑ Checking {n} extensions in parallel…", "zh": "↑ 并發檢查 {n} 個擴展…"},
    "uptodate": {"en": "  ✔ {name} is up to date", "zh": "  ✔ {name} 已是最新"},
    "updating_ext": {"en": "↓ Updating {n} extension(s)…", "zh": "↓ 正在更新 {n} 個擴展…"},
    "ext_ok": {"en": "     ✔ {name}", "zh": "     ✔ {name}"},
    "ext_fail": {"en": "     ✘ {name}", "zh": "     ✘ {name}"},
    "all_uptodate": {"en": "✔ All extensions are up to date", "zh": "✔ 所有擴展均為最新"},
    "enter_url": {"en": "Please enter a Git URL", "zh": "請輸入 Git URL"},
    "dir_exists": {"en": "Directory already exists", "zh": "目錄已存在"},
    "installing": {"en": "⬇ Installing {name} …", "zh": "⬇ 正在安裝 {name} …"},
    "installed": {"en": "✔ Installed successfully: {name}", "zh": "✔ 安裝成功：{name}"},
    "install_failed": {"en": "✘ Install failed", "zh": "✘ 安裝失敗"},
    "git_missing": {"en": "✘ git not found", "zh": "✘ 未找到 git"},
    "err": {"en": "Error: {e}", "zh": "錯誤：{e}"},
}

def _lighten(c, a=28):
    try:
        h = c.lstrip("#")
        return "#{:02x}{:02x}{:02x}".format(
            min(255, int(h[0:2], 16) + a),
            min(255, int(h[2:4], 16) + a),
            min(255, int(h[4:6], 16) + a),
        )
    except:
        return c

def is_port_in_use(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.15)
    try:
        s.connect(("127.0.0.1", port))
        s.close()
        return True
    except Exception:
        s.close()
        return False

class ComfyLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ComfyUI Launcher")
        self.geometry("1280x760")
        self.minsize(1100, 640)
        self.configure(bg=BG)
        self.resizable(True, True)
        self.withdraw()

        self._comfy_proc = None
        self._log_lock = threading.Lock()
        self._auto_open_done = False
        self.lang = "zh"           # "zh" = 正體中文, "en" = English
        self._is_running = False
        self._is_adv = False
        self._text_btns = []

        self._set_icon()
        self._build_ui()
        self._check_paths()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        def _probe():
            if is_port_in_use(8188):
                self.after(0, lambda: (self._set_running(True),
                                       self._log(T["attached"][self.lang], "warn")))
        threading.Thread(target=_probe, daemon=True).start()
        self.deiconify()

    def _set_icon(self):
        try:
            raw = base64.b64decode(_ICON_B64)
            tmp = tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
            tmp.write(raw)
            tmp.close()
            self.iconbitmap(tmp.name)
            self.after(1000, lambda: os.unlink(tmp.name))
        except:
            pass

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(20, 12))
        self._hdr_a = tk.Label(hdr, text=T["title_a"][self.lang], font=(SANS, 22, "bold"), fg=ACCENT, bg=BG)
        self._hdr_a.pack(side="left")
        self._hdr_b = tk.Label(hdr, text=T["title_b"][self.lang], font=(SANS, 22), fg=TEXT, bg=BG)
        self._hdr_b.pack(side="left")

        sf = tk.Frame(hdr, bg=BG)
        sf.pack(side="right")
        self._dot_lbl = tk.Label(sf, text="⬤", font=(SANS, 13), fg=TEXT_DIM, bg=BG)
        self._dot_lbl.pack(side="left")
        self._status_lbl = tk.Label(sf, text=T["st_not"][self.lang], font=(SANS, 10), fg=TEXT_DIM, bg=BG)
        self._status_lbl.pack(side="left")
        self._btn_lang = self._make_btn(sf, T["lang"][self.lang], BORDER, self._toggle_lang, key="lang")
        self._btn_lang.pack(side="left", padx=(12, 0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 8))

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=20, pady=(0, 8))

        self._btn_start = self._make_btn(btn_row, T["btn_start"][self.lang], ACCENT, self._start_comfy, key="btn_start")
        self._btn_start.pack(side="left", padx=(0, 6))
        self._btn_start_adv = self._make_btn(btn_row, T["btn_noapi"][self.lang], "#6e40c9", self._start_comfy_adv, key="btn_noapi")
        self._btn_start_adv.pack(side="left", padx=(0, 12))
        self._btn_stop = self._make_btn(btn_row, T["btn_stop"][self.lang], RED, self._stop_comfy, disabled=True, key="btn_stop")
        self._btn_stop.pack(side="left", padx=(0, 16))

        self._btn_upd_comfy = self._make_btn(btn_row, T["btn_upd_comfy"][self.lang], AMBER, self._update_comfyui, key="btn_upd_comfy")
        self._btn_upd_comfy.pack(side="left", padx=(0, 6))
        self._btn_upd_ext = self._make_btn(btn_row, T["btn_upd_ext"][self.lang], AMBER, self._update_extensions, key="btn_upd_ext")
        self._btn_upd_ext.pack(side="left", padx=(0, 6))

        self._btn_browser = self._make_btn(btn_row, T["btn_browser"][self.lang], ACCENT2, self._open_browser, disabled=True, key="btn_browser")
        self._btn_browser.pack(side="right")

        inst_frame = tk.Frame(self, bg=BG)
        inst_frame.pack(fill="x", padx=20, pady=(10, 0))
        self._inst_lbl = tk.Label(inst_frame, text=T["inst_label"][self.lang], font=(SANS, 10, "bold"), fg=TEXT_DIM, bg=BG)
        self._inst_lbl.pack(anchor="w")
        row2 = tk.Frame(inst_frame, bg=BG)
        row2.pack(fill="x", pady=(5, 0))
        eb = tk.Frame(row2, bg=BORDER, padx=1, pady=1)
        eb.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.repo_entry = tk.Entry(eb, font=(MONO, 10), bg=PANEL, fg=TEXT, insertbackground=ACCENT, relief="flat")
        self.repo_entry.pack(fill="x")
        self.repo_entry.bind("<FocusIn>", lambda e: eb.config(bg=ACCENT))
        self.repo_entry.bind("<FocusOut>", lambda e: eb.config(bg=BORDER))
        self.repo_entry.bind("<Return>", lambda e: self._install_extension())
        self._btn_install = self._make_btn(row2, T["btn_install"][self.lang], GREEN, self._install_extension, key="btn_install")
        self._btn_install.pack(side="right")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(12, 0))

        log_hdr = tk.Frame(self, bg=BG)
        log_hdr.pack(fill="x", padx=20, pady=(6, 4))
        self._log_title = tk.Label(log_hdr, text=T["log_title"][self.lang], font=(MONO, 9, "bold"), fg=TEXT_DIM, bg=BG)
        self._log_title.pack(side="left")
        self._btn_clear = self._make_btn(log_hdr, T["btn_clear"][self.lang], BORDER, self._clear_log, key="btn_clear")
        self._btn_clear.pack(side="right")

        log_wrap = tk.Frame(self, bg=BORDER)
        log_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self._log_box = scrolledtext.ScrolledText(
            log_wrap, bg=PANEL, fg=TEXT, font=("Consolas", 10),
            bd=0, relief="flat", wrap="word", state="disabled", padx=12, pady=10
        )
        self._log_box.pack(fill="both", expand=True, padx=1, pady=1)

        for t, c in [("info", ACCENT2), ("success", GREEN), ("error", RED), ("warn", AMBER), ("dim", TEXT_DIM), ("normal", TEXT)]:
            self._log_box.tag_config(t, foreground=c)

    def _make_btn(self, p, t, c, cmd, disabled=False, key=None):
        b = tk.Label(
            p, text=t, font=(SANS, 10, "bold"),
            bg=c if not disabled else BORDER,
            fg="#fff" if not disabled else TEXT_DIM,
            padx=14, pady=8,
            cursor="hand2" if not disabled else "arrow",
        )
        b._color = c
        b._disabled = disabled
        b._key = key
        if key:
            self._text_btns.append((b, key))

        def click(e):
            if not b._disabled:
                cmd()

        def enter(e):
            if not b._disabled:
                b.config(bg=_lighten(b._color))

        def leave(e):
            if not b._disabled:
                b.config(bg=b._color)

        b.bind("<Button-1>", click)
        b.bind("<Enter>", enter)
        b.bind("<Leave>", leave)
        return b

    def _set_btn_disabled(self, btn, d):
        btn._disabled = d
        if d:
            btn.config(bg=BORDER, fg=TEXT_DIM, cursor="arrow")
        else:
            btn.config(bg=btn._color, fg="#ffffff", cursor="hand2")

    def _set_running(self, r):
        self._set_btn_disabled(self._btn_start, r)
        self._set_btn_disabled(self._btn_start_adv, r)
        self._set_btn_disabled(self._btn_stop, not r)
        self._set_btn_disabled(self._btn_browser, not r)
        self._is_running = r
        if not r:
            self._is_adv = False
        if r:
            self._dot_lbl.config(fg=GREEN)
            self._status_lbl.config(fg=GREEN, text=T["st_run_adv"][self.lang] if self._is_adv else T["st_run"][self.lang])
        else:
            self._dot_lbl.config(fg=TEXT_DIM)
            self._status_lbl.config(fg=TEXT_DIM, text=T["st_not"][self.lang])

    def _toggle_lang(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self._hdr_a.config(text=T["title_a"][self.lang])
        self._hdr_b.config(text=T["title_b"][self.lang])
        for b, k in self._text_btns:
            b.config(text=T[k][self.lang])
        self._inst_lbl.config(text=T["inst_label"][self.lang])
        self._log_title.config(text=T["log_title"][self.lang])
        if self._is_running:
            self._status_lbl.config(text=T["st_run_adv"][self.lang] if self._is_adv else T["st_run"][self.lang])
        else:
            self._status_lbl.config(text=T["st_not"][self.lang])

    def _check_paths(self):
        self._log(T["ready"][self.lang], "info")
        for key, path in [
            ("ls_std", RUN_BAT),
            ("ls_adv", RUN_BAT_ADV),
            ("up_bat", UPDATE_BAT),
            ("cn_dir", NODES_DIR),
            ("py_dir", PYTHON_EXE),
        ]:
            self._log(
                f"  {'✔' if os.path.exists(path) else '⚠'}  {T[key][self.lang]}",
                "success" if os.path.exists(path) else "warn",
            )

    def _log(self, msg, level="normal"):
        ts = datetime.now().strftime("%H:%M:%S")
        with self._log_lock:
            self._log_box.config(state="normal")
            self._log_box.insert("end", f"[{ts}]  ", "dim")
            self._log_box.insert("end", msg + "\n", level)
            self._log_box.config(state="disabled")
            self._log_box.see("end")

    def _clear_log(self):
        self._log_box.config(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.config(state="disabled")

    @staticmethod
    def _find_pid_on_port(port=8188):
        """
        Find the PID of the process currently listening on the given port via netstat.
        Because the bat script uses start /b to launch python.exe asynchronously,
        once the bat's own cmd.exe exits (pause skips when stdin is empty),
        self._comfy_proc.pid is no longer tied to the real ComfyUI process.
        Therefore both "is running" checks and "stop" use port-based lookup.
        """
        try:
            out = subprocess.check_output(
                ["netstat", "-ano"],
                text=True, encoding="gbk", errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            for line in out.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if parts and parts[-1].isdigit():
                        return int(parts[-1])
        except Exception:
            pass
        return None

    def _wait_for_port_and_open(self, host="127.0.0.1", port=8188, timeout=180):
        start = time.time()
        while time.time() - start < timeout:
            try:
                with socket.create_connection((host, port), timeout=1):
                    return True
            except:
                time.sleep(1)
        return False

    def _start_process(self, args, cwd):
        # Force child process to use UTF-8 output (override Windows GBK system code page)
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"           # Python 3.7+ UTF-8 mode
        env["PYTHONIOENCODING"] = "utf-8"  # Compatibility with older versions
        env["COMFY_LAUNCHER"] = "1"        # launch bat detects this and skips its own explorer step
        return subprocess.Popen(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

    @staticmethod
    def _decode_line(raw: bytes) -> str:
        """
        Child process output actually mixes two encoding sources:
        - ComfyUI/python.exe output: forced to UTF-8 via PYTHONUTF8/PYTHONIOENCODING;
        - cmd.exe own prompts/system error messages (e.g. redirect not supported): system code page GBK.
        Therefore try UTF-8 first, fall back to GBK, and finally UTF-8+replace as last resort.
        """
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return raw.decode("gbk")
            except UnicodeDecodeError:
                return raw.decode("utf-8", errors="replace")

    def _start_comfy(self):
        if (self._comfy_proc and self._comfy_proc.poll() is None) or self._find_pid_on_port(8188):
            return self._log(T["already_running"][self.lang], "warn")
        if not os.path.exists(RUN_BAT):
            return self._log(T["not_found"][self.lang].format(path=RUN_BAT), "error")
        self._auto_open_done = False
        self._is_adv = False
        self._log(T["starting"][self.lang], "info")
        try:
            self._comfy_proc = self._start_process(
                ["cmd", "/c", RUN_BAT],
                os.path.dirname(RUN_BAT),
            )
            self._set_running(True)
            threading.Thread(target=self._stream_output, args=(self._comfy_proc,), daemon=True).start()
            threading.Thread(target=self._auto_open_browser_when_ready, daemon=True).start()
        except Exception as e:
            self._log(T["start_fail"][self.lang].format(e=e), "error")

    def _start_comfy_adv(self):
        if (self._comfy_proc and self._comfy_proc.poll() is None) or self._find_pid_on_port(8188):
            return self._log(T["already_running"][self.lang], "warn")
        if not os.path.exists(RUN_BAT_ADV):
            return self._log(T["not_found"][self.lang].format(path=RUN_BAT_ADV), "error")
        self._auto_open_done = False
        self._is_adv = True
        self._log(T["starting_adv"][self.lang], "info")
        try:
            self._comfy_proc = self._start_process(
                ["cmd", "/c", RUN_BAT_ADV],
                os.path.dirname(RUN_BAT_ADV),
            )
            self._set_running(True)
            threading.Thread(target=self._stream_output, args=(self._comfy_proc,), daemon=True).start()
            threading.Thread(target=self._auto_open_browser_when_ready, daemon=True).start()
        except Exception as e:
            self._log(T["start_fail"][self.lang].format(e=e), "error")

    # ANSI escape sequence regex (filter terminal color/control characters)
    _ANSI_RE = re.compile(r"(?:\x1b|\033)\[[0-9;]*[A-Za-z]")

    @staticmethod
    def _sanitize(text):
        """
        Strip ANSI escape codes and replace non-BMP characters (code point > U+FFFF,
        i.e. 4-byte emoji) with [?], so Consolas can render everything cleanly.
        Special characters within the BMP (box-drawing ━ █, symbols ⭐ ✨, etc.)
        are displayable by Consolas.
        """
        text = ComfyLauncher._ANSI_RE.sub("", text)
        return "".join(c if ord(c) <= 0xFFFF else "[?]" for c in text)

    def _stream_output(self, proc):
        try:
            for raw in iter(proc.stdout.readline, b""):
                line = self._decode_line(raw).rstrip()
                if not line:
                    continue
                line = self._sanitize(line)
                if not line:
                    continue
                low = line.lower()
                level = (
                    "error" if any(k in low for k in ("error", "traceback", "exception"))
                    else "warn" if "warn" in low
                    else "success" if any(k in low for k in ("ready", "server", "loaded", "listening"))
                    else "normal"
                )
                self.after(0, self._log, line, level)
        except Exception as e:
            self.after(0, self._log, T["stream_err"][self.lang].format(e=e), "error")
        finally:
            self.after(0, self._on_comfy_exit)

    def _auto_open_browser_when_ready(self):
        # Open the browser from the launcher itself once port 8188 accepts
        # connections. Relying on the bat's own "explorer URL" step is not
        # reliable under the launcher (hidden console, redirected stdio): in
        # that mode the bat process is already gone before explorer's request
        # reaches the shell, so no browser tab is opened. The bats detect
        # COMFY_LAUNCHER=1 and skip their own explorer step, so there is no
        # duplicate tab; double-clicking a bat directly still opens the browser.
        if self._wait_for_port_and_open():
            if not self._auto_open_done:
                self._auto_open_done = True
                try:
                    webbrowser.open("http://127.0.0.1:8188")
                    self.after(0, self._log, T["ready_opened"][self.lang], "info")
                except Exception:
                    subprocess.call(["explorer", "http://127.0.0.1:8188"],
                                    creationflags=subprocess.CREATE_NO_WINDOW)
                    self.after(0, self._log, T["ready_explorer"][self.lang], "info")
        else:
            self.after(0, self._log, T["timeout"][self.lang], "warn")

    def _on_comfy_exit(self):
        self._log(T["exited"][self.lang], "warn")
        self._set_running(False)
        self._auto_open_done = False

    def _stop_comfy(self, confirm=True):
        cmd_alive = self._comfy_proc and self._comfy_proc.poll() is None
        port_pid = self._find_pid_on_port(8188)
        if not cmd_alive and not port_pid:
            self._set_running(False)
            return
        if confirm and not messagebox.askyesno(
            T["confirm_stop_title"][self.lang],
            T["confirm_stop_text"][self.lang],
        ):
            return
        self._log(T["stopping"][self.lang], "warn")
        # First try to kill the process we hold directly (bat's cmd.exe, if still alive)
        if self._comfy_proc:
            try:
                subprocess.call(
                    ["taskkill", "/F", "/T", "/PID", str(self._comfy_proc.pid)],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            except:
                pass
        # bat uses start /b to launch python.exe asynchronously; after cmd.exe exits
        # the two become detached, so also kill the real ComfyUI process found by port 8188
        port_pid = self._find_pid_on_port(8188)
        if port_pid:
            try:
                subprocess.call(
                    ["taskkill", "/F", "/PID", str(port_pid)],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            except:
                pass
        self._set_running(False)
        self._log(T["stopped"][self.lang], "info")

    def _open_browser(self):
        webbrowser.open("http://127.0.0.1:8188")
        self._log(T["opened_ui"][self.lang], "info")

    def _update_comfyui(self):
        if not os.path.exists(UPDATE_BAT):
            return self._log(T["upd_not"][self.lang], "error")
        self._set_btn_disabled(self._btn_upd_comfy, True)
        self._log(T["updating_comfy"][self.lang], "info")

        def _do():
            try:
                p = subprocess.Popen(
                    ["cmd", "/c", UPDATE_BAT, "noprompt"],
                    cwd=os.path.dirname(UPDATE_BAT),
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    text=True, encoding="gbk", errors="replace",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                for l in iter(p.stdout.readline, ""):
                    if l.strip():
                        self.after(
                            0, self._log, l.strip(),
                            "error" if "error" in l.lower() else "normal",
                        )
                p.wait()
                self.after(
                    0, self._log,
                    T["upd_done"][self.lang] if p.returncode == 0 else T["upd_fail"][self.lang].format(code=p.returncode),
                    "success" if p.returncode == 0 else "error",
                )
            except Exception as e:
                self.after(0, self._log, T["upd_err"][self.lang].format(e=e), "error")
            finally:
                self.after(0, self._set_btn_disabled, self._btn_upd_comfy, False)

        threading.Thread(target=_do, daemon=True).start()

    def _update_extensions(self):
        if not os.path.isdir(NODES_DIR):
            return self._log(T["no_nodes"][self.lang], "error")
        repos = [
            (n, os.path.join(NODES_DIR, n))
            for n in sorted(os.listdir(NODES_DIR))
            if os.path.isdir(os.path.join(NODES_DIR, n))
            and os.path.isdir(os.path.join(NODES_DIR, n, ".git"))
        ]
        if not repos:
            return self._log(T["no_git_ext"][self.lang], "warn")

        self._set_btn_disabled(self._btn_upd_ext, True)
        self._set_btn_disabled(self._btn_upd_comfy, True)
        self._log(T["checking_ext"][self.lang].format(n=len(repos)), "info")

        def _git(args, cwd):
            try:
                r = subprocess.run(
                    ["git"] + args, cwd=cwd, capture_output=True, text=True,
                    encoding="utf-8", timeout=20,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                return r.returncode, (r.stdout + r.stderr).strip()
            except:
                return -1, ""

        def _check(name, path):
            code, _ = _git(["fetch", "--quiet"], path)
            if code != 0:
                return name, path, False
            _, local = _git(["rev-parse", "HEAD"], path)
            _, remote = _git(["rev-parse", "FETCH_HEAD"], path)
            return name, path, (local.strip() != remote.strip())

        def _do():
            outdated = []
            with ThreadPoolExecutor(max_workers=8) as ex:
                futures = {ex.submit(_check, name, path): name for name, path in repos}
                for fut in as_completed(futures):
                    name, path, needs_update = fut.result()
                    if needs_update:
                        outdated.append((name, path))
                    else:
                        self.after(0, self._log, T["uptodate"][self.lang].format(name=name), "dim")

            if outdated:
                self.after(0, self._log, T["updating_ext"][self.lang].format(n=len(outdated)), "info")
                for name, path in outdated:
                    self.after(0, self._log, f"  → {name}", "dim")
                    code, _ = _git(["pull", "--ff-only"], path)
                    self.after(
                        0, self._log,
                        (T["ext_ok"] if code == 0 else T["ext_fail"])[self.lang].format(name=name),
                        "success" if code == 0 else "error",
                    )
            else:
                self.after(0, self._log, T["all_uptodate"][self.lang], "success")

            self.after(0, self._set_btn_disabled, self._btn_upd_ext, False)
            self.after(0, self._set_btn_disabled, self._btn_upd_comfy, False)

        threading.Thread(target=_do, daemon=True).start()

    def _install_extension(self):
        url = self.repo_entry.get().strip()
        if not url:
            return self._log(T["enter_url"][self.lang], "warn")
        name = url.rstrip("/").split("/")[-1].replace(".git", "")
        target = os.path.join(NODES_DIR, name)
        if os.path.exists(target):
            return self._log(T["dir_exists"][self.lang], "warn")
        self._set_btn_disabled(self._btn_install, True)
        self._log(T["installing"][self.lang].format(name=name), "info")

        def _do():
            try:
                p = subprocess.Popen(
                    ["git", "clone", "--progress", url, target],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                for l in iter(p.stdout.readline, ""):
                    if l.strip():
                        self.after(0, self._log, f"   {l.strip()}", "dim")
                p.wait()
                if p.returncode == 0:
                    self.after(0, self._log, T["installed"][self.lang].format(name=name), "success")
                    req = os.path.join(target, "requirements.txt")
                    if os.path.exists(req):
                        self.after(0, lambda t=target: self._pip_install(t))
                else:
                    self.after(0, self._log, T["install_failed"][self.lang], "error")
            except FileNotFoundError:
                self.after(0, self._log, T["git_missing"][self.lang], "error")
            except Exception as e:
                self.after(0, self._log, T["err"][self.lang].format(e=e), "error")
            finally:
                self.after(0, self._set_btn_disabled, self._btn_install, False)

        threading.Thread(target=_do, daemon=True).start()

    def _pip_install(self, target):
        req = os.path.join(target, "requirements.txt")
        if not os.path.exists(PYTHON_EXE) or not os.path.exists(req):
            return

        def _do():
            try:
                p = subprocess.Popen(
                    [PYTHON_EXE, "-m", "pip", "install", "-r", req, "--quiet"],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8",
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                for l in iter(p.stdout.readline, ""):
                    if l.strip():
                        self.after(0, self._log, f"pip: {l.strip()}", "dim")
            except:
                pass

        threading.Thread(target=_do, daemon=True).start()

    def _on_close(self):
        if self._is_running:
            if not messagebox.askyesno(
                T["confirm_exit_title"][self.lang],
                T["confirm_exit_text"][self.lang],
            ):
                return
            self._stop_comfy(confirm=False)
            time.sleep(0.5)
        self.destroy()

if __name__ == "__main__":
    ComfyLauncher().mainloop()
