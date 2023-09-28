import random
import battle_pb2
import battle_pb2_grpc
import grpc
import time

print("Welcome to battle simulation!!")
Size = int(input("Enter battle field size (Enter value N for battlefield of size N X N): "))
Time = int(input("Enter duration of battle simulation (in seconds): "))
soldiers_count = casulty_count = 0

delay = int(input("Enter regular intervals at which missiles will be launched (in seconds): "))
missile_types_list = ['M1', 'M2', 'M3', 'M4']

with grpc.insecure_channel('localhost:50051') as channel:
        stub = battle_pb2_grpc.DefenderStub(channel)
        #Do check line 18 again!!
        soldiers_list = stub.InitializeSoldiers(battle_pb2.InitReq(N=Size, T=Time))
        soldiers = soldiers_list.sol_details
        #print(type(soldiers))
        soldiers_count = len(soldiers)
        #print(soldiers_count)
        
        while Time >= delay and casulty_count < soldiers_count / 2:
            random_missile = random.choice(missile_types_list)
            missile_x = random.randint(0, Size - 1)
            missile_y = random.randint(0, Size - 1)
            missile_notification = [delay, random_missile, missile_x, missile_y]
            tracking_details = stub.MissileApproaching(battle_pb2.MissileNotification(t=delay, x=missile_x, y=missile_y, missile_type=random_missile))
            casulty_count = tracking_details.casulty_count
            if casulty_count >= soldiers_count / 2:
                 print("Defender troop lost the war!! Hurray!!")
            else:
                 print("We lost the war :(") 
            time.sleep(delay)
            Time = Time - delay