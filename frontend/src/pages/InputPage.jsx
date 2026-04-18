import { useState } from "react";
import { useNavigate } from "react-router-dom";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:4000";

export default function InputPage() {
  const navigate = useNavigate();
  const [task, setTask] = useState("");
  const [labels, setLabels] = useState("");
  const [samples, setSamples] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    const parsedLabels = labels
      .split(",")
      .map((label) => label.trim())
      .filter(Boolean);

    try {
      const response = await fetch(`${API_BASE_URL}/generate-dataset`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          task: task.trim(),
          labels: parsedLabels,
          samples: Number(samples)
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate dataset.");
      }

      navigate("/output", {
        state: {
          dataset: data.dataset,
          task: task.trim()
        }
      });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-shell">
      <div className="card">
        <h1>Generate Dataset</h1>
        <form className="form" onSubmit={handleSubmit}>
          <label>
            Task Name
            <input
              type="text"
              value={task}
              onChange={(event) => setTask(event.target.value)}
              placeholder="e.g. News classification"
            />
          </label>

          <label>
            Labels
            <input
              type="text"
              value={labels}
              onChange={(event) => setLabels(event.target.value)}
              placeholder="e.g. Fake, Real"
            />
          </label>

          <label>
            Number of Samples
            <input
              type="number"
              min="1"
              value={samples}
              onChange={(event) => setSamples(event.target.value)}
            />
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate Dataset"}
          </button>
        </form>
        {loading ? <p className="status">Generating dataset...</p> : null}
        {error ? <p className="error">{error}</p> : null}
      </div>
    </div>
  );
}
