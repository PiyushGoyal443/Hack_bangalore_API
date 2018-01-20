from controllers.modules import *

__PERM__UPLOADS__ = "uploads/permanent/"

class AddUserHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, contentType")
        self.set_header('Access-Control-Allow-Methods', ' POST,OPTIONS')

    def upload(self, fileinfo, uname):

        fname = fileinfo['filename']
        extn = splitext(fname)[1]
        cname = uname + extn
        fh = open(__PERM__UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()

        return {"status" : 200, "message" : "File Sucessfully Uploaded", "img_loc" : __PERM__UPLOADS__ + cname, "ext" : extn}

    @coroutine
    def post(self):

        name = self.get_argument("name")
        uname = self.get_argument("uname")
        card_no = self.get_argument("card_no")
        exp_date = self.get_argument("exp_date", "")
        cvv = self.get_argument("cvv")
        ph_no = self.get_argument("ph_no")
        img_link = self.upload(self.request.files['image'][0], uname)

        user_contract_instance.addUser(uname, card_no, cvv, name, ph_no, img_link["ext"], transact={'from': acc[1]})
        self.write({"status" : 200, "message" : "Sucessfully Added"})

    def options(self):
        set_status(204)
