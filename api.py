from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError
from werkzeug.utils import secure_filename
import os
import tempfile
from portfolio_optimizer.interface import optimize_today

class OptimizeTodaySchema(Schema):
    budget = fields.Int(required=True)
    depth = fields.Int(required=True)
    grid = fields.Int(required=True)
    shots = fields.Int(required=True)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "QAOA Portfolio Optimizer"}), 200

    @app.route('/optimize/today', methods=['POST'])
    def optimize_today_endpoint():
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed. Only CSV files are supported."}), 400

        # Get form data for other parameters
        try:
            budget = int(request.form.get('budget'))
            depth = int(request.form.get('depth'))
            grid = int(request.form.get('grid'))
            shots = int(request.form.get('shots'))
        except (TypeError, ValueError) as e:
            return jsonify({"error": "Invalid parameter values. All parameters must be integers."}), 400

        # Validate parameters using schema
        schema = OptimizeTodaySchema()
        try:
            data = schema.load({
                'budget': budget,
                'depth': depth,
                'grid': grid,
                'shots': shots
            })
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400

        try:
            # Save the uploaded file temporarily
            filename = secure_filename(file.filename)
            
            # Use temporary file to ensure cleanup
            with tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False) as temp_file:
                file.save(temp_file.name)
                temp_path = temp_file.name
            
            try:
                # Process the file
                picks = optimize_today(
                    path=temp_path,
                    budget=data["budget"],
                    depth=data["depth"],
                    grid=data["grid"],
                    shots=data["shots"]
                )
                return jsonify({
                    "picks": picks,
                    "filename": filename,
                    "parameters": {
                        "budget": data["budget"],
                        "depth": data["depth"],
                        "grid": data["grid"],
                        "shots": data["shots"]
                    }
                })
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=9000, debug=True)
