import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";
import Sidebar from "./Sidebar";

import "../styles/upload-file.css";

export default function UploadFile() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    try {
      setLoading(true);
      setMessage("Uploading file...");

      const formData = new FormData();

      formData.append("file", file);

      // 1. Upload file
      const uploadResponse = await api.post(
        "/files/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const uploadedFile = uploadResponse.data;

      console.log(
        "Upload Success:",
        uploadedFile
      );

      setMessage("File uploaded. Scanning...");

      // 2. Automatically scan uploaded file
      const scanResponse = await api.post(
        `/scan/${uploadedFile.id}`
      );

      console.log(
        "Scan Success:",
        scanResponse.data
      );

      setMessage(
        "File uploaded and scanned successfully."
      );

      // 3. Redirect to scan report
      navigate(
        `/scan/${uploadedFile.id}`
      );

    } catch (error) {

      console.error(
        "Upload and Scan Error:",
        error
      );

      setMessage(
        error.response?.data?.detail ||
        "Upload or scanning failed."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-layout">

      <Sidebar />

      <main className="upload-page">

        <div className="upload-card">

          <h1>Upload File</h1>

          <p>
            Upload a file to automatically scan it
            for security threats.
          </p>

          <input
            type="file"
            onChange={(event) =>
              setFile(event.target.files[0])
            }
          />

          {file && (
            <p>
              Selected file: {file.name}
            </p>
          )}

          <button
            onClick={handleUpload}
            disabled={loading}
          >
            {loading
              ? "Uploading & Scanning..."
              : "Upload and Scan"}
          </button>

          {message && (
            <p>
              {message}
            </p>
          )}

        </div>

      </main>

    </div>
  );
}