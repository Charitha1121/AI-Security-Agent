import "../styles/dashboard.css";
import { ShieldCheck, FileText, Clock, Brain } from "lucide-react";

export default function DashboardCards({ files }) {
 const total = files.length;

const scanned = files.filter(
  (f) => f.scan_status === "completed"
).length;

const pending = total - scanned;

  return (
    <div className="cards">
      <div className="card blue">
        <FileText size={40} />
        <h2>{total}</h2>
        <p>Total Files</p>
      </div>

      <div className="card green">
        <ShieldCheck size={40} />
        <h2>{scanned}</h2>
        <p>Scanned</p>
      </div>

      <div className="card orange">
        <Clock size={40} />
        <h2>{pending}</h2>
        <p>Pending</p>
      </div>

      <div className="card purple">
        <Brain size={40} />
        <h2>AI</h2>
        <p>Powered by Groq</p>
      </div>
    </div>
  );
}