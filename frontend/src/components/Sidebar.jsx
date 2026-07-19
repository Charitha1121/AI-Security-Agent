import {
  Shield,
  LayoutDashboard,
  Upload,
  History,
  Settings,
} from "lucide-react";

import { useNavigate, useLocation } from "react-router-dom";

import "../styles/sidebar.css";

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="sidebar">

      <div className="logo">
        <Shield size={32} />
        <h2>AI Security</h2>
      </div>

      <ul>

        <li
          className={location.pathname === "/dashboard" ? "active" : ""}
          onClick={() => navigate("/dashboard")}
        >
          <LayoutDashboard size={20} />
          Dashboard
        </li>

        <li
          className={location.pathname === "/upload" ? "active" : ""}
          onClick={() => navigate("/upload")}
        >
          <Upload size={20} />
          Upload Files
        </li>

        <li
          className={location.pathname === "/scan-history" ? "active" : ""}
          onClick={() => navigate("/scan-history")}
        >
          <History size={20} />
          Scan History
        </li>

        <li
          className={location.pathname === "/settings" ? "active" : ""}
          onClick={() => navigate("/settings")}
        >
          <Settings size={20} />
          Settings
        </li>

      </ul>

    </div>
  );
}