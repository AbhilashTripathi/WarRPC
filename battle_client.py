import grpc
import battle_pb2
import battle_pb2_grpc

def notify_missile(position_x, position_y, time, missile_type):
    channel = grpc.insecure_channel('localhost:50051')
    stub = battle_pb2_grpc.BattleServiceStub(channel)
    request = battle_pb2.MissileNotification(
        position_x=position_x,
        position_y=position_y,
        time=time,
        type=missile_type
    )
    response = stub.MissileApproaching(request)
    print("Missile notification sent")

def query_status(soldier_id):
    channel = grpc.insecure_channel('localhost:50051')
    stub = battle_pb2_grpc.BattleServiceStub(channel)
    request = battle_pb2.StatusRequest(soldier_id=soldier_id)
    response = stub.Status(request)
    print(f"Soldier {soldier_id} status: Was hit: {response.was_hit}")

if __name__ == '__main__':
    max_workers = int(input("Enter the maximum number of worker threads for the server: "))
    
    # Example usage: Notify missile and query status
    notify_missile(10, 20, 5, "red")
    query_status(1)
