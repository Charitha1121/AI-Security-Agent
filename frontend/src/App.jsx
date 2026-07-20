import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ScanResult from "./components/ScanResult";
import ScanHistory from "./pages/ScanHistory";
import UploadPage from "./pages/UploadPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/upload"
          element={<UploadPage />}
        />

        <Route
          path="/scan/:fileId"
          element={<ScanResult />}
        />

        <Route
          path="/scan-history"
          element={<ScanHistory />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;