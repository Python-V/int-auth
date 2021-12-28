import grpc
import sys
sys.path.append("..")
sys.path.append("../..")

from libs import verification_pb2_grpc as grpcpb
from libs import verification_pb2 as pb
from concurrent import futures

from sql_connector import Connect
from datetime import datetime

db = Connect()

class ValidationService(grpcpb.Auth):
    def get_access_token(self, token):
        cursor = db.conn.cursor()
        cursor.execute('''SELECT * from provider_accesstoken WHERE token=%s and invalid=%s;''', (token, False))
        result = cursor.fetchone()
        print(result)
        return result


    def ValidateToken(self, request, target):
        access_token = request.bearer
        if not access_token:
            return pb.TokenValidatorResponse(
                msg= 'Token missing',
                success= False
            )
        try:
            user_access_token = self.get_access_token(access_token)
            # user_id = user_access_token.user_id
            # print("user_id", user_id)
            # need to check user permissions too
            if not user_access_token:
                return pb.TokenValidatorResponse(
                    msg= 'Invalid Token',
                    success= False
                )
            return pb.TokenValidatorResponse(
                msg= 'Token valid',
                success= True
            )
        except Exception as e:
            print(e)
            return pb.TokenValidatorResponse(
                msg= 'Invalid Token',
                success= False
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcpb.add_AuthServicer_to_server(ValidationService(), server)
    server.add_insecure_port("[::]:50051")
    print("Starting server at: 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
    db.conn.Close()