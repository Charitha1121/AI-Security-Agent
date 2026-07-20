import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";
import "../styles/upload-file.css";

export default function UploadPage() {
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first.");
      return;
    }

    try {
      setUploading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", selectedFile);

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

      console.log("Upload successful:", uploadedFile);

      // 2. Immediately scan uploaded file
      const scanResponse = await api.post(
        `/scan/${uploadedFile.id}`
      );

      console.log("Scan successful:", scanResponse.data);

      // 3. Open scan report
      navigate(`/scan/${uploadedFile.id}`);

    } catch (err) {
      console.error("Upload/Scan Error:", err);

      setError(
        err.response?.data?.detail ||
        "Upload or scanning failed."
      );

    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-page">

      <div className="upload-card">

        <h1>Upload File</h1>

        <p className="upload-description">
          Upload a file to scan it for security threats,
          sensitive information, and malicious content.
        </p>

        <label className="file-drop-area">

          <input
            type="file"
            onChange={(e) =>
              setSelectedFile(e.target.files[0])
            }
          />

          <div className="upload-icon">
            ⬆
          </div>

          <strong>
            {selectedFile
              ? selectedFile.name
              : "Choose a file to upload"}
          </strong>

          <span>
            Supported documents, images, videos, audio,
            archives, and more
          </span>

        </label>

        {selectedFile && (
          <div className="selected-file">
            <span>{selectedFile.name}</span>

            <button
              onClick={() => setSelectedFile(null)}
            >
              Remove
            </button>
          </div>
        )}

        {error && (
          <div className="upload-error">
            {error}
          </div>
        )}

        <button
          className="upload-button"
          onClick={handleUpload}
          disabled={uploading}
        >
          {uploading
            ? "Uploading and Scanning..."
            : "Upload & Scan"}
        </button>

      </div>

    </div>
  );
}