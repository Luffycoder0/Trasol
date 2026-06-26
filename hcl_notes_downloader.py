import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import json
import win32com.client
import pythoncom
from datetime import datetime
from pathlib import Path

LANGUAGES = {
    "English": {
        "title": "HCL Notes Attachment Downloader",
        "start": "Start Download",
        "stop": "Stop",
        "browse": "Browse",
        "save_path": "Save Path:",
        "mark_read": "Mark emails as Read after download",
        "archive": "Move emails to Archive after download",
        "status_idle": "Idle — ready to scan.",
        "status_scanning": "Scanning last 100 unread emails…",
        "status_done": "Done.",
        "status_stopped": "Stopped by user.",
        "log_header": "Activity Log",
        "clear_log": "Clear Log",
        "language": "Language:",
        "emails_checked": "Emails checked:",
        "attachments_saved": "Attachments saved:",
        "skipped": "Skipped:",
        "no_path": "Please choose a save folder first.",
        "notes_error": "Could not connect to HCL Notes.\nMake sure Notes is running.",
        "folder_not_found": "Inbox not found in Notes.",
        "about_text": "HCL Notes Attachment Downloader\nPublisher: Djed Tech.ink\nVersion 2.2",
        "connected": "Connected to HCL Notes",
        "connecting": "Connecting to HCL Notes…",
    },
    "\u0627\u0644\u0639\u0631\u0628\u064a\u0629": {
        "title": "\u0623\u062f\u0627\u0629 \u062a\u062d\u0645\u064a\u0644 \u0645\u0631\u0641\u0642\u0627\u062a HCL Notes",
        "start": "\u0628\u062f\u0621 \u0627\u0644\u062a\u062d\u0645\u064a\u0644",
        "stop": "\u0625\u064a\u0642\u0627\u0641",
        "browse": "\u0627\u0633\u062a\u0639\u0631\u0627\u0636",
        "save_path": "\u0645\u0633\u0627\u0631 \u0627\u0644\u062d\u0641\u0638:",
        "mark_read": "\u062a\u0639\u0644\u064a\u0645 \u0627\u0644\u0631\u0633\u0627\u0626\u0644 \u0643\u0645\u0642\u0631\u0648\u0621\u0629 \u0628\u0639\u062f \u0627\u0644\u062a\u062d\u0645\u064a\u0644",
        "archive": "\u0646\u0642\u0644 \u0627\u0644\u0631\u0633\u0627\u0626\u0644 \u0625\u0644\u0649 \u0627\u0644\u0623\u0631\u0634\u064a\u0641 \u0628\u0639\u062f \u0627\u0644\u062a\u062d\u0645\u064a\u0644",
        "status_idle": "\u062c\u0627\u0647\u0632 \u2014 \u0641\u064a \u0627\u0646\u062a\u0638\u0627\u0631 \u0627\u0644\u0628\u062f\u0621.",
        "status_scanning": "\u062c\u0627\u0631\u064a \u0641\u062d\u0635 \u0622\u062e\u0631 100 \u0628\u0631\u064a\u062f \u063a\u064a\u0631 \u0645\u0642\u0631\u0648\u0621\u2026",
        "status_done": "\u0627\u0643\u062a\u0645\u0644.",
        "status_stopped": "\u062a\u0648\u0642\u0641 \u0628\u0623\u0645\u0631 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645.",
        "log_header": "\u0633\u062c\u0644 \u0627\u0644\u0646\u0634\u0627\u0637",
        "clear_log": "\u0645\u0633\u062d \u0627\u0644\u0633\u062c\u0644",
        "language": "\u0627\u0644\u0644\u063a\u0629:",
        "emails_checked": "\u0627\u0644\u0631\u0633\u0627\u0626\u0644 \u0627\u0644\u0645\u0641\u062d\u0648\u0635\u0629:",
        "attachments_saved": "\u0627\u0644\u0645\u0631\u0641\u0642\u0627\u062a \u0627\u0644\u0645\u062d\u0641\u0648\u0638\u0629:",
        "skipped": "\u0627\u0644\u0631\u0633\u0627\u0626\u0644 \u0627\u0644\u0645\u062a\u062c\u0627\u0648\u0632\u0629:",
        "no_path": "\u064a\u0631\u062c\u0649 \u0627\u062e\u062a\u064a\u0627\u0631 \u0645\u062c\u0644\u062f \u0627\u0644\u062d\u0641\u0638 \u0623\u0648\u0644\u0627\u064b.",
        "notes_error": "\u062a\u0639\u0630\u0631 \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u0640 HCL Notes.\n\u062a\u0623\u0643\u062f \u0645\u0646 \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0628\u0631\u0646\u0627\u0645\u062c.",
        "folder_not_found": "\u0644\u0645 \u064a\u064f\u0639\u062b\u0631 \u0639\u0644\u0649 \u0635\u0646\u062f\u0648\u0642 \u0627\u0644\u0648\u0627\u0631\u062f \u0641\u064a Notes.",
        "about_text": "\u0623\u062f\u0627\u0629 \u062a\u062d\u0645\u064a\u0644 \u0645\u0631\u0641\u0642\u0627\u062a HCL Notes\n\u0627\u0644\u0646\u0627\u0634\u0631: Djed Tech.ink\n\u0627\u0644\u0625\u0635\u062f\u0627\u0631 2.2",
        "connected": "\u0645\u062a\u0635\u0644 \u0628\u0640 HCL Notes",
        "connecting": "\u062c\u0627\u0631\u064a \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u0640 HCL Notes\u2026",
    },
}

SKIP_FROM = "\u0646\u0638\u0645 \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a"
SKIP_SUBJECT = "\u0631\u0641\u0636 \u0627\u0644\u0641\u0627\u0643\u0633"
MAX_EMAILS = 100

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "config.json")


def load_config():
    defaults = {"language": "English", "save_path": "", "mark_read": True, "archive": False}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            defaults.update(data)
        except Exception:
            pass
    return defaults


def save_config(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.lang_key = self.cfg.get("language", "English")
        self.L = LANGUAGES[self.lang_key]

        self.title(self.L["title"])
        self.resizable(False, False)
        self.configure(bg="#0f0f1a")

        self._set_icon()
        self._apply_font()
        self._build_ui()

        self.running = False
        self.worker_thread = None

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _set_icon(self):
        icon_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

    def _apply_font(self):
        is_arabic = self.lang_key == "\u0627\u0644\u0639\u0631\u0628\u064a\u0629"
        self.base_font = ("Tahoma", 10) if is_arabic else ("Segoe UI", 10)
        self.title_font = ("Tahoma", 14, "bold") if is_arabic else ("Segoe UI", 14, "bold")
        self.mono_font = ("Courier New", 9) if is_arabic else ("Consolas", 9)

    def _build_ui(self):
        PAD = 20
        BG = "#0f0f1a"
        CARD = "#16213e"
        CARD2 = "#1a1a2e"
        ACCENT = "#7c3aed"
        ACCENT_HOVER = "#5b21b6"
        FG = "#e2e8f0"
        FG2 = "#94a3b8"
        BORDER = "#2d2d4e"
        GREEN = "#22c55e"
        RED = "#ef4444"
        BLUE = "#60a5fa"

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background=BG)
        style.configure("Card.TFrame", background=CARD)
        style.configure("Card2.TFrame", background=CARD2)

        style.configure("TLabel", background=BG, foreground=FG, font=self.base_font)
        style.configure("Card.TLabel", background=CARD, foreground=FG, font=self.base_font)
        style.configure("Muted.TLabel", background=BG, foreground=FG2, font=self.base_font)
        style.configure("CardMuted.TLabel", background=CARD, foreground=FG2, font=self.base_font)
        style.configure("Title.TLabel", background=BG, foreground=FG, font=self.title_font)

        style.configure("Accent.TButton",
                        background=ACCENT, foreground="#ffffff",
                        font=(self.base_font[0], 10, "bold"),
                        borderwidth=0, focusthickness=0, padding=(20, 10))
        style.map("Accent.TButton",
                  background=[("active", ACCENT_HOVER), ("disabled", "#3a3a5c")],
                  foreground=[("disabled", "#6b6b8a")])

        style.configure("Danger.TButton",
                        background=RED, foreground="#ffffff",
                        font=(self.base_font[0], 10, "bold"),
                        borderwidth=0, focusthickness=0, padding=(20, 10))
        style.map("Danger.TButton",
                  background=[("active", "#b91c1c"), ("disabled", "#3a3a5c")],
                  foreground=[("disabled", "#6b6b8a")])

        style.configure("Ghost.TButton",
                        background=CARD2, foreground=FG2,
                        font=self.base_font, borderwidth=1,
                        relief="flat", padding=(10, 6))
        style.map("Ghost.TButton", background=[("active", BORDER)])

        style.configure("TEntry",
                        fieldbackground="#0d1117", foreground=FG,
                        insertcolor=FG, borderwidth=0, relief="flat",
                        padding=(8, 6))

        style.configure("TCheckbutton", background=CARD, foreground=FG, font=self.base_font)
        style.map("TCheckbutton",
                  background=[("active", CARD)],
                  indicatorcolor=[("selected", ACCENT), ("!selected", BORDER)])

        style.configure("TCombobox",
                        fieldbackground="#0d1117", background="#0d1117",
                        foreground=FG, selectbackground=ACCENT,
                        selectforeground="#fff", borderwidth=0, relief="flat")
        style.map("TCombobox", fieldbackground=[("readonly", "#0d1117")])

        style.configure("Horizontal.TProgressbar",
                        troughcolor=BORDER, background=ACCENT,
                        thickness=4, borderwidth=0)

        style.configure("TScrollbar",
                        background=BORDER, troughcolor=CARD2,
                        borderwidth=0, arrowsize=12)
        style.map("TScrollbar", background=[("active", ACCENT)])

        root_frame = ttk.Frame(self, style="TFrame", padding=(PAD, PAD))
        root_frame.grid(row=0, column=0, sticky="nsew")

        header_frame = ttk.Frame(root_frame, style="TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        dot1 = tk.Frame(header_frame, bg=ACCENT, width=4, height=30)
        dot1.pack(side="left", padx=(0, 10))

        title_lbl = ttk.Label(header_frame, text=self.L["title"], style="Title.TLabel")
        title_lbl.pack(side="left")

        publisher_lbl = tk.Label(header_frame, text="Djed Tech.ink",
                                 bg=BG, fg=FG2, font=(self.base_font[0], 8))
        publisher_lbl.pack(side="left", padx=(10, 0), pady=(4, 0))

        lang_frame = ttk.Frame(header_frame, style="TFrame")
        lang_frame.pack(side="right")
        ttk.Label(lang_frame, text=self.L["language"], style="Muted.TLabel").pack(side="left", padx=(0, 6))
        self.lang_var = tk.StringVar(value=self.lang_key)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                   values=list(LANGUAGES.keys()),
                                   width=10, state="readonly")
        lang_combo.pack(side="left")
        lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        sep = tk.Frame(root_frame, bg=BORDER, height=1)
        sep.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        left = ttk.Frame(root_frame, style="TFrame")
        left.grid(row=2, column=0, sticky="nsew", padx=(0, 16))
        left.columnconfigure(0, weight=1)

        def make_card(parent, row, pady=(0, 14)):
            outer = tk.Frame(parent, bg=BORDER, bd=0)
            outer.grid(row=row, column=0, sticky="ew", pady=pady, ipady=1, ipadx=1)
            inner = tk.Frame(outer, bg=CARD)
            inner.pack(fill="both", expand=True, padx=1, pady=1)
            content = tk.Frame(inner, bg=CARD, padx=16, pady=14)
            content.pack(fill="both", expand=True)
            return content

        path_card = make_card(left, 0)
        path_title = tk.Label(path_card, text=self.L["save_path"],
                              bg=CARD, fg=FG2, font=(self.base_font[0], 9))
        path_title.pack(anchor="w", pady=(0, 8))
        path_row = tk.Frame(path_card, bg=CARD)
        path_row.pack(fill="x")
        self.path_var = tk.StringVar(value=self.cfg.get("save_path", ""))
        path_entry_frame = tk.Frame(path_row, bg="#0d1117", bd=1,
                                    highlightthickness=1, highlightbackground=BORDER)
        path_entry_frame.pack(side="left", fill="x", expand=True)
        path_entry = tk.Entry(path_entry_frame, textvariable=self.path_var,
                              bg="#0d1117", fg=FG, insertbackground=FG,
                              relief="flat", font=self.base_font,
                              bd=6)
        path_entry.pack(fill="x")
        ttk.Button(path_row, text=self.L["browse"], style="Ghost.TButton",
                   command=self._browse).pack(side="right", padx=(8, 0))

        opts_card = make_card(left, 1)
        self.mark_read_var = tk.BooleanVar(value=self.cfg.get("mark_read", True))
        self.archive_var = tk.BooleanVar(value=self.cfg.get("archive", False))

        mr_cb = tk.Checkbutton(opts_card, text=self.L["mark_read"],
                                variable=self.mark_read_var,
                                bg=CARD, fg=FG, selectcolor=CARD2,
                                activebackground=CARD, activeforeground=FG,
                                font=self.base_font, bd=0,
                                highlightthickness=0)
        mr_cb.pack(anchor="w", pady=(0, 8))
        ar_cb = tk.Checkbutton(opts_card, text=self.L["archive"],
                                variable=self.archive_var,
                                bg=CARD, fg=FG, selectcolor=CARD2,
                                activebackground=CARD, activeforeground=FG,
                                font=self.base_font, bd=0,
                                highlightthickness=0)
        ar_cb.pack(anchor="w")

        stats_card = make_card(left, 2)
        self.stat_checked_var = tk.StringVar(value="0")
        self.stat_saved_var = tk.StringVar(value="0")
        self.stat_skipped_var = tk.StringVar(value="0")
        stats_data = [
            (self.L["emails_checked"], self.stat_checked_var, FG),
            (self.L["attachments_saved"], self.stat_saved_var, GREEN),
            (self.L["skipped"], self.stat_skipped_var, FG2),
        ]
        for lbl_text, var, color in stats_data:
            row = tk.Frame(stats_card, bg=CARD)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=lbl_text, bg=CARD, fg=FG2,
                     font=(self.base_font[0], 9)).pack(side="left")
            tk.Label(row, textvariable=var, bg=CARD, fg=color,
                     font=(self.base_font[0], 12, "bold")).pack(side="right")

        prog_frame = tk.Frame(left, bg=BG)
        prog_frame.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        self.progress = ttk.Progressbar(prog_frame, mode="indeterminate",
                                        style="Horizontal.TProgressbar")
        self.progress.pack(fill="x")

        btn_frame = tk.Frame(left, bg=BG)
        btn_frame.grid(row=4, column=0, sticky="w")
        self.start_btn = ttk.Button(btn_frame, text=self.L["start"],
                                    style="Accent.TButton", command=self._start)
        self.start_btn.pack(side="left", padx=(0, 10))
        self.stop_btn = ttk.Button(btn_frame, text=self.L["stop"],
                                   style="Danger.TButton", command=self._stop,
                                   state="disabled")
        self.stop_btn.pack(side="left")

        self.status_var = tk.StringVar(value=self.L["status_idle"])
        status_lbl = tk.Label(left, textvariable=self.status_var,
                               bg=BG, fg=FG2, font=(self.base_font[0], 9),
                               anchor="w")
        status_lbl.grid(row=5, column=0, sticky="ew", pady=(12, 0))

        right_frame = ttk.Frame(root_frame, style="TFrame")
        right_frame.grid(row=2, column=1, sticky="nsew")
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        log_hdr = tk.Frame(right_frame, bg=BG)
        log_hdr.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        tk.Label(log_hdr, text=self.L["log_header"],
                 bg=BG, fg=FG2, font=(self.base_font[0], 9)).pack(side="left")
        ttk.Button(log_hdr, text=self.L["clear_log"], style="Ghost.TButton",
                   command=self._clear_log).pack(side="right")

        log_outer = tk.Frame(right_frame, bg=BORDER, bd=0)
        log_outer.grid(row=1, column=0, sticky="nsew")
        log_inner = tk.Frame(log_outer, bg=CARD)
        log_inner.pack(fill="both", expand=True, padx=1, pady=1)

        self.log_text = tk.Text(log_inner, width=52, height=22,
                                bg=CARD, fg=FG,
                                font=self.mono_font,
                                insertbackground=FG, relief="flat",
                                state="disabled", wrap="word",
                                padx=12, pady=12)
        vsb = ttk.Scrollbar(log_inner, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.log_text.pack(side="left", fill="both", expand=True)

        self.log_text.tag_configure("ok", foreground=GREEN)
        self.log_text.tag_configure("err", foreground=RED)
        self.log_text.tag_configure("info", foreground=BLUE)
        self.log_text.tag_configure("muted", foreground=FG2)

        root_frame.columnconfigure(0, weight=0)
        root_frame.columnconfigure(1, weight=1)
        root_frame.rowconfigure(2, weight=1)

    def _on_lang_change(self, *_):
        new_lang = self.lang_var.get()
        if new_lang == self.lang_key:
            return
        self.cfg["language"] = new_lang
        save_config(self.cfg)
        messagebox.showinfo(
            "Language / \u0627\u0644\u0644\u063a\u0629",
            "Please restart the application to apply the language change.\n"
            "\u064a\u0631\u062c\u0649 \u0625\u0639\u0627\u062f\u0629 \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0628\u0631\u0646\u0627\u0645\u062c \u0644\u062a\u0637\u0628\u064a\u0642 \u0627\u0644\u0644\u063a\u0629."
        )

    def _browse(self):
        folder = filedialog.askdirectory(title="Select Save Folder")
        if folder:
            self.path_var.set(folder)

    def _log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}]  {msg}\n"
        self.log_text.configure(state="normal")
        self.log_text.insert("end", line, tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _start(self):
        save_path = self.path_var.get().strip()
        if not save_path:
            messagebox.showwarning("Warning", self.L["no_path"])
            return

        self.cfg["save_path"] = save_path
        self.cfg["mark_read"] = self.mark_read_var.get()
        self.cfg["archive"] = self.archive_var.get()
        save_config(self.cfg)

        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.start(10)
        self.status_var.set(self.L["status_scanning"])

        self.stat_checked_var.set("0")
        self.stat_saved_var.set("0")
        self.stat_skipped_var.set("0")

        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def _stop(self):
        self.running = False
        self.status_var.set(self.L["status_stopped"])

    def _worker(self):
        pythoncom.CoInitialize()
        try:
            self._do_download()
        except Exception as exc:
            self.after(0, lambda e=exc: self._log(f"Fatal error: {e}", "err"))
        finally:
            pythoncom.CoUninitialize()
            self.after(0, self._worker_done)

    def _worker_done(self):
        self.running = False
        self.progress.stop()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if self.status_var.get() != self.L["status_stopped"]:
            self.status_var.set(self.L["status_done"])

    def _do_download(self):
        save_path = self.path_var.get().strip()
        mark_read = self.mark_read_var.get()
        do_archive = self.archive_var.get()

        self.after(0, lambda: self._log(self.L["connecting"], "muted"))

        try:
            session = win32com.client.Dispatch("Lotus.NotesSession")
            session.InitializeUsingNotesUserName("", "")
        except Exception as e:
            self.after(0, lambda: self._log(self.L["notes_error"], "err"))
            self.after(0, lambda err=e: self._log(str(err), "err"))
            return

        self.after(0, lambda: self._log(self.L["connected"], "ok"))

        try:
            db = session.CurrentDatabase
        except Exception as e:
            self.after(0, lambda err=e: self._log(f"DB error: {err}", "err"))
            return

        if db is None:
            self.after(0, lambda: self._log("No current database found.", "err"))
            return

        try:
            inbox = db.GetFolderDocuments("($Inbox)")
        except Exception:
            try:
                inbox = db.Search('Form = "Memo"', None, 0)
            except Exception as e2:
                self.after(0, lambda: self._log(self.L["folder_not_found"], "err"))
                self.after(0, lambda err=e2: self._log(str(err), "err"))
                return

        total_docs = inbox.Count
        start_index = max(1, total_docs - MAX_EMAILS + 1)

        self.after(0, lambda: self._log(
            f"Inbox total: {total_docs}  |  Checking last {MAX_EMAILS}", "muted"))

        checked = 0
        saved = 0
        skipped = 0
        folder_index = 0

        for i in range(start_index, total_docs + 1):
            if not self.running:
                break

            try:
                doc = inbox.GetNthDocument(i)
            except Exception:
                continue
            if doc is None:
                continue

            try:
                unread_raw = doc.GetItemValue("$Unread")
                is_unread = bool(unread_raw and str(unread_raw[0]).strip() == "")
                if not is_unread:
                    continue
            except Exception:
                pass

            try:
                sender = ""
                subject = ""
                try:
                    sv = doc.GetItemValue("From")
                    sender = str(sv[0]) if sv else ""
                except Exception:
                    pass
                try:
                    subv = doc.GetItemValue("Subject")
                    subject = str(subv[0]) if subv else ""
                except Exception:
                    pass

                if SKIP_FROM in sender or SKIP_SUBJECT in subject:
                    skipped += 1
                    self.after(0, lambda s=skipped: self.stat_skipped_var.set(str(s)))
                    self.after(0, lambda snd=sender, sub=subject:
                               self._log(f"Skipped | From: {snd} | Subject: {sub}", "muted"))
                    continue

                attachments = []
                try:
                    attachments = doc.GetItemValue("$FILE") or []
                except Exception:
                    pass

                if not attachments:
                    checked += 1
                    self.after(0, lambda c=checked: self.stat_checked_var.set(str(c)))
                    continue

                folder_index += 1
                folder_name = str(folder_index)
                email_folder = os.path.join(save_path, folder_name)
                os.makedirs(email_folder, exist_ok=True)

                self.after(0, lambda fn=folder_name, sub=subject:
                           self._log(f"\U0001f4c1 {fn}: {sub}", "info"))

                for att_name in attachments:
                    if not self.running:
                        break
                    try:
                        eo = doc.GetAttachment(att_name)
                        if eo is None:
                            continue
                        out_path = os.path.join(email_folder, att_name)
                        eo.ExtractFile(out_path)
                        saved += 1
                        self.after(0, lambda s=saved: self.stat_saved_var.set(str(s)))
                        self.after(0, lambda n=att_name:
                                   self._log(f"  \u2713 {n}", "ok"))
                    except Exception as ae:
                        self.after(0, lambda n=att_name, e=ae:
                                   self._log(f"  \u2717 {n}: {e}", "err"))

                if mark_read:
                    try:
                        doc.MarkRead(True)
                    except Exception:
                        pass

                if do_archive:
                    try:
                        doc.PutInFolder("Archive Attachments")
                        doc.RemoveFromFolder("($Inbox)")
                    except Exception:
                        pass

                checked += 1
                self.after(0, lambda c=checked: self.stat_checked_var.set(str(c)))

            except Exception as outer_e:
                self.after(0, lambda e=outer_e: self._log(f"Error: {e}", "err"))

        self.after(0, lambda c=checked, s=saved, sk=skipped:
                   self._log(
                       f"\u2714 Done | Checked: {c} | Saved: {s} | Skipped: {sk}",
                       "ok"))

    def _on_close(self):
        self.cfg["save_path"] = self.path_var.get()
        self.cfg["mark_read"] = self.mark_read_var.get()
        self.cfg["archive"] = self.archive_var.get()
        save_config(self.cfg)
        if self.running:
            self.running = False
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
