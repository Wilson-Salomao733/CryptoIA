from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
import os
from dotenv import load_dotenv

# Import our services
from services.data_processor import DataProcessor
from services.ml_service import MLService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React Native
api = Api(app)

# Initialize services
data_processor = DataProcessor()
ml_service = MLService()

class HealthCheck(Resource):
    def get(self):
        return {"status": "healthy", "message": "Python backend is running!"}

class ProcessData(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400
            
            processed_data = data_processor.process(data)
            return {"success": True, "result": processed_data}
        except Exception as e:
            return {"error": str(e)}, 500

class PredictData(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'features' not in data:
                return {"error": "Features are required"}, 400
            
            prediction = ml_service.predict(data['features'])
            return {"success": True, "prediction": prediction}
        except Exception as e:
            return {"error": str(e)}, 500

class UserData(Resource):
    def get(self):
        # Sample user data endpoint
        users = [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
        ]
        return {"users": users}
    
    def post(self):
        data = request.get_json()
        # In a real app, you'd save to a database
        return {"success": True, "message": "User created", "user": data}, 201

# Register API routes
api.add_resource(HealthCheck, '/api/health')
api.add_resource(ProcessData, '/api/process')
api.add_resource(PredictData, '/api/predict')
api.add_resource(UserData, '/api/users')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
