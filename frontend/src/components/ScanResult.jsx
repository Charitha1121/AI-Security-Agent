import "../styles/dashboard.css";
import ReactMarkdown from "react-markdown";

export default function ScanResult({ scan }) {

return (

<div className="section">

<h2>Scan Result</h2>

<h3>

Risk Score : {scan.risk_score}

</h3>

<h3>

Verdict : {scan.verdict}

</h3>

<div className="summary">

<ReactMarkdown>

{scan.ai_summary}

</ReactMarkdown>

</div>

</div>

);

}