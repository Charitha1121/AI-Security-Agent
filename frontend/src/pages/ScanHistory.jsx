import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import "../styles/scan-history.css";

const API_URL = "http://127.0.0.1:8000";

export default function ScanHistory() {
  const navigate = useNavigate();

  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchScanHistory();
  }, []);

  const fetchScanHistory = async () => {
    try {
      setLoading(true);
      setError("");

      const token = localStorage.getItem("token");

      if (!token) {
        throw new Error("Authentication token not found");
      }

      const response = await fetch(
        `${API_URL}/api/v1/scan/history`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        const errorData =
          await response.json().catch(() => null);

        console.error(
          "Scan history API error:",
          response.status,
          errorData
        );

        throw new Error(
          errorData?.detail ||
            "Failed to load scan history"
        );
      }

      const data = await response.json();

      console.log("Scan History:", data);

      setScans(data);

    } catch (error) {
      console.error(
        "Scan History Error:",
        error
      );

      setError(
        error.message ||
          "Unable to load scan history"
      );

    } finally {
      setLoading(false);
    }
  };

  const getRiskClass = (score) => {
    if (score >= 70) return "high-risk";
    if (score >= 30) return "warning-risk";
    return "safe-risk";
  };

  return (
    <div className="app-layout">

      <Sidebar />

      <main className="history-page">

        <div className="history-header">

          <h1>Scan History</h1>

          <p>
            View all your previous security scans
          </p>

        </div>

        {loading && (
          <div className="history-message">
            Loading scan history...
          </div>
        )}

        {error && (
          <div className="history-error">
            {error}
          </div>
        )}

        {!loading &&
          !error &&
          scans.length === 0 && (

            <div className="history-message">
              No scan history found.
            </div>

          )}

        {!loading &&
          !error &&
          scans.length > 0 && (

            <div className="history-table-container">

              <table className="history-table">

                <thead>

                  <tr>

                    <th>File ID</th>

                    <th>Risk Score</th>

                    <th>Verdict</th>

                    <th>Emails</th>

                    <th>URLs</th>

                    <th>Secrets</th>

                    <th>Scanned On</th>

                    <th>Action</th>

                  </tr>

                </thead>

                <tbody>

                  {scans.map((scan) => (

                    <tr key={scan.id}>

                      <td>

                        {scan.file_id
                          ? `${scan.file_id.slice(
                              0,
                              8
                            )}...`
                          : "N/A"}

                      </td>

                      <td>

                        <span
                          className={`risk-score ${getRiskClass(
                            scan.risk_score
                          )}`}
                        >

                          {scan.risk_score}%

                        </span>

                      </td>

                      <td>

                        <span
                          className={`verdict ${getRiskClass(
                            scan.risk_score
                          )}`}
                        >

                          {scan.verdict}

                        </span>

                      </td>

                      <td>

                        {scan.detected_emails
                          ?.length || 0}

                      </td>

                      <td>

                        {scan.detected_urls
                          ?.length || 0}

                      </td>

                      <td>

                        {scan.detected_secrets
                          ?.length || 0}

                      </td>

                      <td>

                        {scan.created_at
                          ? new Date(
                              scan.created_at
                            ).toLocaleDateString()
                          : "N/A"}

                      </td>

                      <td>

                        <button
                          className="view-scan-button"
                          onClick={() =>
                            navigate(
                              `/scan/${scan.file_id}`
                            )
                          }
                        >

                          View Report

                        </button>

                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

      </main>

    </div>
  );
}