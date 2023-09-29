import random
import battle_pb2
import battle_pb2_grpc
import grpc
from concurrent import futures

class Defender(battle_pb2_grpc.DefenderServicer):

    def InitializeSoldiers(self, request, context):
        self.N = request.N
        self.T = request.T
        self.M = 0  # Initialize the number of soldiers

        soldier_details = self.initialize_soldiers()
        return battle_pb2.InitDetails(sol_details=soldier_details)

    def MissileApproaching(self, request, context):
        self.t = request.t
        self.missile_type = request.missile_type
        self.x = request.x
        self.y = request.y

        # Simulate the battle and take casuality count as return
        self.simulate_battle((self.x, self.y), self.missile_type)

        #return battle_pb2.TrackingDetails(casualty_count=self.casualty_count, soldier_count=len(Defender.soldiers))
        return battle_pb2.TrackingDetails(casualty_count=self.casualty_count, soldier_count=len(self.soldiers))
    
    def __init__(self, N, T):
        self.N = N  # Grid size
        self.T = T  # Number of iterations (duration of battle)
        self.t = 0  # Duration after which the attacker launches a new missile
        self.missile_types = ['M1', 'M2', 'M3', 'M4']  # Types of missiles (impact radii)
        self.speed = 0  # Initial soldier speed range
        self.casualty_count = 0  # Initialize casualty count

        self.grid = []
        # Initialize an empty grid (matrix) with self.N rows and self.N columns.
        for _ in range(self.N):
            row = [0] * self.N
            #Defender.grid.append(row)
            self.grid.append(row)

        self.soldiers = []  # List to store soldier objects
        self.commander = {}  # Current commander
        self.current_time = 0  # Current iteration

    def initialize_soldiers(self):
        occupied_positions = set()  # Create a set to store occupied positions
        generated_soldiers = 0  # Keep track of the number of generated soldiers

        while True:
            self.M = int(input(f"Enter the number of soldiers on the defender side (<= {self.N * self.N}): "))
            if self.M <= self.N * self.N:
                break

        while generated_soldiers < self.M:
            # Generate unique random positions
            while True:
                x = random.randint(0, self.N - 1)
                y = random.randint(0, self.N - 1)
                position = (x, y)

                # Check if the position is already occupied
                if position not in occupied_positions:
                    break  # Position is unique, exit the loop

            soldier = {
                'id': generated_soldiers + 1,
                'x': x,
                'y': y,
                'status': 'Alive',
                'is_commander': False,
                'speed': random.randint(0, 4)  # Set random soldier speed
            }
            #Defender.soldiers.append(soldier)
            self.soldiers.append(soldier)
            #Defender.grid[y][x] = generated_soldiers + 1  # Update grid
            self.grid[y][x] = generated_soldiers + 1  # Update grid

            # Add the occupied position to the set
            occupied_positions.add(position)
            generated_soldiers += 1  # Increment the count of generated soldiers

        # Choose a random soldier to be the commander
        #self.commander = random.choice(Defender.soldiers)
        self.commander = random.choice(self.soldiers)
        self.commander["is_commander"] = True

        print("Commander is: Soldier ",self.commander['id'])

        #return Defender.soldiers  # Return the list of soldier details
        return self.soldiers

    # Rest of the Defender class methods (simulate_battle, update_commander, etc.) remain the same

    def missile_approaching(self, position, time, missile_type):
        x, y = position
        print(f"Missile ({missile_type}) approaching at ({y}, {x})")
        #for soldier in Defender.soldiers:
        for soldier in self.soldiers:
            if soldier['status'] == 'Alive':
                self.take_shelter(soldier, position, missile_type)

    def update_commander(self):
    # Check if the current commander is alive
        if self.commander["status"] == 'Alive':
            return  # Commander is still alive, no need to update

        # Find all alive soldiers who are not the current commander
        alive_soldiers = []
        #for soldier in Defender.soldiers:
        for soldier in self.soldiers:
            if soldier["status"] == 'Alive': #and not soldier.get('is_commander'):
                alive_soldiers.append(soldier)

        if alive_soldiers:
            # Choose a random soldier from the alive soldiers to be the new commander
            commander = random.choice(alive_soldiers)
            commander["is_commander"]= True
            print(f"New commander is {commander}")

    def status(self, soldier_id):
        soldier = next((s for s in self.soldiers if s['id'] == soldier_id), None)
        if soldier:
            return soldier['status']
        else:
            return None

    def status_all(self, soldiers):
        for soldier in self.soldiers:
            if soldier['status'] == 'Hit' or soldier['status'] == 'Deceased':
                soldier['status'] = 'Deceased'
                #Defender.grid[soldier['y']][soldier['x']] = 0
                self.grid[soldier['y']][soldier['x']] = 0
            else:
                soldier['status'] = 'Alive'
                    
        statuses = {}
        for soldier in self.soldiers:
            statuses[soldier['id']] = soldier['status']
        return statuses

    # Returns soldier status
    def was_hit(self, soldier_id, is_hit):
        soldier = next((s for s in self.soldiers if s['id'] == soldier_id), None)
        if soldier:
            if is_hit:
                soldier['status'] = 'Hit'
            else:
                soldier['status'] = 'Alive'

    def calculate_impact_area(self, missile_position, missile_type):
        # Initialize the impact area with the center coordinate (x, y)
        x, y = missile_position
        impact_area = [missile_position]
        offsets = []
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
            if 0 <= neighbor_x < self.N and 0 <= neighbor_y < self.N:
                impact_area.append((neighbor_x, neighbor_y))

        return impact_area

    def calculate_valid_neighbours(self, soldier):
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
                if 0 <= neighbor_x < self.N and 0 <= neighbor_y < self.N:
                    valid_neighbors.append((neighbor_x, neighbor_y))
        return valid_neighbors

    def take_shelter(self, soldier, missile_position, missile_type):
        x, y = soldier['x'], soldier['y']
        mx, my = missile_position
        is_hit = False
        
        #calculate impact coordinates
        impact_areas = self.calculate_impact_area((mx, my), missile_type)
        soldier_possible_coords = self.calculate_valid_neighbours(soldier)

        #if soldier is outside impact zone, he's safe
        if((x, y) not in impact_areas):
                is_hit = False
        else:
            new_x = x
            new_y = y
            for soldier_possible_coord in soldier_possible_coords:
                #if(soldier_possible_coord not in impact_areas and (Defender.grid[soldier_possible_coord[1]][soldier_possible_coord[0]] == 0)):
                if(soldier_possible_coord not in impact_areas and (self.grid[soldier_possible_coord[1]][soldier_possible_coord[0]] == 0)):
                    new_x = soldier_possible_coord[0]
                    new_y = soldier_possible_coord[1]
                    is_hit = False
                    break
                else:
                    is_hit = True

            #Defender.grid[y][x] = 0  # Clear old position
            self.grid[y][x] = 0
            #Defender.grid[new_y][new_x] = soldier['id']  # Update grid
            self.grid[new_y][new_x] = soldier['id']
            soldier['x'], soldier['y'] = new_x, new_y

        #call was_hit() to update the status of the soldier
        soldier_id = soldier['id']
        self.was_hit(soldier_id, is_hit)

    def print_layout(self, impact_area_coords):
        print(f"Time: {self.current_time}")
        
        # Print grid layout
        for y, row in enumerate(self.grid):
            row_str = ''
            for x, cell in enumerate(row):
                if cell == 0:
                    if (x, y) in impact_area_coords:
                        row_str += 'x\t'  # Red dot for impact area
                    else:
                        row_str += '.\t'  # Empty cell
                else:
                    row_str += f'{cell}\t'  # Soldier
            print(row_str)
        
        #for soldier in Defender.soldiers:
        for soldier in self.soldiers:
            print(f"Soldier {soldier['id']} - Status: {soldier['status']}")
        
    def simulate_battle(self, coord, type ):
        #self.initialize_soldiers()
        missile_type = type
        missile_x = coord[0]
        missile_y = coord[1]
        
        self.missile_approaching((missile_x, missile_y), self.current_time, missile_type)
        

        impact_area_coords = self.calculate_impact_area((missile_x, missile_y), missile_type)
        
        self.print_layout(impact_area_coords)

        self.status_all(self.soldiers)

        if(self.commander['status'] == 'Hit'):
            self.update_commander()
        
        # Check battle outcome
        self.casualty_count = self.M - len([s for s in self.soldiers if s['status'] == 'Alive'])
        print("Casualty count: " , self.casualty_count)
        print("Total", self.M)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    N = int(input("Enter battle field dimension: "))
    T = int(input("Total duration: "))
    battle_pb2_grpc.add_DefenderServicer_to_server(Defender(N, T), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started and listening on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()