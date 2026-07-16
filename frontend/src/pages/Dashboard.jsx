import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

import Navbar from "../components/Navbar";
import DashboardCards from "../components/DashboardCards";
import FileUpload from "../components/FileUpload";
import FilesTable from "../components/FilesTable";
import ScanResult from "../components/ScanResult";

import "../styles/dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [scanResult, setScanResult] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const res = await api.get("/files/");
      setFiles(res.data);
    } catch (err) {
      console.log(err);
    }
  };

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
    loadFiles();

  } catch (err) {
    console.log(err);

    if (err.response) {
      console.log("Status:", err.response.status);
      console.log("Response:", err.response.data);

      alert(JSON.stringify(err.response.data));
    } else {
      alert("Server not reachable");
    }
  }

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      await api.post("/files/upload", formData);

      alert("Upload Successful");

      setSelectedFile(null);

      loadFiles();
    } catch (err) {
      console.log(err);
    }
  };

  const scan = async (id) => {
    try {
      const res = await api.post(`/scan/${id}`);
      setScanResult(res.data);
      loadFiles();
    } catch (err) {
      console.log(err);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="dashboard">
      <div className="container">

        <Navbar logout={logout} />

        <DashboardCards files={files} />

        <FileUpload
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          uploadFile={upload}
        />

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