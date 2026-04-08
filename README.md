# Inventory App

A simple React Native app for managing invoices and projects.

## Features

- **Invoices:**  
  - Create, view, and delete invoices.
  - Mark invoices as paid.
  - Automatic status updates (pending, paid, overdue, draft).
  - Line items with quantity, unit, and rate.
  - GST (18%) calculation for supplier invoices.
  - Reconciliation with transactions.

- **Projects:**  
  - Assign invoices to projects.

- **UI:**  
  - Clean, modern interface.
  - Summary cards for totals, paid, pending, and overdue amounts.
  - Filtering by invoice status.
  - Modal forms for adding and viewing invoice details.

## Tech Stack

- **React Native** (with Expo)
- **TypeScript**
- **React Navigation**
- **Async Storage** (for local data persistence)
- **Python Backend** (optional, with FastAPI)

## Getting Started

### React Native App

1. **Clone the repository:**
   ```
   git clone <repo-url>
   cd inventory
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Start the app:**
   ```
   npx expo start
   ```

4. **Run on your device:**
   - Use the Expo Go app on your phone, or
   - Run on an emulator/simulator.

### Python Backend (Optional)

1. **Create and enter the backend folder:**
   ```
   mkdir backend
   cd backend
   ```

2. **Set up a virtual environment:**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install FastAPI and Uvicorn:**
   ```
   uv pip install fastapi uvicorn
   ```
4. install requirements.txt:
    uv pip install -r requirements.txt

4. **Create a simple FastAPI app in `main.py`:**
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"message": "Backend is running!"}
   ```

5. **Run the backend server:**
   ```
   uvicorn main:app --reload
   ```

6. **Access the API:**
   - [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Project Structure

- `/screens` — App screens (e.g., `InvoicesScreen.tsx`)
- `/components` — Reusable UI components
- `/lib` — Helpers, storage, types, and theme
- `/backend` — Python FastAPI backend (optional)

## Customization

- **Theme:**  
  Edit `/lib/theme.ts` for colors, spacing, and fonts.

- **Storage:**  
  Uses simple local storage. For production, integrate with a backend.

## License

MIT

---

*Built with ❤️ using React Native and Expo.*
