from controllers.modules import *

class GetCarsHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, contentType")
        self.set_header('Access-Control-Allow-Methods', ' POST,OPTIONS')

    @coroutine
    def post(self):
        dt = car_contract_instance.getCars()
        dt = [list(map(str, i)) for i in dt]
        ret = []
        for i in range(len(dt[0])):
            ret.append({
                "id" : dt[0][i].replace("\u0000", ""),
                "name" : dt[1][i].replace("\u0000", ""),
                "model_no" : dt[2][i].replace("\u0000", ""),
                "vehicle_no" : dt[3][i].replace("\u0000", ""),
                "color" : dt[4][i].replace("\u0000", ""),
            })
        self.write({"code" : 200, "message" : "SuccessFull", "data" : ret})

    def options(self):
        set_status(204)
