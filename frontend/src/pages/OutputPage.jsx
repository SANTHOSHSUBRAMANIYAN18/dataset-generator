import { useLocation, useNavigate } from "react-router-dom";

function convertToCsv(rows) {
  const header = ["Text", "Label"];
  const csvRows = rows.map((row) =>
    [row.text, row.label]
      .map((value) => `"${String(value).replaceAll('"', '""')}"`)
      .join(",")
  );

  return [header.join(","), ...csvRows].join("\n");
}

export default function OutputPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const dataset = location.state?.dataset || [];
  const task = location.state?.task || "dataset";

  function handleDownload() {
    const csvContent = convertToCsv(dataset);
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${task.toLowerCase().replace(/\s+/g, "-") || "dataset"}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  }

  if (!dataset.length) {
    return (
      <div className="page-shell">
        <div className="card">
          <h1>Generated Dataset</h1>
          <p className="status">No dataset available yet.</p>
          <button onClick={() => navigate("/")}>Generate Again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell">
      <div className="card wide-card">
        <div className="output-header">
          <h1>Generated Dataset</h1>
          <div className="button-row">
            <button onClick={handleDownload}>Download CSV</button>
            <button className="secondary-button" onClick={() => navigate("/")}>
              Generate Again
            </button>
          </div>
        </div>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Text</th>
                <th>Label</th>
              </tr>
            </thead>
            <tbody>
              {dataset.map((row, index) => (
                <tr key={`${row.label}-${index}`}>
                  <td>{row.text}</td>
                  <td>{row.label}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
