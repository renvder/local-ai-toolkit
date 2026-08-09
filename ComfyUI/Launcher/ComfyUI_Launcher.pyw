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

# 高 DPI
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try: ctypes.windll.user32.SetProcessDPIAware()
    except: pass

def _get_root_dir():
    """
    判定 ComfyUI 根目录：
    - 若已被打包成 exe（如通过 PyInstaller build.bat 打包），使用 exe 所在目录；
    - 若仍以 .pyw 脚本方式运行，使用脚本所在目录。
    约定：启动器文件本身需要放在 ComfyUI 根目录下（与 run_nvidia_gpu.bat 同级）。
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

# 路径
COMFYUI_ROOT = _get_root_dir()
RUN_BAT      = os.path.join(COMFYUI_ROOT, "run_nvidia_gpu.bat")
UPDATE_BAT   = os.path.join(COMFYUI_ROOT, "update", "update_comfyui.bat")
NODES_DIR    = os.path.join(COMFYUI_ROOT, "ComfyUI", "custom_nodes")
PYTHON_EXE   = os.path.join(COMFYUI_ROOT, "python_embeded", "python.exe")
RUN_BAT_ADV  = os.path.join(COMFYUI_ROOT, "advanced", "run_nvidia_gpu_disable_api_nodes.bat")
COMFY_MAIN   = os.path.join(COMFYUI_ROOT, "ComfyUI", "main.py")

# 图标
_ICON_B64 = "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"

BG = "#0d1117"; PANEL = "#161b22"; BORDER = "#30363d"; ACCENT = "#58a6ff"; ACCENT2 = "#39c5bb"
GREEN = "#3fb950"; RED = "#f85149"; AMBER = "#f0b72f"; TEXT = "#c9d1d9"; TEXT_DIM = "#8b949e"
SANS = "Segoe UI"; MONO = "Consolas"

def _lighten(c, a=28):
    try:
        h = c.lstrip("#")
        return "#{:02x}{:02x}{:02x}".format(min(255, int(h[0:2], 16) + a), min(255, int(h[2:4], 16) + a), min(255, int(h[4:6], 16) + a))
    except:
        return c

class ComfyLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ComfyUI Launcher")
        self.geometry("1150x760")
        self.configure(bg=BG)
        self.resizable(True, True)

        self._comfy_proc = None
        self._log_lock = threading.Lock()
        self._auto_open_done = False

        self._set_icon()
        self._build_ui()
        self._check_paths()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

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
        tk.Label(hdr, text="⬡ ComfyUI", font=(SANS, 22, "bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text=" Launcher", font=(SANS, 22), fg=TEXT, bg=BG).pack(side="left")

        sf = tk.Frame(hdr, bg=BG)
        sf.pack(side="right")
        self._dot_lbl = tk.Label(sf, text="⬤", font=(SANS, 13), fg=TEXT_DIM, bg=BG)
        self._dot_lbl.pack(side="left")
        self._status_lbl = tk.Label(sf, text=" 未运行", font=(SANS, 10), fg=TEXT_DIM, bg=BG)
        self._status_lbl.pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 8))

        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(fill="x", padx=20, pady=(0, 8))

        self._btn_start = self._make_btn(btn_row, "▶  标准启动", ACCENT, self._start_comfy)
        self._btn_start.pack(side="left", padx=(0, 6))
        self._btn_start_adv = self._make_btn(btn_row, "▶  禁用 API 节点", "#6e40c9", self._start_comfy_adv)
        self._btn_start_adv.pack(side="left", padx=(0, 16))
        self._btn_stop = self._make_btn(btn_row, "■  停止", RED, self._stop_comfy, disabled=True)
        self._btn_stop.pack(side="left", padx=(0, 24))

        self._btn_upd_comfy = self._make_btn(btn_row, "↑  更新 ComfyUI", AMBER, self._update_comfyui)
        self._btn_upd_comfy.pack(side="left", padx=(0, 8))
        self._btn_upd_ext = self._make_btn(btn_row, "↑  更新所有扩展", AMBER, self._update_extensions)
        self._btn_upd_ext.pack(side="left", padx=(0, 8))
        self._btn_browser = self._make_btn(btn_row, "🌐  打开界面", ACCENT2, self._open_browser, disabled=True)
        self._btn_browser.pack(side="right")

        inst_frame = tk.Frame(self, bg=BG)
        inst_frame.pack(fill="x", padx=20, pady=(10, 0))
        tk.Label(inst_frame, text="安装扩展（Git 地址）", font=(SANS, 10, "bold"), fg=TEXT_DIM, bg=BG).pack(anchor="w")
        row2 = tk.Frame(inst_frame, bg=BG)
        row2.pack(fill="x", pady=(5, 0))
        eb = tk.Frame(row2, bg=BORDER, padx=1, pady=1)
        eb.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.repo_entry = tk.Entry(eb, font=(MONO, 10), bg=PANEL, fg=TEXT, insertbackground=ACCENT, relief="flat")
        self.repo_entry.pack(fill="x")
        self.repo_entry.bind("<FocusIn>", lambda e: eb.config(bg=ACCENT))
        self.repo_entry.bind("<FocusOut>", lambda e: eb.config(bg=BORDER))
        self.repo_entry.bind("<Return>", lambda e: self._install_extension())
        self._btn_install = self._make_btn(row2, "⬇  安装", GREEN, self._install_extension)
        self._btn_install.pack(side="right")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(12, 0))

        log_hdr = tk.Frame(self, bg=BG)
        log_hdr.pack(fill="x", padx=20, pady=(6, 4))
        tk.Label(log_hdr, text="OUTPUT LOG", font=(MONO, 9, "bold"), fg=TEXT_DIM, bg=BG).pack(side="left")
        self._btn_clear = self._make_btn(log_hdr, "清空", BORDER, self._clear_log)
        self._btn_clear.pack(side="right")

        log_wrap = tk.Frame(self, bg=BORDER)
        log_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        self._log_box = scrolledtext.ScrolledText(log_wrap, bg=PANEL, fg=TEXT, font=("Consolas", 10), bd=0, relief="flat", wrap="word", state="disabled", padx=12, pady=10)
        self._log_box.pack(fill="both", expand=True, padx=1, pady=1)

        for t, c in [("info", ACCENT2), ("success", GREEN), ("error", RED), ("warn", AMBER), ("dim", TEXT_DIM), ("normal", TEXT)]:
            self._log_box.tag_config(t, foreground=c)

    def _make_btn(self, p, t, c, cmd, disabled=False):
        b = tk.Label(p, text=t, font=(SANS, 10, "bold"), bg=c if not disabled else BORDER, fg="#fff" if not disabled else TEXT_DIM, padx=16, pady=9, cursor="hand2" if not disabled else "arrow")
        b._color = c
        b._disabled = disabled
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
        if r:
            self._dot_lbl.config(fg=GREEN)
            self._status_lbl.config(fg=GREEN, text=" 运行中")
        else:
            self._dot_lbl.config(fg=TEXT_DIM)
            self._status_lbl.config(fg=TEXT_DIM, text=" 未运行")

    def _check_paths(self):
        self._log("✦  ComfyUI Launcher 已就绪", "info")
        for label, path in [("启动脚本（标准）", RUN_BAT), ("启动脚本（禁用API）", RUN_BAT_ADV), ("更新脚本", UPDATE_BAT), ("custom_nodes", NODES_DIR), ("python_embeded", PYTHON_EXE)]:
            self._log(f"  {'✔' if os.path.exists(path) else '⚠'}  {label}", "success" if os.path.exists(path) else "warn")

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
        通过 netstat 查找当前监听指定端口的进程 PID。
        因为 bat 脚本用 start /b 异步拉起 python.exe，一旦 bat 自身的
        cmd.exe 退出（pause 遇到空 stdin 会立即跳过），我们手里的
        self._comfy_proc.pid 就和真正的 ComfyUI 进程脱钩了，
        所以判断"是否在运行"和"停止"都改为按端口查找真实进程。
        """
        try:
            out = subprocess.check_output(
                ["netstat", "-ano"],
                text=True, encoding="gbk", errors="replace",
                creationflags=subprocess.CREATE_NO_WINDOW
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
        # 强制子进程使用 UTF-8 输出（覆盖 Windows GBK 系统代码页）
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"          # Python 3.7+ UTF-8 模式
        env["PYTHONIOENCODING"] = "utf-8" # 兼容旧版
        return subprocess.Popen(
            args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    @staticmethod
    def _decode_line(raw: bytes) -> str:
        """
        子进程输出实际混合了两种编码来源：
        - ComfyUI/python.exe 自身输出：已通过 PYTHONUTF8/PYTHONIOENCODING 强制为 UTF-8；
        - cmd.exe 自身的提示/系统错误信息（如重定向不支持等）：使用系统代码页 GBK。
        因此优先按 UTF-8 解码，失败再退回 GBK，两者都失败才用 UTF-8+replace 兜底为 [?]。
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
            return self._log("已在运行（检测到 8188 端口已被占用）", "warn")
        if not os.path.exists(RUN_BAT):
            return self._log(f"找不到启动脚本：{RUN_BAT}", "error")
        self._auto_open_done = False
        self._log("▶  正在启动 ComfyUI …", "info")
        try:
            self._comfy_proc = self._start_process(
                ["cmd", "/c", RUN_BAT],
                os.path.dirname(RUN_BAT)
            )
            self._set_running(True)
            self._status_lbl.config(text=" 运行中")
            threading.Thread(target=self._stream_output, args=(self._comfy_proc,), daemon=True).start()
            threading.Thread(target=self._auto_open_browser_when_ready, daemon=True).start()
        except Exception as e:
            self._log(f"启动失败：{e}", "error")

    def _start_comfy_adv(self):
        if (self._comfy_proc and self._comfy_proc.poll() is None) or self._find_pid_on_port(8188):
            return self._log("已在运行（检测到 8188 端口已被占用）", "warn")
        if not os.path.exists(RUN_BAT_ADV):
            return self._log(f"找不到启动脚本：{RUN_BAT_ADV}", "error")
        self._auto_open_done = False
        self._log("▶  正在以禁用API节点模式启动 …", "info")
        try:
            self._comfy_proc = self._start_process(
                ["cmd", "/c", RUN_BAT_ADV],
                os.path.dirname(RUN_BAT_ADV)
            )
            self._set_running(True)
            self._status_lbl.config(text=" 运行中（禁用API）")
            threading.Thread(target=self._stream_output, args=(self._comfy_proc,), daemon=True).start()
            threading.Thread(target=self._auto_open_browser_when_ready, daemon=True).start()
        except Exception as e:
            self._log(f"启动失败：{e}", "error")

    # ANSI 转义码正则（过滤终端颜色控制字符）
    # ANSI 转义码过滤（终端颜色/控制字符）
    _ANSI_RE = re.compile(r'(?:\x1b|\033)\[[0-9;]*[A-Za-z]')

    @staticmethod
    def _sanitize(text):
        """
        去除 ANSI 转义码，并将非 BMP 字符（码点 > U+FFFF，即 4 字节 emoji）
        替换为 [?]，使 Consolas 字体能正常渲染所有内容。
        BMP 内的特殊字符（框线 ━ █、符号 ⭐ ✨ 等）Consolas 均可显示。
        """
        # 过滤 ANSI
        text = ComfyLauncher._ANSI_RE.sub('', text)
        # 替换非 BMP emoji（U+10000+）为 [?]
        return ''.join(c if ord(c) <= 0xFFFF else '[?]' for c in text)

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
                level = ("error"   if any(k in low for k in ("error", "traceback", "exception"))
                    else "warn"    if "warn" in low
                    else "success" if any(k in low for k in ("ready", "server", "loaded", "listening"))
                    else "normal")
                self.after(0, self._log, line, level)
        except Exception as e:
            self.after(0, self._log, f"日志读取异常：{e}", "error")
        finally:
            self.after(0, self._on_comfy_exit)

    def _auto_open_browser_when_ready(self):
        # 注意：run_nvidia_gpu.bat / run_nvidia_gpu_disable_api_nodes.bat
        # 自身检测到端口就绪后会用 explorer 打开浏览器，
        # 这里不再重复打开，避免出现两个浏览器窗口/标签页，仅做就绪提示。
        if self._wait_for_port_and_open():
            if not self._auto_open_done:
                self._auto_open_done = True
                self.after(0, self._log, "🌐  ComfyUI 已就绪（浏览器由启动脚本自动打开）", "info")
        else:
            self.after(0, self._log, "⚠  等待 ComfyUI 启动超时", "warn")

    def _on_comfy_exit(self):
        self._log("■  ComfyUI 进程已退出", "warn")
        self._set_running(False)
        self._status_lbl.config(text=" 未运行")
        self._auto_open_done = False

    def _stop_comfy(self):
        cmd_alive = self._comfy_proc and self._comfy_proc.poll() is None
        port_pid = self._find_pid_on_port(8188)
        if not cmd_alive and not port_pid:
            self._set_running(False)
            return
        if not messagebox.askyesno("确认停止", "ComfyUI 正在运行，确定要停止吗？\n\n此操作将中断 ComfyUI 的运行。"):
            return
        self._log("■  正在停止 ComfyUI …", "warn")
        # 先尝试杀掉我们直接持有的进程（bat 对应的 cmd.exe，如果还活着）
        if self._comfy_proc:
            try:
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(self._comfy_proc.pid)], creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
        # bat 用 start /b 异步拉起 python.exe，cmd.exe 退出后两者会脱钩，
        # 因此再按 8188 端口找到真正的 ComfyUI 进程杀掉，确保杀干净
        port_pid = self._find_pid_on_port(8188)
        if port_pid:
            try:
                subprocess.call(["taskkill", "/F", "/PID", str(port_pid)], creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
        self._set_running(False)
        self._log("■  已停止", "info")

    def _open_browser(self):
        webbrowser.open("http://127.0.0.1:8188")
        self._log("🌐  已打开界面", "info")

    def _update_comfyui(self):
        if not os.path.exists(UPDATE_BAT):
            return self._log("找不到更新脚本", "error")
        self._set_btn_disabled(self._btn_upd_comfy, True)
        self._log("↑  正在更新 ComfyUI …", "info")
        def _do():
            try:
                p = subprocess.Popen(
                    ["cmd", "/c", UPDATE_BAT, "noprompt"],
                    cwd=os.path.dirname(UPDATE_BAT),
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    text=True, encoding="gbk", errors="replace",
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                for l in iter(p.stdout.readline, ""):
                    if l.strip():
                        self.after(0, self._log, l.strip(), "error" if "error" in l.lower() else "normal")
                p.wait()
                self.after(0, self._log, "✔ 更新完成" if p.returncode == 0 else f"✘ 更新失败 {p.returncode}", "success" if p.returncode == 0 else "error")
            except Exception as e:
                self.after(0, self._log, f"更新出错：{e}", "error")
            finally:
                self.after(0, self._set_btn_disabled, self._btn_upd_comfy, False)
        threading.Thread(target=_do, daemon=True).start()

    def _update_extensions(self):
        if not os.path.isdir(NODES_DIR):
            return self._log("找不到 custom_nodes", "error")
        repos = [(n, os.path.join(NODES_DIR, n)) for n in sorted(os.listdir(NODES_DIR)) if os.path.isdir(os.path.join(NODES_DIR, n)) and os.path.isdir(os.path.join(NODES_DIR, n, ".git"))]
        if not repos:
            return self._log("未发现 git 扩展", "warn")

        self._set_btn_disabled(self._btn_upd_ext, True)
        self._set_btn_disabled(self._btn_upd_comfy, True)
        self._log(f"↑ 并行检查 {len(repos)} 个扩展…", "info")

        def _git(args, cwd):
            try:
                r = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
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
                        self.after(0, self._log, f"  ✔ {name} 已是最新", "dim")

            if outdated:
                self.after(0, self._log, f"↓ 开始更新 {len(outdated)} 个扩展…", "info")
                for name, path in outdated:
                    self.after(0, self._log, f"  → {name}", "dim")
                    code, _ = _git(["pull", "--ff-only"], path)
                    self.after(0, self._log, f"     {'✔' if code == 0 else '✘'} {name}", "success" if code == 0 else "error")
            else:
                self.after(0, self._log, "✔ 所有扩展已是最新版本", "success")

            self.after(0, self._set_btn_disabled, self._btn_upd_ext, False)
            self.after(0, self._set_btn_disabled, self._btn_upd_comfy, False)

        threading.Thread(target=_do, daemon=True).start()

    def _install_extension(self):
        url = self.repo_entry.get().strip()
        if not url:
            return self._log("请输入Git地址", "warn")
        name = url.rstrip("/").split("/")[-1].replace(".git", "")
        target = os.path.join(NODES_DIR, name)
        if os.path.exists(target):
            return self._log("目录已存在", "warn")
        self._set_btn_disabled(self._btn_install, True)
        self._log(f"⬇ 安装 {name} …", "info")
        def _do():
            try:
                p = subprocess.Popen(["git", "clone", "--progress", url, target], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW)
                for l in iter(p.stdout.readline, ""):
                    if l.strip():
                        self.after(0, self._log, f"   {l.strip()}", "dim")
                p.wait()
                if p.returncode == 0:
                    self.after(0, self._log, f"✔ 安装成功 {name}", "success")
                    req = os.path.join(target, "requirements.txt")
                    if os.path.exists(req):
                        self.after(0, lambda t=target: self._pip_install(t))
                else:
                    self.after(0, self._log, "✘ 安装失败", "error")
            except FileNotFoundError:
                self.after(0, self._log, "✘ 未找到 git", "error")
            except Exception as e:
                self.after(0, self._log, f"出错：{e}", "error")
            finally:
                self.after(0, self._set_btn_disabled, self._btn_install, False)
        threading.Thread(target=_do, daemon=True).start()

    def _pip_install(self, target):
        req = os.path.join(target, "requirements.txt")
        if not os.path.exists(PYTHON_EXE) or not os.path.exists(req):
            return
        def _do():
            try:
                p = subprocess.Popen([PYTHON_EXE, "-m", "pip", "install", "-r", req, "--quiet"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW)
                for l in iter(p.stdout.readline, ""):
                    if l.strip():
                        self.after(0, self._log, f"pip: {l.strip()}", "dim")
            except:
                pass
        threading.Thread(target=_do, daemon=True).start()

    def _on_close(self):
        if self._comfy_proc and self._comfy_proc.poll() is None:
            if not messagebox.askyesno("退出确认", "ComfyUI 正在运行，确定要停止并退出吗？\n\n此操作将中断 ComfyUI 的运行。"):
                return
            self._stop_comfy()
            time.sleep(0.5)
        self.destroy()

if __name__ == "__main__":
    ComfyLauncher().mainloop()
