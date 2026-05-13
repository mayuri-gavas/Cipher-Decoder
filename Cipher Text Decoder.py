import customtkinter as ctk


class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cipher Pro")
        self.geometry("600x700")  # Reduced height since the wheel is gone
        self.configure(fg_color="#0a0a0a")
        self.current_shift = 0

        # Header
        ctk.CTkLabel(
            self,
            text="Cipher Decoder",
            font=("Consolas", 32, "bold"),
            text_color="#00FF41"
        ).pack(pady=20)

        # Input Section
        ctk.CTkLabel(self, text="MESSAGE INPUT:", text_color="white", font=("Consolas", 14)).pack()

        self.input_text = ctk.CTkTextbox(
            self,
            height=120,
            width=500,
            fg_color="#1a1a1a",
            text_color="#ffffff",
            border_color="#00FF41",
            border_width=1,
            font=("Consolas", 14)
        )
        self.input_text.pack(pady=10)

        # Shift Configuration Frame
        shift_frame = ctk.CTkFrame(self, fg_color="transparent")
        shift_frame.pack(pady=20)

        ctk.CTkLabel(
            shift_frame,
            text="SHIFT VALUE (0-25):",
            font=("Consolas", 16, "bold"),
            text_color="#00FF41"
        ).grid(row=0, column=0, padx=15)

        self.shift_entry = ctk.CTkEntry(
            shift_frame,
            width=80,
            height=35,
            placeholder_text="0",
            fg_color="#1a1a1a",
            text_color="#00FF41",
            border_color="#00FF41",
            font=("Consolas", 16, "bold"),
            justify="center"
        )
        self.shift_entry.grid(row=0, column=1)
        self.shift_entry.insert(0, "0")
        self.shift_entry.bind("<KeyRelease>", self.manual_shift_change)

        # Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="ENCRYPT",
            width=120,
            height=40,
            fg_color="#1f6aa5",
            font=("Consolas", 13, "bold"),
            command=lambda: self.process("enc")
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_frame,
            text="DECRYPT",
            width=120,
            height=40,
            fg_color="#942a2a",
            font=("Consolas", 13, "bold"),
            command=lambda: self.process("dec")
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            btn_frame,
            text="BRUTE FORCE",
            width=120,
            height=40,
            fg_color="#444",
            font=("Consolas", 13, "bold"),
            command=self.brute
        ).grid(row=0, column=2, padx=10)

        # Output Section
        ctk.CTkLabel(self, text="OUTPUT / ANALYSIS:", text_color="white", font=("Consolas", 14)).pack(pady=(10, 0))

        self.output_text = ctk.CTkTextbox(
            self,
            height=180,
            width=500,
            fg_color="#000000",
            text_color="#00FF41",
            border_color="#333",
            border_width=1,
            font=("Consolas", 13)
        )
        self.output_text.pack(pady=10)

        # Utility Buttons
        util_frame = ctk.CTkFrame(self, fg_color="transparent")
        util_frame.pack(pady=20)

        ctk.CTkButton(
            util_frame,
            text="COPY RESULT",
            width=150,
            command=self.copy_res
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            util_frame,
            text="CLEAR ALL",
            width=150,
            fg_color="transparent",
            border_width=1,
            command=self.clear
        ).grid(row=0, column=1, padx=10)

    def manual_shift_change(self, event):
        val = self.shift_entry.get()
        try:
            if val.isdigit():
                self.current_shift = int(val) % 26
            elif len(val) == 1 and val.isalpha():
                self.current_shift = ord(val.upper()) - 65
        except ValueError:
            self.current_shift = 0

    def process(self, mode):
        text = self.input_text.get("1.0", "end-1c")
        # Ensure we have the latest shift from the entry
        self.manual_shift_change(None)

        s = self.current_shift if mode == "enc" else -self.current_shift

        res = "".join([
            chr((ord(c) - (65 if c.isupper() else 97) + s) % 26 + (65 if c.isupper() else 97))
            if c.isalpha() else c
            for c in text
        ])

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", res)

    def brute(self):
        text = self.input_text.get("1.0", "end-1c")
        res = "--- BRUTE FORCE ANALYSIS ---\n"

        for i in range(26):
            trial = "".join([
                chr((ord(c) - (65 if c.isupper() else 97) - i) % 26 + (65 if c.isupper() else 97))
                if c.isalpha() else c
                for c in text
            ])
            res += f"Shift {i:02d} ({chr(65 + i)}): {trial[:40]}...\n"

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", res)

    def copy_res(self):
        self.clipboard_clear()
        self.clipboard_append(self.output_text.get("1.0", "end-1c"))

    def clear(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.shift_entry.delete(0, "end")
        self.shift_entry.insert(0, "0")
        self.current_shift = 0


if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()