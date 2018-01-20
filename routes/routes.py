"""
module to storing all the routes
"""

from controllers import *

routes = [
    (
        r"/add/car",
        addcar.AddCarHandler
    ),
    (
        r"/get/cars",
        getcars.GetCarsHandler
    ),
    (
        r"/add/user",
        adduser.AddUserHandler
    ),
    (
        r"/get/users",
        getusers.GetUsersHandler
    ),
    (
        r"/predict",
        predict.PredictHandler
    )
]
