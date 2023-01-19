# HyperXite 8 Control System

The control system consists of the pod control backend and control station client.

## First-Time Setup

This project combines a React frontend with a Python backend.

### React Frontend

1. Install dependencies
   ```shell
   cd control-station
   npm ci
   ```

### Python Backend

1. Create a virtual environment

   ```shell
   python3 -m venv .venv --prompt hx8-control-system
   ```

2. Activate virtual environment

   VS Code may prompt to automatically select the newly created virtual environment. Otherwise, run

   ```shell
   source .venv/bin/activate
   ```

3. Install dependencies
   ```shell
   pip install -r requirements.txt -r requirements-dev.txt
   ```

## Running Development Environment

Run the React development server

```shell
cd control-station
npm run dev
```

Run the Python backend

```shell
cd pod-control
python3 src/main.py
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.
