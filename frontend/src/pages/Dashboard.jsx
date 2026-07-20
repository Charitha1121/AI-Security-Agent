import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";
import Analytics from "../components/Analytics";
import Navbar from "../components/Navbar";
import DashboardCards from "../components/DashboardCards";
import FilesTable from "../components/FilesTable";
import Sidebar from "../components/Sidebar";

import "../styles/dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [files, setFiles] = useState([]);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const res = await api.get("/files/");

      console.log("Files Loaded:", res.data);

      setFiles(res.data);

    } catch (err) {
      console.error("Load Files Error:", err);

      if (err.response) {
        console.error("Request URL:", err.config?.url);
        console.error("Status:", err.response.status);
        console.error("Response:", err.response.data);
      }
    }
  };

  const scan = async (id) => {
    try {
      const res = await api.post(`/scan/${id}`);

      console.log("Scan Success:", res.data);

      await loadFiles();

      navigate(`/scan/${id}`);

    } catch (err) {
      console.error("Scan Error:", err);

      alert(
        err.response?.data?.detail ||
        "Scan failed"
      );
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="dashboard-layout">

      <Sidebar />

      <div className="main-content">

        <Navbar logout={logout} />

        <DashboardCards
          files={files}
        />

        <Analytics
          files={files}
        />

        <FilesTable
          files={files}
          scanFile={scan}
        />

      </div>

    </div>
  );
}