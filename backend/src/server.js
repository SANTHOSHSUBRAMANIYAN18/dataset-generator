import express from "express";
import cors from "cors";

const app = express();
const PORT = process.env.PORT || 4000;
const ML_SERVICE_URL =
  process.env.ML_SERVICE_URL || "http://127.0.0.1:8000/generate";

app.use(cors());
app.use(express.json());

function validatePayload(task, labels, samples) {
  if (!task || typeof task !== "string" || !task.trim()) {
    return "Task is required.";
  }

  if (!Array.isArray(labels) || labels.length === 0) {
    return "At least one label is required.";
  }

  if (labels.some((label) => typeof label !== "string" || !label.trim())) {
    return "Labels must be non-empty strings.";
  }

  if (!Number.isInteger(samples) || samples <= 0) {
    return "Samples must be a positive integer.";
  }

  return null;
}

app.post("/generate-dataset", async (req, res) => {
  const { task, labels, samples } = req.body;
  const error = validatePayload(task, labels, samples);

  if (error) {
    return res.status(400).json({ error });
  }

  try {
    const response = await fetch(ML_SERVICE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        task: task.trim(),
        labels: labels.map((label) => label.trim()),
        samples
      })
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data.detail || "ML service failed to generate the dataset."
      });
    }

    return res.json({ dataset: data.dataset });
  } catch (serviceError) {
    return res.status(500).json({
      error: "Could not reach the ML service."
    });
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
