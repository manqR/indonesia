from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

auth = HTTPBasicAuth()
mysql = MySQL()

users = {
     "demo": "demo123",
}

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'userDB'
app.config['MYSQL_DATABASE_PASSWORD'] = 'passwordDB'
app.config['MYSQL_DATABASE_DB'] = 'mysqlDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)
api = Api(app)

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


class GetAllProvince(Resource):
    
    @auth.login_required
 
    def post(self):
        try:         
            conn = mysql.connect()
            cursor = conn.cursor()
        
            query_string = "SELECT * FROM provinces"
            cursor.execute(query_string)

            return jsonify(data=cursor.fetchall())

            # data = cursor.fetchall()

            # items_list=[]
            # for item in data:
            #     i = {
            #         'Id':item[0],
            #         'Name':item[1]
            #     }
            #     items_list.append(i)

            # return {'StatusCode':'200','Items':items_list}

        except Exception as e:
            return {'error': str(e)}
    


class GetRegencies(Resource):
    @auth.login_required
    def post(self):
        try:         
            conn = mysql.connect()
            cursor = conn.cursor()

            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            args = parser.parse_args()
            _province_id = args['id']

            query_string = "SELECT * FROM regencies  WHERE province_id = %s"
            cursor.execute(query_string, (_province_id))

            return jsonify(data=cursor.fetchall())
          

        except Exception as e:
            return {'error': str(e)}
    
    
class GetDistrict(Resource):
    @auth.login_required
    def post(self):
        try:         
            conn = mysql.connect()
            cursor = conn.cursor()

            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            args = parser.parse_args()
            _regency_id = args['id']

            query_string = "SELECT * FROM districts  WHERE regency_id = %s"
            cursor.execute(query_string, (_regency_id))

            return jsonify(data=cursor.fetchall())
          

        except Exception as e:
            return {'error': str(e)}
    
    
class GetVillage(Resource):
    @auth.login_required
    def post(self):
        try:         
            conn = mysql.connect()
            cursor = conn.cursor()

            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            args = parser.parse_args()
            _district_id = args['id']

            query_string = "SELECT * FROM villages  WHERE district_id = %s"
            cursor.execute(query_string, (_district_id))

            return jsonify(data=cursor.fetchall())
          

        except Exception as e:
            return {'error': str(e)}


api.add_resource(GetAllProvince, '/GetAllProvince')
api.add_resource(GetRegencies, '/GetRegencies')
api.add_resource(GetDistrict, '/GetDistrict')
api.add_resource(GetVillage, '/GetVillage')

if __name__ == '__main__':
    app.run(host='flask.shoper.co.id', port=8080, debug=None, load_dotenv=True)
