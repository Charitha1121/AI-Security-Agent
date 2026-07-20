import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import api from "../api/api";
import Sidebar from "./Sidebar";

import "../styles/scan-result.css";

export default function ScanResult({ scan: dashboardScan }) {
  const { fileId } = useParams();

  const [scan, setScan] = useState(
    dashboardScan || null
  );

  const [loading, setLoading] = useState(
    !dashboardScan
  );

  const [error, setError] = useState("");

  useEffect(() => {
    if (!dashboardScan && fileId) {
      loadScanResult();
    }
  }, [fileId, dashboardScan]);

  const loadScanResult = async () => {
    try {
      setLoading(true);
      setError("");

      console.log(
        "Request URL:",
        `/scan/${fileId}`
      );

      const response = await api.get(
        `/scan/${fileId}`
      );

      console.log(
        "Loaded Scan Result:",
        response.data
      );

      setScan(response.data);

    } catch (err) {
      console.error(
        "Load Scan Result Error:",
        err
      );

      console.error(
        "Status:",
        err.response?.status
      );

      console.error(
        "Response:",
        err.response?.data
      );

      setError(
        err.response?.data?.detail ||
        "Failed to load scan result"
      );

    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="app-layout">

        <Sidebar />

        <main className="scan-result-page">

          <h1>
            Loading Scan Report...
          </h1>

        </main>

      </div>
    );
  }

  if (error) {
    return (
      <div className="app-layout">

        <Sidebar />

        <main className="scan-result-page">

          <h1>
            Scan Report
          </h1>

          <p className="history-error">
            {error}
          </p>

        </main>

      </div>
    );
  }

  if (!scan) {
    return (
      <div className="app-layout">

        <Sidebar />

        <main className="scan-result-page">

          <h1>
            No scan result found
          </h1>

        </main>

      </div>
    );
  }

  return (
    <div className="app-layout">

      <Sidebar />

      <main className="scan-result-page">

        <div className="scan-result-header">

          <h1>
            Security Scan Report
          </h1>

          <p>
            Detailed analysis of the scanned file
          </p>

        </div>

        <div className="scan-overview">

          <div className="result-card">

            <h3>
              Risk Score
            </h3>

            <div className="risk-score-large">

              {scan.risk_score}%

            </div>

          </div>

          <div className="result-card">

            <h3>
              Verdict
            </h3>

            <div className="verdict-large">

              {scan.verdict}

            </div>

          </div>

        </div>

        <div className="result-section">

          <h2>
            AI Threat Summary
          </h2>

          <p>

            {scan.ai_summary ||
              "No AI summary available."}

          </p>

        </div>

        <div className="result-section">

          <h2>
            Detection Analysis
          </h2>

          <div className="detection-grid">

            <div>
              <strong>
                Emails
              </strong>

              <span>
                {scan.detected_emails?.length || 0}
              </span>
            </div>

            <div>
              <strong>
                URLs
              </strong>

              <span>
                {scan.detected_urls?.length || 0}
              </span>
            </div>

            <div>
              <strong>
                Secrets
              </strong>

              <span>
                {scan.detected_secrets?.length || 0}
              </span>
            </div>

            <div>
              <strong>
                Phones
              </strong>

              <span>
                {scan.detected_phones?.length || 0}
              </span>
            </div>

            <div>
              <strong>
                IP Addresses
              </strong>

              <span>
                {scan.detected_ips?.length || 0}
              </span>
            </div>

          </div>

        </div>

        <div className="result-section">

          <h2>
            Detected Keywords
          </h2>

          {scan.detected_keywords?.length > 0 ? (

            <ul>

              {scan.detected_keywords.map(
                (keyword, index) => (

                  <li key={index}>
                    {keyword}
                  </li>

                )
              )}

            </ul>

          ) : (

            <p>
              No suspicious keywords detected.
            </p>

          )}

        </div>

        <div className="result-section">

          <h2>
            Detected URLs
          </h2>

          {scan.detected_urls?.length > 0 ? (

            <ul>

              {scan.detected_urls.map(
                (url, index) => (

                  <li key={index}>
                    {url}
                  </li>

                )
              )}

            </ul>

          ) : (

            <p>
              No URLs detected.
            </p>

          )}

        </div>

      </main>

    </div>
  );
}