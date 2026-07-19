import { useState } from "react";
import {
  FileText,
  FileImage,
  FileSpreadsheet,
  Search,
} from "lucide-react";

import "../styles/dashboard.css";

export default function FilesTable({ files, scanFile }) {
  const [search, setSearch] = useState("");

  const filteredFiles = files.filter((file) =>
    file.filename.toLowerCase().includes(search.toLowerCase())
  );

  const getIcon = (type) => {
    if (type.includes("pdf")) return <FileText size={20} color="#ef4444" />;
    if (type.includes("image")) return <FileImage size={20} color="#22c55e" />;
    return <FileSpreadsheet size={20} color="#2563eb" />;
  };

  return (
    <div className="section">

      <div className="table-header">

        <h2>Uploaded Files</h2>

        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search file..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

      </div>

      <table>

        <thead>

          <tr>
            <th>File</th>
            <th>Type</th>
            <th>Status</th>
            <th>Uploaded</th>
            <th>Action</th>
          </tr>

        </thead>

        <tbody>

          {filteredFiles.map((file) => (

            <tr key={file.id}>

              <td className="filename-cell">
                {getIcon(file.file_type)}
                {file.filename}
              </td>

              <td>{file.file_type}</td>

              <td>
                <span className={`status ${file.scan_status}`}>
                  {file.scan_status}
                </span>
              </td>

              <td>
                {new Date(file.created_at).toLocaleDateString()}
              </td>

              <td>

                {file.scan_status === "completed" ? (

                  <button
                    className="completed-btn"
                    disabled
                  >
                    ✓ Completed
                  </button>

                ) : (

                  <button
                    className="scan-btn"
                    onClick={() => scanFile(file.id)}
                  >
                    Scan
                  </button>

                )}

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}