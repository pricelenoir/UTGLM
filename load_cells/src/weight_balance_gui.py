import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import colorsys
import math

class WeightBalanceBoard:
    def __init__(self, master):
        self.master = master
        master.title("Golf Swing Balance Board Analyzer")

        # Canvas for visualization
        self.canvas_width = 600
        self.canvas_height = 500
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.pack(pady=20)

        # Labels frame
        self.info_frame = tk.Frame(master, bg='black')
        self.info_frame.pack(pady=10, fill=tk.X)

        self.title_label = tk.Label(self.info_frame, text="GOLF SWING BALANCE ANALYZER",
                                    font=("Helvetica", 16, "bold"), bg='black', fg='white')
        self.title_label.pack(pady=5)

        self.weight_frame = tk.Frame(self.info_frame, bg='black')
        self.weight_frame.pack(pady=5)

        self.weight_labels = {
            'top_right': tk.Label(self.weight_frame, text="TOP RIGHT: 0.00", font=("Helvetica", 12), bg='black', fg='#3498db', width=20),
            'bottom_right': tk.Label(self.weight_frame, text="BOTTOM RIGHT: 0.00", font=("Helvetica", 12), bg='black', fg='#2ecc71', width=20),
            'top_left': tk.Label(self.weight_frame, text="TOP LEFT: 0.00", font=("Helvetica", 12), bg='black', fg='#e74c3c', width=20),
            'bottom_left': tk.Label(self.weight_frame, text="BOTTOM LEFT: 0.00", font=("Helvetica", 12), bg='black', fg='#f39c12', width=20)
        }

        for i, (key, label) in enumerate(self.weight_labels.items()):
            label.grid(row=0, column=i, padx=5)

        self.com_label = tk.Label(self.info_frame, text="CENTER OF MASS: (0.00, 0.00)",
                                  font=("Helvetica", 14, "bold"), bg='black', fg='white')
        self.com_label.pack(pady=5)

        self.hint_label = tk.Label(self.info_frame, text="IDEAL POSITION: CENTER",
                                   font=("Helvetica", 10, "italic"), bg='black', fg='#7f8c8d')
        self.hint_label.pack(pady=2)

        # Board layout info
        self.board_left = 100
        self.board_top = 100
        self.board_right = self.canvas_width - 100
        self.board_bottom = self.canvas_height - 100
        self.board_width = self.board_right - self.board_left
        self.board_height = self.board_bottom - self.board_top

        self.load_cell_points = {
            'top_right': (self.board_right, self.board_top),
            'bottom_right': (self.board_right, self.board_bottom),
            'top_left': (self.board_left, self.board_top),
            'bottom_left': (self.board_left, self.board_bottom)
        }

        # Pre-draw static background
        self.static_background = self.create_static_background()
        self.canvas.create_image(0, 0, image=self.static_background, anchor=tk.NW, tags='background')

        # Placeholders for dynamic elements
        self.heatmap_id = None
        self.com_id = None

    def create_static_background(self):
        img = Image.new("RGB", (self.canvas_width, self.canvas_height), "black")
        draw = ImageDraw.Draw(img)

        # Board outline
        draw.rectangle([self.board_left, self.board_top, self.board_right, self.board_bottom],
                       outline="#27ae60", width=3)

        # Gridlines
        for i in range(1, 4):
            x = self.board_left + (self.board_width * i // 4)
            y = self.board_top + (self.board_height * i // 4)
            draw.line([x, self.board_top, x, self.board_bottom], fill="#2c3e50", width=1)
            draw.line([self.board_left, y, self.board_right, y], fill="#2c3e50", width=1)

        return ImageTk.PhotoImage(img)

    def generate_heatmap(self, weights):
        size = 80  # Lower resolution heatmap
        heatmap = np.zeros((size, size, 3), dtype=np.uint8)

        top_right = max(0, weights.get('Differential 0-1', [0])[0])
        bottom_right = max(0, weights.get('Differential 2-3', [0])[0])
        top_left = max(0, weights.get('Differential 4-5', [0])[0])
        bottom_left = max(0, weights.get('Differential 6-7', [0])[0])

        total_weight = top_right + bottom_right + top_left + bottom_left
        if total_weight == 0:
            total_weight = 1.0

        for y in range(size):
            for x in range(size):
                nx = x / size
                ny = y / size

                d_tl = math.hypot(nx - 0, ny - 0)
                d_tr = math.hypot(nx - 1, ny - 0)
                d_bl = math.hypot(nx - 0, ny - 1)
                d_br = math.hypot(nx - 1, ny - 1)

                influence = 2.0
                i_tl = 1.0 / (1.0 + d_tl * influence)
                i_tr = 1.0 / (1.0 + d_tr * influence)
                i_bl = 1.0 / (1.0 + d_bl * influence)
                i_br = 1.0 / (1.0 + d_br * influence)

                w_tl = i_tl * top_left / total_weight
                w_tr = i_tr * top_right / total_weight
                w_bl = i_bl * bottom_left / total_weight
                w_br = i_br * bottom_right / total_weight

                total_influence = w_tl + w_tr + w_bl + w_br
                if total_influence > 0:
                    avg_hue = (0.0 * w_tl + 0.6 * w_tr + 0.083 * w_bl + 0.3 * w_br) / total_influence
                    sat = min(1.0, total_influence * 2)
                    light = 0.5 * (1.0 - min(0.8, total_influence))
                    r, g, b = colorsys.hls_to_rgb(avg_hue, light, sat)
                    heatmap[y, x] = [int(r*255), int(g*255), int(b*255)]
                else:
                    heatmap[y, x] = [0, 0, 0]

        return Image.fromarray(heatmap)

    def calculate_center_of_mass(self, weights):
        top_right = weights.get('Differential 0-1', [0])[0]
        bottom_right = weights.get('Differential 2-3', [0])[0]
        top_left = weights.get('Differential 4-5', [0])[0]
        bottom_left = weights.get('Differential 6-7', [0])[0]

        total_weight = top_right + bottom_right + top_left + bottom_left
        if total_weight == 0:
            return ((self.board_left + self.board_right) / 2, (self.board_top + self.board_bottom) / 2)

        x = (self.load_cell_points['top_right'][0] * top_right +
             self.load_cell_points['bottom_right'][0] * bottom_right +
             self.load_cell_points['top_left'][0] * top_left +
             self.load_cell_points['bottom_left'][0] * bottom_left) / total_weight

        y = (self.load_cell_points['top_right'][1] * top_right +
             self.load_cell_points['bottom_right'][1] * bottom_right +
             self.load_cell_points['top_left'][1] * top_left +
             self.load_cell_points['bottom_left'][1] * bottom_left) / total_weight

        return x, y

    def update_visualization(self, voltages, weights):
        if self.heatmap_id:
            self.canvas.delete(self.heatmap_id)
        if self.com_id:
            self.canvas.delete(self.com_id)

        heatmap_img = self.generate_heatmap(weights)
        heatmap_img = heatmap_img.resize(
            (self.board_right - self.board_left, self.board_bottom - self.board_top)
        )
        self.heatmap_photo = ImageTk.PhotoImage(heatmap_img)
        self.heatmap_id = self.canvas.create_image(
            self.board_left, self.board_top, image=self.heatmap_photo, anchor=tk.NW, tags='heatmap'
        )

        com_x, com_y = self.calculate_center_of_mass(weights)
        marker_size = 8
        self.com_id = self.canvas.create_oval(
            com_x - marker_size, com_y - marker_size,
            com_x + marker_size, com_y + marker_size,
            fill='white', outline='', tags='com'
        )

        channel_keys = ['Differential 0-1', 'Differential 2-3', 'Differential 4-5', 'Differential 6-7']
        corner_positions = ['top_right', 'bottom_right', 'top_left', 'bottom_left']

        for i, key in enumerate(channel_keys):
            value = weights.get(key, [0])[0]
            corner_name = corner_positions[i].replace('_', ' ').upper()
            self.weight_labels[corner_positions[i]].config(text=f"{corner_name}: {value:.2f}")

        norm_x = 100 * (com_x - self.board_left) / (self.board_right - self.board_left)
        norm_y = 100 * (com_y - self.board_top) / (self.board_bottom - self.board_top)

        self.com_label.config(text=f"CENTER OF MASS: ({norm_x:.1f}%, {norm_y:.1f}%)")

        hint_text = "IDEAL: CENTER"
        if norm_x < 40:
            hint_text += " | TOO FAR TOE SIDE"
        elif norm_x > 60:
            hint_text += " | TOO FAR HEEL SIDE"
        if norm_y < 40:
            hint_text += " | TOO FAR FORWARD"
        elif norm_y > 60:
            hint_text += " | TOO FAR BACK"

        self.hint_label.config(text=hint_text)
