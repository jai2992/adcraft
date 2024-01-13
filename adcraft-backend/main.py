from inference import Adcraft
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from time import sleep

adcraft = Adcraft()
generate_args = reqparse.RequestParser()
generate_args.add_argument("brand", type=str, required=True)
generate_args.add_argument("slogan", type=str, required=True)
generate_args.add_argument("category", type=str, required=True)

app = Flask(__name__)
CORS(app)
api = Api(app=app)


class Hello(Resource):
    def get(self):
        return {"message": "Hello World"}


class Generate(Resource):
    def post(self):
        args = generate_args.parse_args()
        adcraft.generate_image(args.get("category"))
        sleep(1)
        adcraft.add_text_to_image(args.get("brand"), args.get("slogan"))
        return args


api.add_resource(Hello, "/")
api.add_resource(Generate, "/gen")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
