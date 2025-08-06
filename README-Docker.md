# QAOA Portfolio Optimizer - Docker Deployment

This document provides instructions for running the QAOA Portfolio Optimizer API service using Docker.

## Prerequisites

- Docker (version 20.10+ recommended)
- Docker Compose (version 2.0+ recommended)
- CSV data files for portfolio optimization

## Quick Start

### 1. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 2. Build and Run with Docker Only

```bash
# Build the image
docker build -t qaoa-portfolio-optimizer .

# Run the container
docker run -p 9000:9000 qaoa-portfolio-optimizer
```

## Project Structure

```
.
├── api.py                      # Main Flask API application
├── portfolio_optimizer/        # Core optimization package
│   ├── data_loader.py          # Data loading utilities
│   ├── interface.py            # Main interface module
│   └── qaoa_solver.py          # QAOA quantum solver
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker build configuration
├── docker-compose.yml          # Docker Compose configuration
└── .dockerignore              # Docker ignore patterns
```

## API Endpoints

### Health Check
```
GET /health
```
Returns service health status.

### Portfolio Optimization
```
POST /optimize/today
Content-Type: multipart/form-data
```

**Request (Form Data):**
- `file`: CSV file containing stock price data
- `budget`: Integer - Number of stocks to select (e.g., 5)
- `depth`: Integer - QAOA circuit depth (e.g., 2)
- `grid`: Integer - Parameter grid search size (e.g., 3)
- `shots`: Integer - Number of quantum circuit shots (e.g., 1000)

**Response:**
```json
{
    "picks": ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"],
    "filename": "stock_data.csv",
    "parameters": {
        "budget": 5,
        "depth": 2,
        "grid": 3,
        "shots": 1000
    }
}
```

## Data Requirements

The service accepts CSV files uploaded directly through the API. No need to pre-configure data files.

### CSV Format
- Index: Date column (will be parsed as datetime)  
- Columns: Stock ticker symbols
- Values: Stock prices

### File Upload Constraints
- Maximum file size: 16MB
- Supported format: CSV only
- Files are processed temporarily and automatically cleaned up after processing

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |

## Docker Configuration Details

### Dockerfile Features
- Based on Python 3.10 slim image
- Installs system dependencies (gcc, g++, curl)
- Runs as non-root user for security
- Includes health check endpoint
- Optimized for production use

### Docker Compose Features
- Automatic restart policy
- Health check monitoring
- Network isolation
- Volume mounting for data files

## Testing the Service

### 1. Check Service Health
```bash
curl http://localhost:9000/health
```

### 2. Test Portfolio Optimization
```bash
# Test with file upload
curl -X POST http://localhost:9000/optimize/today \
  -F "file=@your_stock_data.csv" \
  -F "budget=5" \
  -F "depth=2" \
  -F "grid=3" \
  -F "shots=1000"
```

### 3. Alternative Test with HTML Form
Create a simple test HTML file:
```html
<!DOCTYPE html>
<html>
<head><title>QAOA Test</title></head>
<body>
    <form action="http://localhost:9000/optimize/today" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required><br>
        <input type="number" name="budget" placeholder="Budget (e.g., 5)" required><br>
        <input type="number" name="depth" placeholder="Depth (e.g., 2)" required><br>
        <input type="number" name="grid" placeholder="Grid (e.g., 3)" required><br>
        <input type="number" name="shots" placeholder="Shots (e.g., 1000)" required><br>
        <input type="submit" value="Optimize Portfolio">
    </form>
</body>
</html>
```

## Troubleshooting

### Container Health Issues
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs qaoa-api

# Check health
docker-compose exec qaoa-api curl http://localhost:9000/health
```

### Performance Considerations
- Increase `shots` parameter for better optimization quality (slower)
- Increase `grid` parameter for finer parameter search (slower)
- Increase `depth` parameter for deeper QAOA circuits (slower)

### Common Issues

1. **File Not Found**: Ensure CSV files are accessible in the container
2. **Memory Issues**: QAOA optimization can be memory-intensive for large portfolios
3. **Slow Response**: Quantum simulation is computationally expensive

## Stopping the Service

```bash
# With docker-compose
docker-compose down

# Remove volumes and images (complete cleanup)
docker-compose down -v --rmi all
```

## Security Notes

- The container runs as a non-root user
- Only port 9000 is exposed
- Network isolation through Docker networks
- Consider using HTTPS in production
- Validate input data before processing

## Production Deployment

For production deployment, consider:

1. Using environment-specific docker-compose files
2. Setting up reverse proxy (nginx, traefik)
3. Implementing authentication/authorization
4. Adding logging and monitoring
5. Using secrets management for sensitive configuration
6. Setting resource limits (CPU, memory)