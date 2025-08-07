import tkinter as tk

class HP12CCalculator:
    def __init__(self, master):
        self.master = master
        master.title("HP-12C Simulator")

        # RPN Stack: X, Y, Z, T
        self.stack = [0.0, 0.0, 0.0, 0.0]
        # Financial registers: n, i (as decimal), PV, PMT, FV
        self.registers = {key: 0.0 for key in ['n', 'i', 'PV', 'PMT', 'FV']}

        # Display for X register
        self.display_var = tk.StringVar(value=self.format_number(self.stack[0]))
        self.display = tk.Entry(master, textvariable=self.display_var,
                                 font=("Arial", 24), bd=10, relief=tk.RIDGE, justify='right')
        self.display.grid(row=0, column=0, columnspan=6, pady=(10,0), sticky='we')

        # Frame for financial registers display
        reg_frame = tk.LabelFrame(master, text="Financial Registers", padx=5, pady=5)
        reg_frame.grid(row=1, column=0, columnspan=6, pady=10, sticky='we')
        self.reg_labels = {}
        for idx, key in enumerate(['n', 'i', 'PV', 'PMT', 'FV']):
            lbl = tk.Label(reg_frame, text=f"{key}: {self.format_number(self.registers[key])}",
                           width=12, anchor='w')
            lbl.grid(row=0, column=idx, padx=5)
            self.reg_labels[key] = lbl

        # Basic RPN buttons
        btn_text = [
            ('7', self.enter_digit), ('8', self.enter_digit), ('9', self.enter_digit), ('/', self.op_div),
            ('4', self.enter_digit), ('5', self.enter_digit), ('6', self.enter_digit), ('*', self.op_mul),
            ('1', self.enter_digit), ('2', self.enter_digit), ('3', self.enter_digit), ('-', self.op_sub),
            ('0', self.enter_digit), ('.', self.enter_dot), ('ENTER', self.op_enter), ('+', self.op_add),
        ]
        for idx, (txt, cmd) in enumerate(btn_text):
            tk.Button(master, text=txt, width=5, height=2,
                      command=lambda t=txt, c=cmd: c(t)).grid(row=2 + idx//4, column=idx%4, padx=3, pady=3)

        # Financial functions and STO/RCL
        fn_frame = tk.Frame(master)
        fn_frame.grid(row=2, column=4, rowspan=4, padx=5)
        funcs = [
            ('n STO', lambda: self.op_sto('n')), ('n RCL', lambda: self.op_rcl('n')),
            ('i STO', lambda: self.op_sto('i')), ('i RCL', lambda: self.op_rcl('i')),
            ('PV', self.compute_pv), ('PMT', self.compute_pmt),
            ('FV', self.compute_fv), ('PV STO', lambda: self.op_sto('PV')),
            ('PMT STO', lambda: self.op_sto('PMT')), ('FV STO', lambda: self.op_sto('FV')),
        ]
        for idx, (txt, cmd) in enumerate(funcs):
            tk.Button(fn_frame, text=txt, width=8, command=cmd).grid(row=idx//2, column=idx%2, pady=2)

    def format_number(self, num):
        return f"{num:.10g}"

    def update_display(self):
        self.display_var.set(self.format_number(self.stack[0]))

    def update_registers(self):
        for key, val in self.registers.items():
            self.reg_labels[key].config(text=f"{key}: {self.format_number(val)}")

    # RPN operations
    def op_enter(self, _=None):
        self.stack = [self.stack[0]] + self.stack[:-1]
        self.update_display()

    def push(self, value):
        self.op_enter()
        self.stack[0] = value
        self.update_display()

    def op_add(self, _=None):
        r = self.stack[1] + self.stack[0]
        self.stack = [r] + self.stack[2:]
        self.update_display()

    def op_sub(self, _=None):
        r = self.stack[1] - self.stack[0]
        self.stack = [r] + self.stack[2:]
        self.update_display()

    def op_mul(self, _=None):
        r = self.stack[1] * self.stack[0]
        self.stack = [r] + self.stack[2:]
        self.update_display()

    def op_div(self, _=None):
        r = self.stack[1] / self.stack[0] if self.stack[0] != 0 else float('inf')
        self.stack = [r] + self.stack[2:]
        self.update_display()

    def enter_digit(self, digit):
        cur = self.display_var.get()
        new = digit if cur == '0' else cur + digit
        try:
            val = float(new)
            self.stack[0] = val
            self.update_display()
        except ValueError:
            pass

    def enter_dot(self, _=None):
        cur = self.display_var.get()
        if '.' not in cur:
            self.display_var.set(cur + '.')

    # Register operations
    def op_sto(self, key):
        self.registers[key] = self.stack[0]
        self.update_registers()

    def op_rcl(self, key):
        self.push(self.registers[key])

    # Financial computations
    def compute_pv(self):
        n = self.registers['n']
        i = self.registers['i']
        pmt = self.registers['PMT']
        fv = self.registers['FV']
        pv = -(pmt*(1 - (1+i)**(-n))/i + fv*(1+i)**(-n))
        self.registers['PV'] = pv
        self.push(pv)
        self.update_registers()

    def compute_fv(self):
        n = self.registers['n']
        i = self.registers['i']
        pmt = self.registers['PMT']
        pv = self.registers['PV']
        fv = -(pv*(1+i)**n + pmt*(( (1+i)**n -1)/i ))
        self.registers['FV'] = fv
        self.push(fv)
        self.update_registers()

    def compute_pmt(self):
        n = self.registers['n']
        i = self.registers['i']
        pv = self.registers['PV']
        fv = self.registers['FV']
        pmt = -(pv*i/(1 - (1+i)**(-n)) + fv*i/((1+i)**n -1))
        self.registers['PMT'] = pmt
        self.push(pmt)
        self.update_registers()

if __name__ == "__main__":
    root = tk.Tk()
    HP12CCalculator(root)
    root.mainloop()
