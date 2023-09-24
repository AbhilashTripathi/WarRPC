import random

class BattlefieldSimulation:
    #constructor of the class
    def __init__(self, N, M, t, T, Si):
        self.N = N  # Grid size
        self.M = M  # Number of soldiers
        self.t = t  # Number of iterations (duration of battle)
        self.T = T  # Types of missiles (impact radii)
        self.Si = Si  # Initial soldier speed range
        
        #self.grid = [[0 for _ in range(self.N)] for _ in range(self.N)]  # Grid to represent soldiers
        # Initialize an empty grid (matrix) with self.N rows and self.N columns.
        self.grid = []

        # Create self.N rows.
        for _ in range(self.N):
            # Create a row (list) to store the elements in this row.
            row = []
            # Create self.N columns in the current row and set them to 0.
            for _ in range(self.N):
                row.append(0)
            # Append the row to the grid.
            self.grid.append(row)

        #print(self.grid)
            
        self.soldiers = []  # List to store soldier objects
        self.commander = None  # Current commander
        
        self.current_time = 0  # Current iteration
    
    def initialize_soldiers(self):
        for i in range(self.M):
            x = random.randint(0, self.N - 1)
            y = random.randint(0, self.N - 1)
            speed = random.randint(0, self.Si)
            soldier = {
                'id': i + 1,
                'x': x,
                'y': y,
                'speed': speed,
                'status': 'Alive',
                'is_commander': False
            }
            self.soldiers.append(soldier)
            self.grid[y][x] = i + 1

        #print(self.soldiers)
        
        self.commander = random.choice(self.soldiers)
        self.commander['is_commander'] = True
        #print(self.commander)

        #print(self.soldiers)       #this updated list will have 1 commmander in it
        
    def missile_approaching(self, position, time, missile_type):
        x, y = position     #this is the current_missile position
        print(f"Missile ({missile_type}) approaching at ({x}, {y}) at time {time}")
        for soldier in self.soldiers:
            if soldier['status'] == 'Alive':
                self.take_shelter(soldier, position)
    
    def status(self, soldier_id):
        soldier = next((s for s in self.soldiers if s['id'] == soldier_id), None)
        if soldier:
            return soldier['status']
        else:
            return None
    
    def status_all(self):
        statuses = {}
        for soldier in self.soldiers:
            statuses[soldier['id']] = soldier['status']
        return statuses
    
    #should return the soldier status
    def was_hit(self, soldier_id, is_hit):
        soldier = next((s for s in self.soldiers if s['id'] == soldier_id), None)
        if soldier:
            if is_hit:
                soldier['status'] = 'Hit'
            else:
                soldier['status'] = 'Alive'     #'Evasive Action'

    
    '''
    def take_shelter(self, soldier, missile_position):
        x, y = soldier['x'], soldier['y']
        mx, my = missile_position
        is_hit = False

        # Calculate the distance to the missile
        distance = max(abs(x - mx), abs(y - my))    #change it with distance left to cover wrt missile radius

        # Check if the soldier is within the red zone and has insufficient speed to escape
        if distance <= soldier['speed']:
            #soldier['status'] = 'Hit'
            is_hit = True
        else:
            is_hit = False
            # Calculate the direction to move away from the missile in the x and y directions
            dx = x - mx
            dy = y - my

            # Determine the direction (x or y) in which the soldier should move to increase distance
            move_x = abs(dx) >= abs(dy)
            move_y = not move_x

            # Calculate the movement in the chosen direction while limiting it to the soldier's maximum speed
            if move_x:
                dx = max(-soldier['speed'], min(soldier['speed'], dx))
                dy = 0
            else:
                dx = 0
                dy = max(-soldier['speed'], min(soldier['speed'], dy))

            # Update the soldier's position
            new_x = x + dx
            new_y = y + dy

            # Ensure the new position is within the battlefield boundaries
            if 0 <= new_x < self.N and 0 <= new_y < self.N:
                self.grid[y][x] = 0  # Clear old position
                self.grid[new_y][new_x] = soldier['id']  # Update grid
                soldier['x'], soldier['y'] = new_x, new_y

        #call was_hit() to update the status of thesoldier
        soldier_id = soldier['id']
        self.was_hit(soldier_id, is_hit)
'''

    def calculate_impact_area(missile_type, missile_position):
        # Initialize the impact area with the center coordinate (x, y)
        x, y = missile_position
        impact_area = [missile_position]

        # Define the offsets for the neighboring coordinates based on the missile type
        if missile_type == 'M1':
            # M1 impacts only the center coordinate
            return impact_area
        elif missile_type == 'M2':
            offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2)]
        elif missile_type == 'M3':
            offsets = [(i, j) for i in range(-2, 3) for j in range(-2, 3)]
        elif missile_type == 'M4':
            offsets = [(i, j) for i in range(-3, 4) for j in range(-3, 4) ]

        # Calculate the neighboring coordinates within the impact area
        for offset in offsets:
            neighbor_x = x + offset[0]
            neighbor_y = y + offset[1]
            if 0 <= neighbor_x < N and 0 <= neighbor_y < N:
                impact_area.append((neighbor_x, neighbor_y))

        return impact_area
    
    def calculate_valid_neighbors(soldier):
        # Define the maximum offset based on the soldier's speed
        max_offset = soldier['speed']

        # Initialize a list to store valid neighboring coordinates
        valid_neighbors = []

        # Iterate through possible offsets
        for dx in range(-max_offset, max_offset + 1):
            for dy in range(-max_offset, max_offset + 1):
                # Calculate the neighbor's coordinates
                neighbor_x = soldier['x'] + dx
                neighbor_y = soldier['y'] + dy

                # Check if the neighbor is within the grid boundaries
                if 0 <= neighbor_x < N and 0 <= neighbor_y < N:
                    valid_neighbors.append((neighbor_x, neighbor_y))

    def take_shelter(self, soldier, missile_position, missile_type):
        is_hit = False
        #calculate impact coordinates
        impact_areas = self.calculate_impact_area(missile_type, missile_position)
        soldier_possible_coords = self.calculate_valid_neighbours(soldier)
        for soldier_possible_coord in soldier_possible_coords:
            if((soldier['x'], soldier['y']) not in impact_areas):
                is_hit = False
            elif(soldier_possible_coord not in impact_areas):
                soldier['x'] = soldier_possible_coord[0]
                soldier['y'] = soldier_possible_coord[1]
            else:
                is_hit = True

        #call was_hit() to update the status of thesoldier
        soldier_id = soldier['id']
        self.was_hit(soldier_id, is_hit)

    #def update_commander(soldier, self.commander):


    
    def print_layout(self):
        print(f"Time: {self.current_time}")
        
        # Print grid layout
        for row in self.grid:
            row_str = ''
            for cell in row:
                if cell == 0:
                    row_str += '.  '  # Empty cell
                else:
                    row_str += f'{cell}  '  # Soldier
            print(row_str)
        
        
        # Print soldier status
        soldier = self.status_all()
        for soldier in self.soldiers:
            print(f"Soldier {soldier['id']} - Status: {soldier['status']}")
        
    def simulate_battle(self):
        self.initialize_soldiers()
        for self.current_time in range(self.t):
            missile_type = random.choice(self.T)
            missile_x = random.randint(0, self.N - 1)
            missile_y = random.randint(0, self.N - 1)
            self.missile_approaching((missile_x, missile_y), self.current_time, missile_type)
            
            # Check status after missile impact
            #statuses = self.status_all()
            #print(statuses)
            
            self.print_layout()

            self.update_commander()
            
            # Check battle outcome
            casualty_count = self.M - len([s for s in self.soldiers if s['status'] == 'Alive'])
            if (self.M - casualty_count) / self.M <= 0.5:
                print("Battle lost!")
                break
        else:
            print("Battle won.")

# Define hyperparameters
N = 30  # Grid size
M = 10  # Number of soldiers
t = 20  # Number of iterations (duration of battle)
T = ['M1', 'M2', 'M3', 'M4']  # Types of missiles (impact radii)
Si = 4  # Initial soldier speed range

# Create and run the simulation
sim = BattlefieldSimulation(N, M, t, T, Si)
sim.simulate_battle()
