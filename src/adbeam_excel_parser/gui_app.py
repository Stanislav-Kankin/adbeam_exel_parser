from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from adbeam_excel_parser.excel_reader import read_excel_summary

WINDOW_TITLE = "AdBeam Excel Parser"
WINDOW_SIZE = "980x720"
TEXT_FONT = ("Consolas", 10)


class ExcelParserApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(840, 520)

        self.file_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Выберите Excel-файл для проверки.")

        self._build_layout()

    def run(self) -> None:
        self.root.mainloop()

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        top_frame = ttk.Frame(self.root, padding=12)
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            top_frame,
            text="AdBeam Excel Parser — шаг 2",
            font=("Segoe UI", 16, "bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        path_frame = ttk.Frame(top_frame)
        path_frame.grid(row=1, column=0, sticky="ew")
        path_frame.columnconfigure(0, weight=1)

        path_entry = ttk.Entry(path_frame, textvariable=self.file_path_var)
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        browse_button = ttk.Button(path_frame, text="Выбрать файл", command=self._browse_file)
        browse_button.grid(row=0, column=1, sticky="ew")

        controls_frame = ttk.Frame(top_frame)
        controls_frame.grid(row=2, column=0, sticky="w", pady=(10, 0))

        run_button = ttk.Button(controls_frame, text="Проверить Excel", command=self._analyze_file)
        run_button.grid(row=0, column=0, padx=(0, 8))

        clear_button = ttk.Button(controls_frame, text="Очистить", command=self._clear_output)
        clear_button.grid(row=0, column=1)

        hint_label = ttk.Label(
            top_frame,
            text="Сейчас интерфейс работает через выбор файла кнопкой. CLI-режим тоже сохранен.",
        )
        hint_label.grid(row=3, column=0, sticky="w", pady=(10, 0))

        status_frame = ttk.Frame(self.root, padding=(12, 0, 12, 8))
        status_frame.grid(row=1, column=0, sticky="ew")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor="w")

        output_frame = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        output_frame.grid(row=2, column=0, sticky="nsew")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap="word", font=TEXT_FONT)
        self.output_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def _browse_file(self) -> None:
        selected_file = filedialog.askopenfilename(
            title="Выберите Excel-файл",
            filetypes=[("Excel files", "*.xlsx")],
        )
        if selected_file:
            self.file_path_var.set(selected_file)
            self.status_var.set("Файл выбран. Нажмите 'Проверить Excel'.")

    def _analyze_file(self) -> None:
        raw_path = self.file_path_var.get().strip()
        if not raw_path:
            messagebox.showwarning("Нет файла", "Сначала выберите Excel-файл.")
            return

        try:
            file_path = Path(raw_path).expanduser().resolve()
            summary = read_excel_summary(file_path)
        except Exception as exc:
            self.status_var.set("Ошибка при чтении Excel.")
            messagebox.showerror("Ошибка", str(exc))
            return

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", summary.model_dump_json(indent=2, exclude_none=True))
        self.status_var.set(
            f"Готово: лист '{summary.sheet_name}', строк {summary.total_rows}, сайтов найдено {summary.rows_with_websites}."
        )

    def _clear_output(self) -> None:
        self.file_path_var.set("")
        self.output_text.delete("1.0", tk.END)
        self.status_var.set("Выберите Excel-файл для проверки.")


def run_gui() -> None:
    app = ExcelParserApp()
    app.run()
