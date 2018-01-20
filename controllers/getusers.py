from controllers.modules import *

__PERM__UPLOADS__ = "uploads/permanent/"

class GetUsersHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, contentType")
        self.set_header('Access-Control-Allow-Methods', ' POST,OPTIONS')

    @coroutine
    def post(self):
        dt = user_contract_instance.getUsers()
        dt = [list(map(str, i)) for i in dt]
        ret = []
        for i in range(len(dt[0])):
            ret.append({
                "uname" : dt[0][i].replace("\u0000", ""),
                "card_no" : dt[1][i].replace("\u0000", ""),
                "cvv" : dt[2][i].replace("\u0000", ""),
                "name" : dt[3][i].replace("\u0000", ""),
                "ph_no" : dt[4][i].replace("\u0000", ""),
                "photo" : __PERM__UPLOADS__ +  dt[0][i].replace("\u0000", "") + dt[5][i].replace("\u0000", "")
            })
        self.write({"code" : 200, "message" : "SuccessFull", "data" : ret})

    def options(self):
        set_status(204)
