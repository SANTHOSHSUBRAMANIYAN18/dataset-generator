import { Routes, Route } from "react-router-dom";
import InputPage from "./pages/InputPage";
import OutputPage from "./pages/OutputPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<InputPage />} />
      <Route path="/output" element={<OutputPage />} />
    </Routes>
  );
}
