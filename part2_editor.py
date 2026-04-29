"""
╔══════════════════════════════════════════════════╗
║   TOPIC DIGITAL DIARY — PART 2 of 3             ║
║   Contributor: Collaborator 2                   ║
║   Role: Entry Editor + Save / Load Logic        ║
║                                                  ║
║   This file provides:                           ║
║   - Topic input field                           ║
║   - Rich text editor area (mood + body)         ║
║   - Save, Delete entry actions                  ║
║   - Auto-generates entry key (date + time)      ║
╚══════════════════════════════════════════════════╝

  Import: from part2_editor import DiaryEditor
  Used by: part1_app_shell.py  (do NOT run standalone)
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# Re-use shared constants from Part 1
from part1_app_shell import THEME, FONTS, load_entries, save_entries

MOODS = ["😊 Happy", "😔 Sad", "😤 Frustrated", "😌 Calm", "🤩 Excited",
         "😰 Anxious", "😴 Tired", "🥰 Grateful", "😐 Neutral", "💪 Motivated"]


class DiaryEditor(tk.Frame):
    """
    The main writing area of the diary.
    Embedded into DiaryApp.editor_frame by Part 1.
    """

    def __init__(self, parent, app):
        super().__init__(parent, bg=THEME["entry_bg"])
        self.app = app          # reference back to DiaryApp
        self.current_key = None # key of the entry being edited ("" = new)

        self._build_editor()
        self.load_entry(key=None)  # start with a blank entry

    # ─────────────────────────────────────────────
    #  BUILD UI
    # ─────────────────────────────────────────────
    def _build_editor(self):
        # ── Top toolbar ──────────────────────────
        toolbar = tk.Frame(self, bg=THEME["sidebar"], pady=8)
        toolbar.pack(fill="x")

        # Topic label + input
        tk.Label(
            toolbar, text="TOPIC",
            bg=THEME["sidebar"], fg=THEME["subtext"],
            font=FONTS["small"]
        ).pack(side="left", padx=(20, 4))

        self.topic_var = tk.StringVar()
        topic_entry = tk.Entry(
            toolbar,
            textvariable=self.topic_var,
            bg=THEME["card"], fg=THEME["text"],
            insertbackground=THEME["accent"],
            relief="flat",
            font=FONTS["heading"],
            width=28
        )
        topic_entry.pack(side="left", padx=(0, 18), ipady=5)

        # Mood picker
        tk.Label(
            toolbar, text="MOOD",
            bg=THEME["sidebar"], fg=THEME["subtext"],
            font=FONTS["small"]
        ).pack(side="left", padx=(0, 4))

        self.mood_var = tk.StringVar(value=MOODS[0])
        mood_menu = tk.OptionMenu(toolbar, self.mood_var, *MOODS)
        mood_menu.configure(
            bg=THEME["card"], fg=THEME["text"],
            activebackground=THEME["card_hover"],
            activeforeground=THEME["text"],
            relief="flat", font=FONTS["label"],
            highlightthickness=0, bd=0
        )
        mood_menu["menu"].configure(
            bg=THEME["card"], fg=THEME["text"],
            font=FONTS["label"]
        )
        mood_menu.pack(side="left", padx=(0, 18))

        # Action buttons (right-aligned)
        self._make_btn(toolbar, "🗑  Delete", THEME["border"],
                       THEME["text"], self._delete_entry).pack(side="right", padx=6)
        self._make_btn(toolbar, "💾  Save", THEME["accent"],
                       "white", self._save_entry).pack(side="right", padx=(0, 4))

    def _make_btn(self, parent, text, bg, fg, cmd):
        return tk.Button(
            parent, text=text,
            bg=bg, fg=fg,
            font=FONTS["btn"],
            relief="flat", cursor="hand2",
            activebackground=THEME["card_hover"],
            activeforeground=THEME["text"],
            padx=12, pady=6,
            command=cmd
        )

        # ── Date display ─────────────────────────
    def _build_date_bar(self):
        """Show current date under the toolbar when creating a new entry."""
        if hasattr(self, "date_bar"):
            self.date_bar.destroy()
        self.date_bar = tk.Frame(self, bg=THEME["entry_bg"])
        self.date_bar.pack(fill="x", padx=24, pady=(10, 0))

        date_str = self.current_key if self.current_key else \
                   datetime.now().strftime("%Y-%m-%d  %H:%M")
        tk.Label(
            self.date_bar,
            text=f"📅  {date_str}",
            bg=THEME["entry_bg"], fg=THEME["subtext"],
            font=FONTS["small"]
        ).pack(side="left")

        # ── Writing canvas ────────────────────────
    def _build_text_area(self):
        if hasattr(self, "text_frame"):
            self.text_frame.destroy()

        self.text_frame = tk.Frame(self, bg=THEME["entry_bg"])
        self.text_frame.pack(fill="both", expand=True, padx=24, pady=12)

        # Prompt placeholder label above text box
        tk.Label(
            self.text_frame,
            text="Dear Diary…",
            bg=THEME["entry_bg"], fg=THEME["accent"],
            font=("Georgia", 15, "italic")
        ).pack(anchor="w", pady=(0, 6))

        # Text widget + scrollbar
        txt_container = tk.Frame(self.text_frame, bg=THEME["border"], bd=1)
        txt_container.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(txt_container, bg=THEME["sidebar"])
        scroll.pack(side="right", fill="y")

        self.text_area = tk.Text(
            txt_container,
            bg=THEME["entry_bg"],
            fg=THEME["text"],
            insertbackground=THEME["accent2"],
            font=FONTS["body"],
            wrap="word",
            relief="flat",
            padx=16, pady=14,
            spacing3=4,
            yscrollcommand=scroll.set,
            undo=True
        )
        self.text_area.pack(fill="both", expand=True)
        scroll.configure(command=self.text_area.yview)

        # Word count bar
        self.word_count_var = tk.StringVar(value="0 words")
        tk.Label(
            self.text_frame,
            textvariable=self.word_count_var,
            bg=THEME["entry_bg"], fg=THEME["subtext"],
            font=FONTS["small"]
        ).pack(anchor="e", pady=(4, 0))

        self.text_area.bind("<KeyRelease>", self._update_word_count)

    # ─────────────────────────────────────────────
    #  LOAD / CLEAR
    # ─────────────────────────────────────────────
    def load_entry(self, key=None):
        """
        Load an existing entry (by key) or open a blank editor.
        Called by Part 1 whenever user clicks a card or 'New Entry'.
        """
        self.current_key = key

        # Rebuild date bar and text area fresh
        self._build_date_bar()
        self._build_text_area()

        if key and key in self.app.entries:
            entry = self.app.entries[key]
            self.topic_var.set(entry.get("topic", ""))
            self.mood_var.set(entry.get("mood", MOODS[0]))
            self.text_area.insert("1.0", entry.get("body", ""))
            self.app.status_msg.set(f"Loaded entry: {key}")
        else:
            self.topic_var.set("")
            self.mood_var.set(MOODS[0])
            self.app.status_msg.set("New entry — start writing ✦")

        self._update_word_count()

    # ─────────────────────────────────────────────
    #  SAVE
    # ─────────────────────────────────────────────
    def _save_entry(self):
        body  = self.text_area.get("1.0", "end").strip()
        topic = self.topic_var.get().strip()

        if not body:
            messagebox.showwarning("Empty Entry", "Write something before saving!")
            return
        if not topic:
            topic = "Untitled"

        # Generate a key for new entries
        key = self.current_key or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.app.entries[key] = {
            "topic": topic,
            "mood":  self.mood_var.get(),
            "body":  body,
            "saved": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_entries(self.app.entries)

        self.current_key = key
        self.app.selected_key.set(key)
        self.app.refresh_sidebar()
        self.app.status_msg.set(f"✅  Saved — {key}")
        self._build_date_bar()   # refresh date label

    # ─────────────────────────────────────────────
    #  DELETE
    # ─────────────────────────────────────────────
    def _delete_entry(self):
        if not self.current_key:
            messagebox.showinfo("Nothing to delete", "This entry hasn't been saved yet.")
            return

        confirm = messagebox.askyesno(
            "Delete Entry",
            f"Delete '{self.topic_var.get() or self.current_key}'?\nThis cannot be undone."
        )
        if confirm:
            del self.app.entries[self.current_key]
            save_entries(self.app.entries)
            self.app.selected_key.set("")
            self.app.status_msg.set("Entry deleted.")
            self.app.refresh_sidebar()
            self.load_entry(key=None)

    # ─────────────────────────────────────────────
    #  WORD COUNT
    # ─────────────────────────────────────────────
    def _update_word_count(self, event=None):
        text  = self.text_area.get("1.0", "end").strip()
        words = len(text.split()) if text else 0
        self.word_count_var.set(f"{words} word{'s' if words != 1 else ''}")
