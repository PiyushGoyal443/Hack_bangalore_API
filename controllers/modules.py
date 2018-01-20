"""
module to import all necessary modules
"""

# tornado modules
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options
from tornado.escape import json_encode, json_decode
from tornado.web import RequestHandler, Application, removeslash

import json
import web3

from os.path import join, dirname, isfile, splitext

from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

# other modules
import uuid
import requests
import face_recognition
from os.path import join, dirname, isfile, splitext

from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

from collections import defaultdict

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

cid_global = 1

car_contract_code = """
    pragma solidity ^0.4.0;

    contract CarContract {

      Car[] public cars;

      struct Car {
        bytes32 carID;
        bytes32 name;
        bytes32 model_no;
        bytes32 vehicle_no;
        bytes32 color;
      }

      function addCar(bytes32 _carID, bytes32 _name, bytes32 _model_no, bytes32 _vehicle_no, bytes32 _color) public returns (bool success) {
        Car memory newCar;

        newCar.carID = _carID;
        newCar.name = _name;
        newCar.model_no = _model_no;
        newCar.vehicle_no = _vehicle_no;
        newCar.color = _color;

        cars.push(newCar);

        return true;
      }

      function getLength() public constant returns (uint) {
        return cars.length;
      }

      function getCars() public constant returns (bytes32[] , bytes32[], bytes32[], bytes32[], bytes32[]) {

        uint length = cars.length;

        bytes32[] memory _carIDs = new bytes32[](length);
        bytes32[] memory _names = new bytes32[](length);
        bytes32[] memory _model_nos = new bytes32[](length);
        bytes32[] memory _vehicle_nos = new bytes32[](length);
        bytes32[] memory _colors = new bytes32[](length);

        for(uint i = 0; i < length; i++) {
          Car memory currentCar;

          currentCar = cars[i];

          _carIDs[i] = currentCar.carID;
          _names[i] = currentCar.name;
          _model_nos[i] = currentCar.model_no;
          _vehicle_nos[i] = currentCar.vehicle_no;
          _colors[i] = currentCar.color;

        }

        return (_carIDs, _names, _model_nos, _vehicle_nos, _colors);
      }
    }
    """

user_contract_code = """
    pragma solidity ^0.4.0;

    contract UserContract {

      User[] public users;

      struct User {
        bytes32 uname;
        bytes32 card_no;
        bytes32 cvv;
        bytes32 name;
        bytes32 phno;
        bytes32 img_ext;
      }

      function addUser(bytes32 _uname, bytes32 _card_no, bytes32 _cvv, bytes32 _name, bytes32 _phno, bytes32 _img_ext) public returns (bool success) {
        User memory newUser;
        newUser.uname = _uname;
        newUser.card_no = _card_no;
        newUser.cvv = _cvv;
        newUser.name = _name;
        newUser.phno = _phno;
        newUser.img_ext = _img_ext;

        users.push(newUser);

        return true;
      }

      function getUsers() public constant returns (bytes32[], bytes32[], bytes32[], bytes32[], bytes32[], bytes32[]) {

        uint length = users.length;
        bytes32[] memory _unames = new bytes32[](length);
        bytes32[] memory _card_nos = new bytes32[](length);
        bytes32[] memory _cvvs = new bytes32[](length);
        bytes32[] memory _names = new bytes32[](length);
        bytes32[] memory _phnos = new bytes32[](length);
        bytes32[] memory _img_exts = new bytes32[](length);

        for(uint i = 0; i < length; i++) {
          User memory currentUser;

          currentUser = users[i];

          _unames[i] = currentUser.uname;
          _card_nos[i] = currentUser.card_no;
          _cvvs[i] = currentUser.cvv;
          _names[i] = currentUser.name;
          _phnos[i] = currentUser.phno;
          _img_exts[i] = currentUser.img_ext;

        }

        return (_unames, _card_nos, _cvvs, _names, _phnos, _img_exts);
      }
    }

    """

car_compiled_sol = compile_source(car_contract_code)
car_contract_interface = car_compiled_sol['<stdin>:CarContract']

# web3.py instance
w3 = Web3(TestRPCProvider())

# Instantiate and deploy contract
car_contract = w3.eth.contract(abi=car_contract_interface['abi'], bytecode=car_contract_interface['bin'])

# Get transaction hash from deployed contract
acc = w3.eth.accounts
car_tx_hash = car_contract.deploy(transaction={'from': acc[0]})

# Get tx receipt to get contract address
car_tx_receipt = w3.eth.getTransactionReceipt(car_tx_hash)
car_contract_address = car_tx_receipt['contractAddress']

# Contract instance in concise mode
car_contract_instance = w3.eth.contract(car_contract_interface['abi'], car_contract_address, ContractFactoryClass=ConciseContract)

user_compiled_sol = compile_source(user_contract_code)
user_contract_interface = user_compiled_sol['<stdin>:UserContract']

# Instantiate and deploy contract
user_contract = w3.eth.contract(abi=user_contract_interface['abi'], bytecode=user_contract_interface['bin'])

# Get transaction hash from deployed contract
user_tx_hash = user_contract.deploy(transaction={'from': acc[1]})

# Get tx receipt to get contract address
user_tx_receipt = w3.eth.getTransactionReceipt(user_tx_hash)
user_contract_address = user_tx_receipt['contractAddress']

# Contract instance in concise mode
user_contract_instance = w3.eth.contract(user_contract_interface['abi'], user_contract_address, ContractFactoryClass=ConciseContract)
