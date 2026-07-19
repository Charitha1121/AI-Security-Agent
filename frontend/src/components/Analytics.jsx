import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  XAxis,
  YAxis,
  Bar,
} from "recharts";

export default function Analytics({ files }) {

  const scanned = files.filter(
    f => f.scan_status === "completed"
  ).length;

  const pending = files.length - scanned;

  const pieData = [
    {
      name: "Scanned",
      value: scanned,
    },
    {
      name: "Pending",
      value: pending,
    },
  ];

  const barData = [
    {
      name: "Files",
      Uploaded: files.length,
      Scanned: scanned,
    },
  ];

  const COLORS = [
    "#2563eb",
    "#f59e0b",
  ];

  return (

    <div className="analytics">

      <div className="chart">

        <h3>File Status</h3>

        <ResponsiveContainer
          width="100%"
          height={250}
        >

          <PieChart>

            <Pie
              data={pieData}
              dataKey="value"
              outerRadius={80}
            >

              {pieData.map((entry, index) => (

                <Cell
                  key={index}
                  fill={COLORS[index]}
                />

              ))}

            </Pie>

            <Tooltip />

          </PieChart>

        </ResponsiveContainer>

      </div>

      <div className="chart">

        <h3>Uploads</h3>

        <ResponsiveContainer
          width="100%"
          height={250}
        >

          <BarChart
            data={barData}
          >

            <XAxis dataKey="name"/>

            <YAxis/>

            <Tooltip/>

            <Bar
              dataKey="Uploaded"
              fill="#2563eb"
            />

            <Bar
              dataKey="Scanned"
              fill="#22c55e"
            />

          </BarChart>

        </ResponsiveContainer>

      </div>

    </div>

  );

}