"""
╔══════════════════════════════════════════════════╗
║   TOPIC DIGITAL DIARY — PART 1 of 3             ║
║   Contributor: Collaborator 1                   ║
║   Role: App Foundation + UI Shell               ║
║                                                  ║
║   This file sets up:                            ║
║   - Main application window & theming           ║
║   - Sidebar with entry list                     ║
║   - Color palette & font constants              ║
║   - Entry point (run this file to launch app)   ║
╚══════════════════════════════════════════════════╝

  Dependencies: part2_editor.py, part3_search.py
  Run: python part1_app_shell.py
"""

import tkinter as tk
from tkinter import ttk, font
import os
import json
from datetime import datetime
import sys
import os
# Ensure the folder containing this file is always on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ─────────────────────────────────────────────────
#  THEME CONSTANTS  (shared across all 3 parts)
# ─────────────────────────────────────────────────
THEME = {
    "bg":          "#1A1A2E",   # deep navy background
    "sidebar":     "#16213E",   # sidebar panel
    "card":        "#0F3460",   # entry card
    "card_hover":  "#1B4F8A",   # hovered card
    "accent":      "#E94560",   # red-pink accent
    "accent2":     "#F5A623",   # warm gold
    "text":        "#E0E0E0",   # primary text
    "subtext":     "#8A8FA8",   # muted text
    "entry_bg":    "#0D1B36",   # editor background
    "border":      "#2A2D4E",   # subtle borders
    "success":     "#4CAF50",   # save confirm green
}

FONTS = {
    "title":    ("Georgia", 22, "bold"),
    "heading":  ("Georgia", 13, "bold"),
    "body":     ("Courier New", 12),
    "label":    ("Helvetica", 10),
    "small":    ("Helvetica", 9),
    "btn":      ("Helvetica", 10, "bold"),
}

DATA_FILE = "diary_entries.json"   # shared JSON store


# ─────────────────────────────────────────────────
#  DATA HELPERS  (used by all parts)
# ─────────────────────────────────────────────────
def load_entries():
    """Load all diary entries from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_entries(entries: dict):
    """Persist all diary entries to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────────
#  MAIN APPLICATION CLASS
# ─────────────────────────────────────────────────
class DiaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✦ Topic Digital Diary")
        self.geometry("1100x700")
        self.minsize(800, 550)
        self.configure(bg=THEME["bg"])
        self._center_window()

        # Shared state
        self.entries      = load_entries()
        self.selected_key = tk.StringVar(value="")
        self.status_msg   = tk.StringVar(value="Welcome to your diary ✦")

        self._build_layout()

    # ── Window helpers ──────────────────────────
    def _center_window(self):
        self.update_idletasks()
        w, h = 1100, 700
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ── Master layout ───────────────────────────
    def _build_layout(self):
        """Build the three-column layout: sidebar | editor | (search panel injected by Part 3)."""

        # ── Top header bar ──────────────────────
        header = tk.Frame(self, bg=THEME["sidebar"], height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(
            header, text="✦ My Diary",
            bg=THEME["sidebar"], fg=THEME["accent"],
            font=FONTS["title"]
        ).pack(side="left", padx=20, pady=10)

        # Date/time badge on right
        self.clock_label = tk.Label(
            header, text="",
            bg=THEME["sidebar"], fg=THEME["subtext"],
            font=FONTS["small"]
        )
        self.clock_label.pack(side="right", padx=20)
        self._tick_clock()

        # ── Main content frame ──────────────────
        content = tk.Frame(self, bg=THEME["bg"])
        content.pack(fill="both", expand=True)

        # ── Sidebar ─────────────────────────────
        self.sidebar = tk.Frame(content, bg=THEME["sidebar"], width=240)
        self.sidebar.pack(fill="y", side="left")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # ── Editor area (Part 2 will populate this) ──
        self.editor_frame = tk.Frame(content, bg=THEME["entry_bg"])
        self.editor_frame.pack(fill="both", expand=True, side="left")

        # ── Status bar ──────────────────────────
        status_bar = tk.Frame(self, bg=THEME["card"], height=28)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)
        tk.Label(
            status_bar, textvariable=self.status_msg,
            bg=THEME["card"], fg=THEME["subtext"],
            font=FONTS["small"]
        ).pack(side="left", padx=12, pady=4)

        # Inject Part 2 editor into editor_frame
        self._load_editor()

    # ── Sidebar ─────────────────────────────────
    def _build_sidebar(self):
        """Sidebar: new-entry button + scrollable entry list."""

        # "New Entry" button
        new_btn = tk.Button(
            self.sidebar,
            text="＋  New Entry",
            bg=THEME["accent"], fg="white",
            font=FONTS["btn"],
            relief="flat", cursor="hand2",
            activebackground="#c73550",
            activeforeground="white",
            pady=10,
            command=self._new_entry
        )
        new_btn.pack(fill="x", padx=12, pady=(14, 6))

        # Section label
        tk.Label(
            self.sidebar, text="ENTRIES",
            bg=THEME["sidebar"], fg=THEME["subtext"],
            font=FONTS["small"]
        ).pack(anchor="w", padx=16, pady=(10, 2))

        # Separator
        tk.Frame(self.sidebar, bg=THEME["border"], height=1).pack(fill="x", padx=12)

        # Scrollable list canvas
        list_container = tk.Frame(self.sidebar, bg=THEME["sidebar"])
        list_container.pack(fill="both", expand=True, pady=4)

        self.list_canvas = tk.Canvas(
            list_container, bg=THEME["sidebar"],
            highlightthickness=0, bd=0
        )
        scrollbar = tk.Scrollbar(list_container, orient="vertical",
                                  command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.list_canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(self.list_canvas, bg=THEME["sidebar"])
        self.list_canvas_window = self.list_canvas.create_window(
            (0, 0), window=self.list_frame, anchor="nw"
        )

        self.list_frame.bind("<Configure>", self._on_list_resize)
        self.list_canvas.bind("<Configure>", self._on_canvas_resize)
        self.list_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.refresh_sidebar()

    def _on_list_resize(self, event):
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.list_canvas.itemconfig(self.list_canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def refresh_sidebar(self):
        """Redraw the list of diary entries sorted by date (newest first)."""
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        sorted_keys = sorted(self.entries.keys(), reverse=True)

        if not sorted_keys:
            tk.Label(
                self.list_frame,
                text="No entries yet.\nClick '＋ New Entry'.",
                bg=THEME["sidebar"], fg=THEME["subtext"],
                font=FONTS["small"], justify="center"
            ).pack(pady=30)
            return

        for key in sorted_keys:
            entry  = self.entries[key]
            is_sel = (key == self.selected_key.get())
            self._make_entry_card(key, entry, is_sel)

    def _make_entry_card(self, key, entry, selected=False):
        """Render a single entry card in the sidebar."""
        card_bg = THEME["accent"] if selected else THEME["card"]
        card = tk.Frame(self.list_frame, bg=card_bg, cursor="hand2")
        card.pack(fill="x", padx=8, pady=3)

        # Topic / title
        title_text = entry.get("topic", "Untitled")[:28]
        tk.Label(
            card, text=title_text,
            bg=card_bg, fg=THEME["text"],
            font=FONTS["heading"], anchor="w"
        ).pack(fill="x", padx=10, pady=(7, 1))

        # Date sub-label
        tk.Label(
            card, text=key,
            bg=card_bg, fg=THEME["subtext"] if not selected else "#ffcdd2",
            font=FONTS["small"], anchor="w"
        ).pack(fill="x", padx=10, pady=(0, 7))

        # Hover effects
        for widget in (card, *card.winfo_children()):
            widget.bind("<Enter>",  lambda e, c=card: c.configure(bg=THEME["card_hover"]))
            widget.bind("<Leave>",  lambda e, c=card, s=selected:
                        c.configure(bg=THEME["accent"] if s else THEME["card"]))
            widget.bind("<Button-1>", lambda e, k=key: self._open_entry(k))

    # ── Entry actions ────────────────────────────
    def _new_entry(self):
        """Signal editor to open a blank new-entry form."""
        self.selected_key.set("")
        if hasattr(self, "editor"):
            self.editor.load_entry(key=None)
        self.refresh_sidebar()

    def _open_entry(self, key):
        """Load an existing entry into the editor."""
        self.selected_key.set(key)
        if hasattr(self, "editor"):
            self.editor.load_entry(key=key)
        self.refresh_sidebar()

    # ── Clock ────────────────────────────────────
    def _tick_clock(self):
        now = datetime.now().strftime("%A, %d %B %Y  •  %I:%M %p")
        self.clock_label.configure(text=now)
        self.after(30000, self._tick_clock)

    # ── Load Part 2 editor ───────────────────────
    def _load_editor(self):
        """
        Import and attach Part 2's DiaryEditor widget.
        If part2_editor.py is missing, show a placeholder.
        """
        try:
            from part2_editor import DiaryEditor
            self.editor = DiaryEditor(self.editor_frame, app=self)
            self.editor.pack(fill="both", expand=True)
        except ImportError:
            tk.Label(
                self.editor_frame,
                text="⚠  part2_editor.py not found.\nAdd Collaborator 2's file.",
                bg=THEME["entry_bg"], fg=THEME["accent"],
                font=FONTS["heading"]
            ).pack(expand=True)

        # ── Load Part 3 search & export panel ──
        try:
            from part3_search import attach_search_panel
            attach_search_panel(self)
        except ImportError:
            pass  # Part 3 not yet added — that's fine


# ─────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────
if __name__ == "__main__":
    app = DiaryApp()
    app.mainloop()
