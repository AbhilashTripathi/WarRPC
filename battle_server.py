import grpc
import time
import random  # Import the random module
from concurrent import futures
import battle_pb2
import battle_pb2_grpc
from google.protobuf.empty_pb2 import Empty

class BattleService(battle_pb2_grpc.BattleServiceServicer):
    def __init__(self, max_workers):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
        battle_pb2_grpc.add_BattleServiceServicer_to_server(self, self.server)
        self.server.add_insecure_port('[::]:50051')

        # Initialize the soldiers dictionary with soldier IDs and initial data
        self.soldiers = {
            1: {
                "position": (10, 20),  # Replace with actual initial positions(x1, y1)
                "speed": 2,            # Replace with actual initial speed
                "hit": False           # Initialize hit status as False
            },
            2: {
                "position": (15, 25),  # Replace with actual initial positions(x2, y2)
                "speed": 3,            # Replace with actual initial speed
                "hit": False           # Initialize hit status as False
            },
            # Add more soldiers as needed
        }

    def was_soldier_hit(self, soldier_id):
        # Implement your logic to check if the soldier with the given ID was hit
        # This can involve checking the soldier's hit status or other criteria
        if soldier_id in self.soldiers:
            return self.soldiers[soldier_id]["hit"]
        else:
            return False  # Default to False if the soldier does not exist

    def start(self):
        self.server.start()
        print("Server started, listening on 50051")
        try:
            while True:
                time.sleep(86400)  # Keep server running
        except KeyboardInterrupt:
            self.server.stop(0)

    def MissileApproaching(self, request, context):
        # Handle missile approaching here
        print(f"Missile approaching: x={request.position_x}, y={request.position_y}, type={request.type}")

        # Simulate missile impact based on its type (red, blue, green, or yellow)
        # You can adjust the impact radius and soldier speed based on the missile type
        impact_radius = 0
        if request.type == "red":
            impact_radius = 5
        elif request.type == "blue":
            impact_radius = 3
        elif request.type == "green":
            impact_radius = 2
        elif request.type == "yellow":
            impact_radius = 1

        # Iterate through soldiers and check if they are in the impact zone
        for soldier_id, soldier in self.soldiers.items():
            x, y = soldier["position"]
            speed = soldier["speed"]

            # Calculate the distance from the soldier to the missile's impact point
            distance = ((x - request.position_x) ** 2 + (y - request.position_y) ** 2) ** 0.5

            # Determine if the soldier can move out of the impact zone in time
            if distance <= impact_radius * speed:
                # Soldier is in the impact zone and cannot escape in time
                print(f"Soldier {soldier_id} was hit by the missile!")
                # Perform any logic required when a soldier is hit
                # For example, you might mark the soldier as hit and update the leader

        # After handling missile impact, update the leader if needed
        # Implement your leader election logic here

        # For demonstration purposes, let's assume the leader remains the same for simplicity
        self.current_leader = random.choice(list(self.soldiers.keys()))

        # Return an Empty response
        return Empty()


    def Status(self, request, context):
        # Handle status query for a specific soldier
        soldier_id = request.soldier_id

        # Check if the soldier exists
        if soldier_id not in self.soldiers:
            context.set_details(f"Soldier {soldier_id} does not exist.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return battle_pb2.StatusResponse(was_hit=False)  # Return a response with 'was_hit' set to False

        # Check if the soldier was hit (implement your logic here)
        was_hit = self.was_soldier_hit(soldier_id)  # Implement the 'was_soldier_hit' function

        # Return a StatusResponse with the soldier's status
        response = battle_pb2.StatusResponse(was_hit=was_hit)
        return response


    def StatusAll(self, request, context):
        # Handle status query for all soldiers
        responses = []

        for soldier_id in self.soldiers:
            # Check if the soldier was hit (implement your logic here)
            was_hit = self.was_soldier_hit(soldier_id)  # Implement the 'was_soldier_hit' function

            # Create a StatusResponse for each soldier
            response = battle_pb2.StatusResponse(
                soldier_id=soldier_id,
                was_hit=was_hit
            )
            responses.append(response)

        # Return a StatusAllResponse with status for all soldiers
        status_all_response = battle_pb2.StatusAllResponse(responses=responses)
        return status_all_response


    def WasHit(self, request, context):
        # Handle notification of whether a soldier was hit
        soldier_id = request.soldier_id
        was_hit = request.trueFlag

        # Check if the soldier exists
        if soldier_id not in self.soldiers:
            context.set_details(f"Soldier {soldier_id} does not exist.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Empty()  # Return an Empty response

        # Update the soldier's hit status based on the notification
        self.soldiers[soldier_id]["hit"] = was_hit

        # Implement any additional logic you need when a soldier is hit
        if was_hit:
            print(f"Soldier {soldier_id} was hit by a missile!")
            # Perform additional actions or logic for a hit soldier

        return Empty()  # Return an Empty response


    def TakeShelter(self, request, context):
        # Handle request for a soldier to take shelter
        soldier_id = request.soldier_id

        # Check if the soldier exists
        if soldier_id not in self.soldiers:
            context.set_details(f"Soldier {soldier_id} does not exist.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return Empty()  # Return an Empty response

        # Get the soldier's current position
        current_position = self.soldiers[soldier_id]["position"]
        x, y = current_position

        # Implement logic to move the soldier to a safe location
        # This is a placeholder; replace it with your actual logic
        new_x, new_y = self.find_safe_location(x, y)

        # Update the soldier's position
        self.soldiers[soldier_id]["position"] = (new_x, new_y)

        # Return an Empty response to acknowledge the shelter request
        return Empty()


if __name__ == '__main__':
    max_workers = int(input("Enter the maximum number of worker threads: "))
    server = BattleService(max_workers)
    server.start()
