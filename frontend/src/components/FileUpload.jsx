import "../styles/dashboard.css";
import { UploadCloud } from "lucide-react";

export default function FileUpload({
  selectedFile,
  setSelectedFile,
  uploadFile,
}) {
  return (
    <div className="section upload-section">

      <h2>
        <UploadCloud size={24} />
        Upload File
      </h2>

      <div className="upload-box">

        <input
          type="file"
          onChange={(e) => setSelectedFile(e.target.files[0])}
        />

        <button
          className="primary-btn"
          onClick={uploadFile}
        >
          Upload
        </button>

      </div>

      {selectedFile && (
        <p className="filename">
          Selected:
          <strong> {selectedFile.name}</strong>
        </p>
      )}

    </div>
  );
}