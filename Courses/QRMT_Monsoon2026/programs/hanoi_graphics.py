"""Animate the recursive Tower of Hanoi solution using Python's tkinter.

Run: python3 hanoi_graphics.py 5
Or:  python3 hanoi_graphics.py   (enter n in the window)

No third-party Python packages are needed. Some Python installations need
Tk support installed separately. The puzzle moves from A to C, using B.
"""
import argparse
import colorsys
import tkinter as tk
from tkinter import messagebox, ttk


def hanoi_moves(n, source=0, spare=1, target=2):
    """Yield (source, target) moves, one at a time, without storing the solution.

    Pre: n >= 0; the n disks are a top tower on source. Other disks are larger.
    Post: that tower has moved to target; other disks are unchanged.
    Safety invariant: each peg has smaller disks above larger ones.
    """
    if n < 0:
        raise ValueError('n must be nonnegative')
    if n == 0:                         # Explicit base case: nothing to move.
        return
    yield from hanoi_moves(n - 1, source, target, spare)
    yield source, target              # Move the exposed largest disk.
    yield from hanoi_moves(n - 1, spare, source, target)


class HanoiAnimation:
    def __init__(self, root, n):
        self.root = root
        root.title('Tower of Hanoi — recursion in action')
        root.geometry('960x650')
        root.minsize(750, 540)
        self.running = False
        self.timer = None
        self.done = False
        self.n = n
        self.count = 0
        self.pegs = []
        self.moves = iter(())

        controls = ttk.Frame(root, padding=12)
        controls.pack(fill='x')
        ttk.Label(controls, text='Number of disks (n):').pack(side='left')
        self.input_n = tk.StringVar(value=str(n))
        ttk.Entry(controls, textvariable=self.input_n, width=6).pack(side='left', padx=8)
        ttk.Button(controls, text='Restart / Apply n', command=self.reset).pack(side='left')
        self.play_button = ttk.Button(controls, text='Play', command=self.toggle)
        self.play_button.pack(side='left', padx=8)
        ttk.Button(controls, text='One move', command=self.step).pack(side='left')

        self.caption = tk.StringVar()
        ttk.Label(root, textvariable=self.caption, anchor='center',
                  font=('Arial', 14)).pack(fill='x', pady=8)
        self.canvas = tk.Canvas(root, background='#f5f7fb', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True, padx=12)
        self.canvas.bind('<Configure>', lambda event: self.draw())

        self.status = tk.StringVar()
        ttk.Label(root, textvariable=self.status, anchor='center').pack(fill='x', pady=8)
        speed = ttk.Frame(root, padding=(12, 0, 12, 10))
        speed.pack(fill='x')
        ttk.Label(speed, text='Delay between moves (milliseconds):').pack(side='left')
        self.delay = tk.DoubleVar(value=650)
        ttk.Scale(speed, from_=50, to=1500, variable=self.delay).pack(
            side='left', fill='x', expand=True, padx=12)
        ttk.Label(root, text='Rule: move one top disk; never put a larger disk on a smaller one.',
                  anchor='center').pack(fill='x', pady=(0, 10))
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.reset()

    def pause(self):
        self.running = False
        self.play_button.config(text='Play')
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None

    def reset(self):
        try:
            n = int(self.input_n.get())
            if not 0 <= n <= 20:
                raise ValueError
        except ValueError:
            messagebox.showerror('Invalid input', 'Enter an integer from 0 to 20.\n'
                                 'This limit keeps the disks visible; try 3–6 first.')
            return
        self.pause()
        self.n = n
        self.pegs = [list(range(n, 0, -1)), [], []]  # Bottom to top.
        self.moves = hanoi_moves(n)
        self.count = 0
        self.total = (1 << n) - 1
        self.done = n == 0
        self.last = None
        self.caption.set('No disks: the base case is already solved.' if self.done
                         else f'Move {n} disks from A to C, using B as the spare.')
        self.update_status()
        self.draw()

    def update_status(self):
        self.status.set(f'Moves: {self.count:,} / {self.total:,} = 2^{self.n} − 1'
                        + ('     •     Complete' if self.done else ''))

    def advance(self):
        if self.done:
            return
        source, target = next(self.moves)
        disk = self.pegs[source][-1]
        # Check legality independently of the recursive move generator.
        if self.pegs[target] and self.pegs[target][-1] < disk:
            raise RuntimeError('Attempted to put a larger disk on a smaller disk')
        self.pegs[source].pop()
        self.pegs[target].append(disk)
        self.count += 1
        self.last = source, target, disk
        self.caption.set(f'Move {self.count:,}: disk {disk}, '
                         f'{"ABC"[source]} → {"ABC"[target]}')
        self.done = len(self.pegs[2]) == self.n
        self.update_status()
        self.draw()
        if self.done:
            self.pause()

    def step(self):
        self.pause()
        self.advance()

    def toggle(self):
        if self.running:
            self.pause()
        elif not self.done:
            self.running = True
            self.play_button.config(text='Pause')
            self.tick()

    def tick(self):
        self.timer = None
        if self.running:
            self.advance()
            if self.running:
                self.timer = self.root.after(int(self.delay.get()), self.tick)

    def draw(self):
        c = self.canvas
        c.delete('all')
        if not self.pegs:
            return
        width, height = max(c.winfo_width(), 750), max(c.winfo_height(), 300)
        centers = [width * fraction for fraction in (1/6, 1/2, 5/6)]
        base = height - 55
        disk_height = min(30, (height - 130) / max(self.n, 1))
        max_width = width * .26
        for index, x in enumerate(centers):
            c.create_line(x, 75, x, base, fill='#8492a6', width=8)
            c.create_line(x - max_width/2, base, x + max_width/2, base,
                          fill='#334155', width=7)
            c.create_text(x, base + 28, text=('A — source', 'B — spare', 'C — destination')[index],
                          font=('Arial', 12))
            for level, disk in enumerate(self.pegs[index]):
                w = 35 + (max_width - 35) * disk / max(self.n, 1)
                y = base - level * disk_height
                rgb = colorsys.hsv_to_rgb((disk * .113) % 1, .55, .88)
                color = '#' + ''.join(f'{int(v * 255):02x}' for v in rgb)
                moved = self.last is not None and index == self.last[1] and disk == self.last[2]
                c.create_rectangle(x-w/2, y-disk_height+2, x+w/2, y-2,
                                   fill=color, outline='#111827' if moved else '#ffffff',
                                   width=3 if moved else 1)
                c.create_text(x, y-disk_height/2, text=str(disk),
                              font=('Arial', max(8, min(12, int(disk_height*.55)))), fill='#111827')
        if self.last:
            source, target, _ = self.last
            c.create_line(centers[source], 35, centers[target], 35,
                          arrow=tk.LAST, width=3, fill='#334155')

    def close(self):
        self.pause()
        self.root.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('n', type=int, nargs='?', default=4,
                        help='number of disks, 0–20 (default: 4)')
    args = parser.parse_args()
    if not 0 <= args.n <= 20:
        parser.error('For this display, n must be between 0 and 20.')
    root = tk.Tk()
    HanoiAnimation(root, args.n)
    root.mainloop()


if __name__ == '__main__':
    main()
