import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";
import Analytics from "../components/Analytics";
import Navbar from "../components/Navbar";
import DashboardCards from "../components/DashboardCards";
import FileUpload from "../components/FileUpload";
import FilesTable from "../components/FilesTable";
import ScanResult from "../components/ScanResult";
import Sidebar from "../components/Sidebar";

import "../styles/dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [scanResult, setScanResult] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  // =========================
  // LOAD FILES
  // =========================
  const loadFiles = async () => {
    try {
      const res = await api.get("/files/");
      setFiles(res.data);
    } catch (err) {
      console.error("Load Files Error:", err);

      if (err.response) {
        console.error("Status:", err.response.status);
        console.error("Response:", err.response.data);
      }
    }
  };

  // =========================
  // UPLOAD FILE
  // =========================
  const upload = async () => {
    if (!selectedFile) {
      alert("Please select a file");
      return;
    }

    try {
      const formData = new FormData();

      formData.append("file", selectedFile);

      const res = await api.post("/files/upload", formData);

      console.log("Upload Success:", res.data);

      alert("Upload Successful");

      setSelectedFile(null);

      await loadFiles();

    } catch (err) {
      console.error("Upload Error:", err);

      if (err.response) {
        console.error("Status:", err.response.status);
        console.error("Response:", err.response.data);

        alert(
          err.response.data?.detail ||
          "File upload failed"
        );
      } else {
        alert("Server not reachable");
      }
    }
  };

  // =========================
  // SCAN FILE
  // =========================
 const scan = async (id) => {
  try {
    const res = await api.post(`/${id}`);

    console.log("Scan Success:", res.data);

    setScanResult(res.data);

    await loadFiles();

  } catch (err) {
    console.error("Scan Error:", err);

    if (err.response) {
      console.error("Status:", err.response.status);
      console.error("Response:", err.response.data);

      alert(
        err.response.data?.detail ||
        "Scan failed"
      );
    } else {
      alert("Server not reachable");
    }
  }
};
  // =========================
  // LOGOUT
  // =========================
  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="dashboard-layout">

      <Sidebar />

      <div className="main-content">

        <Navbar logout={logout} />

        <DashboardCards files={files} />

        <FileUpload
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          uploadFile={upload}
        />

        <Analytics files={files} />

        <FilesTable
          files={files}
          scanFile={scan}
        />

        {scanResult && (
          <ScanResult scan={scanResult} />
        )}

      </div>

    </div>
  );
}