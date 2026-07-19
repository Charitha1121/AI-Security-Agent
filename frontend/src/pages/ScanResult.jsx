import "../styles/dashboard.css";
import "react-circular-progressbar/dist/styles.css";
import {
  CircularProgressbar,
  buildStyles,
} from "react-circular-progressbar";

export default function ScanResult({ scan }) {

  const riskColor =
    scan.risk_score > 70
      ? "#ef4444"
      : scan.risk_score > 40
      ? "#f59e0b"
      : "#22c55e";

  return (

    <div className="section">

      <h2>🛡 AI Scan Report</h2>

      <div className="scan-layout">

        <div className="gauge-card">

          <CircularProgressbar
            value={scan.risk_score}
            text={`${scan.risk_score}%`}
            styles={buildStyles({
              pathColor: riskColor,
              textColor: riskColor,
              trailColor: "#eee",
            })}
          />

          <h3>Risk Score</h3>

          <span
            className={`badge ${
              scan.verdict === "Safe"
                ? "safe"
                : scan.verdict === "Warning"
                ? "warning"
                : "danger"
            }`}
          >
            {scan.verdict}
          </span>

        </div>

        <div className="details-card">

          <h3>🤖 AI Summary</h3>

          <p>{scan.ai_summary}</p>

          <hr />

          <h3>🔑 Keywords</h3>

          <ul>
            {(scan.detected_keywords || []).map((k, i) => (
              <li key={i}>{k}</li>
            ))}
          </ul>

          <h3>🌐 URLs</h3>

          <ul>
            {(scan.detected_urls || []).map((u, i) => (
              <li key={i}>{u}</li>
            ))}
          </ul>

          <h3>📧 Emails</h3>

          <ul>
            {(scan.detected_emails || []).map((e, i) => (
              <li key={i}>{e}</li>
            ))}
          </ul>

          <h3>📱 Phone Numbers</h3>

          <ul>
            {(scan.detected_phones || []).map((p, i) => (
              <li key={i}>{JSON.stringify(p)}</li>
            ))}
          </ul>

          <h3>💻 IP Addresses</h3>

          <ul>
            {(scan.detected_ips || []).map((ip, i) => (
              <li key={i}>{ip}</li>
            ))}
          </ul>

          <h3>🚨 Malicious URLs</h3>

          <ul>
            {(scan.malicious_urls || []).map((url, i) => (
              <li key={i}>{url}</li>
            ))}
          </ul>

        </div>

      </div>

    </div>

  );
}