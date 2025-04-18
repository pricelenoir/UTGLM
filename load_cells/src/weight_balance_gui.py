import tkinter as tk

class WeightBalanceBoard:
    def __init__(self, master):
        self.master = master
        master.title("Weight Balancing Board")
        
        # Canvas for visualization
        self.canvas_width = 400
        self.canvas_height = 300
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(pady=20)
        
        # Labels for weight values
        self.weight_frame = tk.Frame(master)
        self.weight_frame.pack(pady=10)
        
        self.weight_labels = {
            'top_right': tk.Label(self.weight_frame, text="Top Right: 0.00"),       # Differential 0-1
            'bottom_right': tk.Label(self.weight_frame, text="Bottom Right: 0.00"), # Differential 2-3
            'top_left': tk.Label(self.weight_frame, text="Top Left: 0.00"),         # Differential 4-5
            'bottom_left': tk.Label(self.weight_frame, text="Bottom Left: 0.00")    # Differential 6-7
        }
        
        # Place weight labels
        for i, (key, label) in enumerate(self.weight_labels.items()):
            label.grid(row=0, column=i, padx=10)
        
        # COM label
        self.com_label = tk.Label(master, text="Center of Mass: (0.00, 0.00)")
        self.com_label.pack(pady=10)
        
        # Draw initial board
        self.draw_board()
        
    def draw_board(self):
        # Clear previous drawings
        self.canvas.delete('all')
        
        # Board boundaries
        padding = 50
        board_left = padding
        board_top = padding
        board_right = self.canvas_width - padding
        board_bottom = self.canvas_height - padding
        
        # Draw board outline
        self.canvas.create_rectangle(board_left, board_top, board_right, board_bottom, outline='black', width=2)
        
        # Load cell points (corners)
        point_size = 10
        self.load_cell_points = {
            'top_right': (board_right, board_top),       # Differential 0-1
            'bottom_right': (board_right, board_bottom), # Differential 2-3
            'top_left': (board_left, board_top),         # Differential 4-5
            'bottom_left': (board_left, board_bottom)    # Differential 6-7
        }
        
        # Draw load cell points and add labels
        for name, point in self.load_cell_points.items():
            x, y = point
            self.canvas.create_oval(x-point_size, y-point_size, x+point_size, y+point_size, fill='blue')
            
            # Add text labels for clarity
            label_offset_x = -20 if 'left' in name else 20
            label_offset_y = -15 if 'top' in name else 15
            channel_index = list(self.load_cell_points.keys()).index(name)
            diff_label = f"Diff {channel_index*2}-{channel_index*2+1}"
            self.canvas.create_text(x + label_offset_x, y + label_offset_y, text=diff_label, anchor=tk.CENTER)
    
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
            return (self.canvas_width/2, self.canvas_height/2)
        
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
    
    def update_visualization(self, voltages, weights):
        # Mapping differential channels to corner positions:
        # Differential 0-1: Top Right
        # Differential 2-3: Bottom Right
        # Differential 4-5: Top Left
        # Differential 6-7: Bottom Left
        channel_keys = ['Differential 0-1', 'Differential 2-3', 'Differential 4-5', 'Differential 6-7']
        corner_positions = ['top_right', 'bottom_right', 'top_left', 'bottom_left']
        
        # Update weight labels
        for i, key in enumerate(channel_keys):
            weight_value = weights.get(key, [0])[0]
            self.weight_labels[corner_positions[i]].config(
                text=f"{corner_positions[i].replace('_', ' ').title()}: {weight_value:.2f}"
            )
        
        # Calculate and draw Center of Mass
        self.canvas.delete('com')  # Remove previous COM marker
        com_x, com_y = self.calculate_center_of_mass(weights)
        self.canvas.create_oval(
            com_x-5, com_y-5, 
            com_x+5, com_y+5, 
            fill='red', 
            tags='com'
        )
        
        # Update COM label
        self.com_label.config(text=f"Center of Mass: ({com_x:.2f}, {com_y:.2f})")