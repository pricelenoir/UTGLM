import numpy as np

def calculate_golf_shot(club_head_speed, club_type):
    # Club mass values (kg)
    club_masses = {
        'driver': 0.200,
        '3w': 0.210,
        '3i': 0.240,
        '4i': 0.247,
        '5i': 0.254,
        '6i': 0.261,
        '7i': 0.268,
        '8i': 0.275,
        '9i': 0.282,
        'PW': 0.289,
        'GW': 0.296,
        'SW': 0.303,
        'LW': 0.310
    }
    
    # Club loft values (degrees)
    club_lofts = {
        'driver': 10.5,
        '3w': 15,
        '3i': 19,
        '4i': 24,
        '5i': 27,
        '6i': 30,
        '7i': 34,
        '8i': 38,
        '9i': 42,
        'PW': 47,
        'GW': 52,
        'SW': 56,
        'LW': 60
    }

    # Constants
    m = 0.046          # Mass of golf ball (kg)
    ball_radius = 2.1  # Radius of golf ball (cm)
    e = 0.830          # Coefficient of restitution
    lift_coef = 0.165  # Lift coefficient
    miss = 0;          # Distance from center hit (in)
    
    M = club_masses.get(club_type)
    loft = club_lofts.get(club_type)

    # Estimated Ball Speed
    vball = club_head_speed * (1 + e) * np.cos(np.radians(loft)) * (1 - 0.14 * miss) / (1 + (m / M))

    smash_factor = vball / club_head_speed
    
    # Estimated Launch Angle
    launch_angle = loft * (0.96 - 0.0071 * loft)

    # Determine drag coefficient based on ball speed
    speed_ranges = [0, 108, 115, 120.5, 126.5, 132.5, 137.5, 142.5, 147, 152.5, 159, 166.5, float('inf')]
    drag_values = [0.29, 0.29, 0.273, 0.255, 0.248, 0.23, 0.225, 0.229, 0.223, 0.237, 0.235, 0.223]
    drag_coef = drag_values[0]

    for i in range(len(speed_ranges) - 1):
        if speed_ranges[i] <= vball < speed_ranges[i + 1]:
            drag_coef = drag_values[i]
            break
    
    # Air density calculation
    temperature = 70 
    air_density = -0.003 * temperature + 1.42
    
    # Cross-sectional area
    cross_section = np.pi * (ball_radius * 0.01) ** 2
    
    # Combined coefficient
    coef = 0.5 * cross_section * air_density

    # Initialize data arrays
    dt = 0.01  # time step in seconds
    max_steps = 30000  # maximum number of steps to prevent infinite loops
    
    # Initialize simulation variables
    velocity = vball * 0.44704  # convert mph to m/s
    angle = np.radians(launch_angle)
    velocity_x = velocity * np.cos(angle)
    velocity_y = velocity * np.sin(angle)
    position_x = 0
    position_y = 0
    max_height = 0
    
    # Simulation loop
    i = 0
    while i < max_steps and position_y >= 0:
        # Calculate accelerations
        accel_x = (-coef * lift_coef * velocity**2 * np.sin(angle) / 0.0459) - (coef * drag_coef * velocity**2 * np.cos(angle) / 0.0459)
        accel_y = (coef * lift_coef * velocity**2 * np.cos(angle) / 0.0459) - (coef * drag_coef * velocity**2 * np.sin(angle) / 0.0459) - 9.81
        
        # Update velocities
        velocity_x = velocity_x + accel_x * dt
        velocity_y = velocity_y + accel_y * dt
        
        # Update angle and total velocity
        angle = np.arctan2(velocity_y, velocity_x)
        velocity = np.sqrt(velocity_x**2 + velocity_y**2)
        
        # Update positions
        delta_x = velocity_x * dt
        position_x = position_x + delta_x + (-0.5 * accel_x * dt**2)
        
        delta_y = velocity_y * dt
        position_y = position_y + delta_y + (-0.5 * accel_y * dt**2)
        
        # Track maximum height
        if position_y > max_height:
            max_height = position_y
            
        i += 1
    
    carry_distance = position_x * 1.09361  # convert m to yards
    max_height_ft = max_height * 3.28084   # convert m to feet
    
    results = {
        'carry_distance': round(carry_distance, 1),
        'club_head_speed': club_head_speed,
        'ball_speed': round(vball, 1),
        'smash_factor': round(smash_factor, 3),
        'max_height': round(max_height_ft, 1),
        'launch_angle': round(launch_angle, 1),
    }
    return results