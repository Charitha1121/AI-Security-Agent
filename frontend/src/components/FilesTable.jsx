import "../styles/dashboard.css";
import { ScanSearch } from "lucide-react";

export default function FilesTable({
  files,
  scanFile,
}) {
  return (
    <div className="section">

      <h2>Uploaded Files</h2>

      <table>

        <thead>

          <tr>
            <th>Filename</th>
            <th>Type</th>
            <th>Status</th>
            <th>Action</th>
          </tr>

        </thead>

        <tbody>

          {files.map((file) => (

            <tr key={file.id}>

              <td>{file.filename}</td>

              <td>{file.file_type}</td>

              <td>

                <span
                  className={`status ${file.scan_status}`}
                >
                  {file.scan_status}
                </span>

              </td>

              <td>

                <button
                  className="scan-btn"
                  onClick={() => scanFile(file.id)}
                >
                  <ScanSearch size={16} />
                  Scan
                </button>

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}