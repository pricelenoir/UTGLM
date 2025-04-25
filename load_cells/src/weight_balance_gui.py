import tkinter as tk
import colorsys
import math
from PIL import Image, ImageTk
import numpy as np

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
        
        # Title
        self.title_label = tk.Label(self.info_frame, text="GOLF SWING BALANCE ANALYZER", 
                                    font=("Helvetica", 16, "bold"), bg='black', fg='white')
        self.title_label.pack(pady=5)
        
        # Weight labels
        self.weight_frame = tk.Frame(self.info_frame, bg='black')
        self.weight_frame.pack(pady=5)
        
        # Changed order to match physical layout
        self.weight_labels = {
            'top_right': tk.Label(self.weight_frame, text="TOP RIGHT: 0.00", 
                                 font=("Helvetica", 12), bg='black', fg='#3498db', width=20),
            'bottom_right': tk.Label(self.weight_frame, text="BOTTOM RIGHT: 0.00", 
                                     font=("Helvetica", 12), bg='black', fg='#2ecc71', width=20),
            'top_left': tk.Label(self.weight_frame, text="TOP LEFT: 0.00", 
                                font=("Helvetica", 12), bg='black', fg='#e74c3c', width=20),
            'bottom_left': tk.Label(self.weight_frame, text="BOTTOM LEFT: 0.00", 
                                    font=("Helvetica", 12), bg='black', fg='#f39c12', width=20)
        }
        
        # Place weight labels
        for i, (key, label) in enumerate(self.weight_labels.items()):
            label.grid(row=0, column=i, padx=5)
        
        # COM label
        self.com_label = tk.Label(self.info_frame, text="CENTER OF MASS: (0.00, 0.00)", 
                                 font=("Helvetica", 14, "bold"), bg='black', fg='white')
        self.com_label.pack(pady=5)
        
        # Hint label
        self.hint_label = tk.Label(self.info_frame, text="IDEAL POSITION: CENTER", 
                                  font=("Helvetica", 10, "italic"), bg='black', fg='#7f8c8d')
        self.hint_label.pack(pady=2)
        
        # Initialize the heatmap image
        self.heatmap_image = None
        self.heatmap_photo = None
        
        # Create visualization buffers
        self.board_left = 100
        self.board_top = 100
        self.board_right = self.canvas_width - 100
        self.board_bottom = self.canvas_height - 100
        self.board_width = self.board_right - self.board_left
        self.board_height = self.board_bottom - self.board_top
        
        # Load cell points (corners)
        self.load_cell_points = {
            'top_right': (self.board_right, self.board_top),       # Differential 0-1
            'bottom_right': (self.board_right, self.board_bottom), # Differential 2-3
            'top_left': (self.board_left, self.board_top),         # Differential 4-5
            'bottom_left': (self.board_left, self.board_bottom)    # Differential 6-7
        }
        
        # Draw initial board
        self.draw_board()
        
    def draw_board(self):
        # Clear previous drawings
        self.canvas.delete('all')
        
        # Background gradient
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, 
                                     fill='black', outline='')
        
        # Draw board outline - golf green color
        self.canvas.create_rectangle(
            self.board_left, self.board_top, 
            self.board_right, self.board_bottom, 
            outline='#27ae60', width=3, dash=(3, 5), tags='board'
        )
        
        # Add gridlines
        for i in range(1, 4):
            # Vertical gridlines
            x = self.board_left + (self.board_width * i // 4)
            self.canvas.create_line(
                x, self.board_top, x, self.board_bottom,
                fill='#2c3e50', width=1, dash=(2, 4)
            )
            
            # Horizontal gridlines
            y = self.board_top + (self.board_height * i // 4)
            self.canvas.create_line(
                self.board_left, y, self.board_right, y,
                fill='#2c3e50', width=1, dash=(2, 4)
            )
        
        # Add feet outline in the center
        feet_width = self.board_width * 0.4
        feet_height = self.board_height * 0.6
        feet_left = self.board_left + (self.board_width - feet_width)/2
        feet_top = self.board_top + (self.board_height - feet_height)/2
        
        # Draw left foot outline
        left_foot_left = feet_left
        left_foot_top = feet_top
        left_foot_width = feet_width/2 - 10
        left_foot_height = feet_height
        
        self.canvas.create_oval(
            left_foot_left, left_foot_top,
            left_foot_left + left_foot_width, left_foot_top + left_foot_height,
            outline='#95a5a6', width=1, dash=(2, 2)
        )
        
        # Draw right foot outline
        right_foot_left = feet_left + feet_width/2 + 10
        right_foot_top = feet_top
        right_foot_width = feet_width/2 - 10
        right_foot_height = feet_height
        
        self.canvas.create_oval(
            right_foot_left, right_foot_top,
            right_foot_left + right_foot_width, right_foot_top + right_foot_height,
            outline='#95a5a6', width=1, dash=(2, 2)
        )
        
        # Draw load cell points
        self.draw_load_cells()
        
        # Add center target
        center_x = (self.board_left + self.board_right) / 2
        center_y = (self.board_top + self.board_bottom) / 2
        
        # Draw target circles
        for r in range(3, 0, -1):
            self.canvas.create_oval(
                center_x - r*10, center_y - r*10,
                center_x + r*10, center_y + r*10,
                outline='white', width=1, dash=(1, 1) if r > 1 else None
            )
    
    def draw_load_cells(self):
        # Draw load cell points with cool indicators
        for name, point in self.load_cell_points.items():
            x, y = point
            color = {
                'top_right': '#3498db',  # Blue
                'bottom_right': '#2ecc71',  # Green
                'top_left': '#e74c3c',  # Red
                'bottom_left': '#f39c12'  # Orange
            }[name]
            
            # Draw sensor indicator
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill='black', outline=color, width=2)
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color)
            
            # Create diagonal lines for a tech look
            line_length = 15
            if 'left' in name:
                self.canvas.create_line(x+8, y-8, x+8+line_length, y-8-line_length, fill=color)
                self.canvas.create_line(x+8, y+8, x+8+line_length, y+8+line_length, fill=color)
            else:
                self.canvas.create_line(x-8, y-8, x-8-line_length, y-8-line_length, fill=color)
                self.canvas.create_line(x-8, y+8, x-8-line_length, y+8+line_length, fill=color)
            
            # Add sensor label
            label_offset_x = -30 if 'left' in name else 30
            label_offset_y = -20 if 'top' in name else 20
            channel_index = list(self.load_cell_points.keys()).index(name)
            diff_label = f"DIFF {channel_index*2}-{channel_index*2+1}"
            
            self.canvas.create_text(x + label_offset_x, y + label_offset_y, 
                                   text=diff_label, fill=color, font=("Helvetica", 8))
    
    def generate_heatmap(self, weights):
        # Create a high-resolution heatmap
        heatmap_size = (200, 200)
        heatmap = np.zeros((heatmap_size[1], heatmap_size[0], 3), dtype=np.uint8)
        
        # Mapping of differential channels to physical locations
        # Diff 0-1: Top Right
        # Diff 2-3: Bottom Right
        # Diff 4-5: Top Left
        # Diff 6-7: Bottom Left
        top_right = max(0, weights.get('Differential 0-1', [0])[0])
        bottom_right = max(0, weights.get('Differential 2-3', [0])[0])
        top_left = max(0, weights.get('Differential 4-5', [0])[0])
        bottom_left = max(0, weights.get('Differential 6-7', [0])[0])
        
        # Normalize weights for color intensity
        total_weight = top_right + bottom_right + top_left + bottom_left
        if total_weight == 0:
            total_weight = 1.0  # Prevent division by zero
        
        # Generate influence field from each corner
        for y in range(heatmap_size[1]):
            for x in range(heatmap_size[0]):
                # Normalize coordinates to [0,1]
                nx = x / heatmap_size[0]
                ny = y / heatmap_size[1]
                
                # Calculate distances to each corner
                d_tl = math.sqrt((nx - 0)**2 + (ny - 0)**2)
                d_tr = math.sqrt((nx - 1)**2 + (ny - 0)**2)
                d_bl = math.sqrt((nx - 0)**2 + (ny - 1)**2)
                d_br = math.sqrt((nx - 1)**2 + (ny - 1)**2)
                
                # Influence is inversely proportional to distance squared
                influence_factor = 2.0  # Higher = sharper gradients
                i_tl = 1.0 / (1.0 + d_tl * influence_factor)
                i_tr = 1.0 / (1.0 + d_tr * influence_factor)
                i_bl = 1.0 / (1.0 + d_bl * influence_factor)
                i_br = 1.0 / (1.0 + d_br * influence_factor)
                
                # Weighted influence
                w_tl = i_tl * top_left / max(0.1, total_weight)
                w_tr = i_tr * top_right / max(0.1, total_weight)
                w_bl = i_bl * bottom_left / max(0.1, total_weight)
                w_br = i_br * bottom_right / max(0.1, total_weight)
                
                # Calculate hue that blends from colors based on weight
                # Red (0), Orange (0.083), Blue (0.6), Green (0.3) - in HSL space
                hue_tl = 0.0  # Red for top left
                hue_tr = 0.6  # Blue for top right
                hue_bl = 0.083  # Orange for bottom left
                hue_br = 0.3  # Green for bottom right
                
                # Combine hues based on weighted influence
                total_influence = w_tl + w_tr + w_bl + w_br
                if total_influence > 0:
                    avg_hue = (hue_tl * w_tl + hue_tr * w_tr + hue_bl * w_bl + hue_br * w_br) / total_influence
                    saturation = min(1.0, total_influence * 2)  # Higher weight = more saturation
                    lightness = 0.5 * (1.0 - min(0.8, total_influence))  # Higher weight = darker
                    
                    # Convert HSL to RGB
                    r, g, b = colorsys.hls_to_rgb(avg_hue, lightness, saturation)
                    heatmap[y, x] = [int(r*255), int(g*255), int(b*255)]
                else:
                    heatmap[y, x] = [0, 0, 0]  # Black for no weight
        
        # Convert to PIL Image
        img = Image.fromarray(heatmap)
        return img
    
    def calculate_center_of_mass(self, weights):
        # Mapping of differential channels to physical locations
        # Diff 0-1: Top Right
        # Diff 2-3: Bottom Right
        # Diff 4-5: Top Left
        # Diff 6-7: Bottom Left
        top_right = weights.get('Differential 0-1', [0])[0]
        bottom_right = weights.get('Differential 2-3', [0])[0]
        top_left = weights.get('Differential 4-5', [0])[0]
        bottom_left = weights.get('Differential 6-7', [0])[0]
        
        # Calculate total weight
        total_weight = top_right + bottom_right + top_left + bottom_left
        
        # Prevent division by zero
        if total_weight == 0:
            return ((self.board_left + self.board_right) / 2, 
                   (self.board_top + self.board_bottom) / 2)
        
        # Calculate weighted average positions
        x_pos = (
            (self.load_cell_points['top_right'][0] * top_right) + 
            (self.load_cell_points['bottom_right'][0] * bottom_right) + 
            (self.load_cell_points['top_left'][0] * top_left) + 
            (self.load_cell_points['bottom_left'][0] * bottom_left)
        ) / total_weight
        
        y_pos = (
            (self.load_cell_points['top_right'][1] * top_right) + 
            (self.load_cell_points['bottom_right'][1] * bottom_right) + 
            (self.load_cell_points['top_left'][1] * top_left) + 
            (self.load_cell_points['bottom_left'][1] * bottom_left)
        ) / total_weight
        
        return (x_pos, y_pos)
    
    def calculate_stability_score(self, com_x, com_y):
        # Calculate distance from center
        center_x = (self.board_left + self.board_right) / 2
        center_y = (self.board_top + self.board_bottom) / 2
        
        max_distance = math.sqrt((self.board_right - self.board_left)**2 + 
                                (self.board_bottom - self.board_top)**2) / 2
        
        distance = math.sqrt((com_x - center_x)**2 + (com_y - center_y)**2)
        
        # Convert to a score between 0-100
        stability_score = 100 * (1 - distance / max_distance)
        return max(0, min(100, stability_score))
    
    def update_visualization(self, voltages, weights):
        # Redraw board elements
        self.draw_board()
        
        # Generate and display heatmap
        heatmap_img = self.generate_heatmap(weights)
        heatmap_img = heatmap_img.resize((self.board_right - self.board_left, 
                                         self.board_bottom - self.board_top))
        
        self.heatmap_photo = ImageTk.PhotoImage(heatmap_img)
        self.canvas.create_image(self.board_left, self.board_top, 
                               image=self.heatmap_photo, anchor=tk.NW)
        
        # Calculate and draw Center of Mass
        com_x, com_y = self.calculate_center_of_mass(weights)
        
        # Draw COM marker
        marker_size = 8
        
        # Outer ring
        self.canvas.create_oval(
            com_x - marker_size*1.5, com_y - marker_size*1.5,
            com_x + marker_size*1.5, com_y + marker_size*1.5,
            outline='white', width=2, tags='com'
        )
        
        # Inner dot
        self.canvas.create_oval(
            com_x - marker_size/2, com_y - marker_size/2,
            com_x + marker_size/2, com_y + marker_size/2,
            fill='white', outline='', tags='com'
        )
        
        # Crosshairs
        line_length = 15
        self.canvas.create_line(com_x - line_length, com_y, com_x + line_length, com_y, 
                              fill='white', width=1, tags='com')
        self.canvas.create_line(com_x, com_y - line_length, com_x, com_y + line_length, 
                              fill='white', width=1, tags='com')
        
        # Calculate normalized position (0-100%)
        norm_x = 100 * (com_x - self.board_left) / (self.board_right - self.board_left)
        norm_y = 100 * (com_y - self.board_top) / (self.board_bottom - self.board_top)
        
        # Calculate stability score
        stability = self.calculate_stability_score(com_x, com_y)
        
        # Mapping differential channels to corner positions
        channel_keys = ['Differential 0-1', 'Differential 2-3', 'Differential 4-5', 'Differential 6-7']
        corner_positions = ['top_right', 'bottom_right', 'top_left', 'bottom_left']
        
        # Update weight labels
        for i, key in enumerate(channel_keys):
            weight_value = weights.get(key, [0])[0]
            corner_name = corner_positions[i].replace('_', ' ').upper()
            self.weight_labels[corner_positions[i]].config(
                text=f"{corner_name}: {weight_value:.2f}"
            )
        
        # Update COM label with stability score
        self.com_label.config(
            text=f"CENTER OF MASS: ({norm_x:.1f}%, {norm_y:.1f}%) - STABILITY: {stability:.0f}%"
        )
        
        # Update hint based on position
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