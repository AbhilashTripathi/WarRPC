import random
import battle_pb2
import battle_pb2_grpc
import grpc
import time
#import asyncio
#import grpc.aio 

print("Welcome to battle simulation!!")
Size = int(input("Enter battle field size (Enter value N for battlefield of size N X N): "))
Time = int(input("Enter duration of battle simulation (in seconds): "))
soldiers_count = casualty_count = 0

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
     
     
     while Time >= delay or casualty_count < soldiers_count / 2:
         flag = 0
         random_missile = random.choice(missile_types_list)
         missile_x = random.randint(0, Size - 1)
         missile_y = random.randint(0, Size - 1)
         missile_notification = [delay, random_missile, missile_x, missile_y]
         print(f"Missile ({random_missile}) Launching at ({missile_y}, {missile_x})")
         tracking_details = stub.MissileApproaching(battle_pb2.MissileNotification(t=delay, x=missile_x, y=missile_y, missile_type=random_missile))
         casualty_count = tracking_details.casualty_count
         print("Casualty count: ", casualty_count)
         Time = Time - delay
         print("Time left: ", Time)
         time.sleep(delay)
         if casualty_count >= soldiers_count / 2:
              flag = 1
              #we won as an attacker
              print("We won the war!! Hurray!!")
              break
         if(Time <= 0): break
     
     #we lost as an attacker
     if(flag == 0): print("We lost the war :( ")