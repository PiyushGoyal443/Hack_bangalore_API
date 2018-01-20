from controllers.modules import *

class AddCarHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, contentType")
        self.set_header('Access-Control-Allow-Methods', ' POST,OPTIONS')

    @coroutine
    def post(self):
        global cid_global
        cid = str(cid_global)
        cid_global += 1
        name = self.get_argument("name")
        model_no = self.get_argument("model_no")
        car_no = self.get_argument("car_no")
        color = self.get_argument("color")

        car_contract_instance.addCar(cid, name, model_no, car_no, color, transact={'from': acc[0]})
        self.write({"status" : 200, "message" : "Sucessfully Added"})

    def options(self):
        set_status(204)
