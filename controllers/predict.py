from controllers.modules import *

__PERM__UPLOADS__ = "uploads/permanent/"
__TEMP__UPLOADS__ = "uploads/temp/"

class PredictHandler(RequestHandler):

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Access-Control-Allow-Origin, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, contentType")
        self.set_header('Access-Control-Allow-Methods', ' POST,OPTIONS')

    def upload(self, fileinfo):

        fname = fileinfo['filename']
        extn = splitext(fname)[1]
        cname = str(uuid.uuid4()) + extn
        fh = open(__TEMP__UPLOADS__ + cname, 'wb')
        fh.write(fileinfo['body'])
        fh.close()

        return {"status" : 200, "message" : "File Sucessfully Uploaded", "img_loc" : __TEMP__UPLOADS__ + cname}

    @coroutine
    def post(self):

        img_res = self.upload(self.request.files['cap_img'][0])

        dt = user_contract_instance.getUsers()
        dt = [list(map(str, i)) for i in dt]
        ret = {}
        # temp = {}
        for i in range(len(dt[0])):
            temp = {
                "uname" : dt[0][i].replace("\u0000", ""),
                "card_no" : dt[1][i].replace("\u0000", ""),
                "cvv" : dt[2][i].replace("\u0000", ""),
                "name" : dt[3][i].replace("\u0000", ""),
                "ph_no" : dt[4][i].replace("\u0000", ""),
                "photo" : __PERM__UPLOADS__ +  dt[0][i].replace("\u0000", "") + dt[5][i].replace("\u0000", "")
            }

            try:
                known_image = face_recognition.load_image_file(temp["photo"])
                unknown_image = face_recognition.load_image_file(img_res["img_loc"])

                known_encoding = face_recognition.face_encodings(known_image)[0]
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                score = 1 - face_recognition.face_distance([known_encoding], unknown_encoding)
                print(score[0])
                if score[0] > 0.47:
                    ret[score[0]] = temp

            except:
                self.write({"status" : 400, "message" : "No face in image", "valid_user_data" : None})

        if len(ret) > 0:
            fscore = max(ret.keys())
            ans = ret[fscore]
            self.write({"status" : 200, "message" : "Sucessfully Executed", "valid_user_data" : ans, "score" : fscore})

        else:
            self.write({"status" : 300, "message" : "No User Found", "valid_user_data" : None})

    def options(self):
        self.set_status(204)
