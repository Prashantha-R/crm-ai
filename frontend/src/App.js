import React, { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const emptyForm = {
    hcp_name: "",
    interaction_type: "Meeting",
    date: "",
    time: "",
    attendees: "",
    topics: "",
    materials: "",
    sentiment: "",
    outcomes: "",
    followup: ""
  };

  const [form, setForm] = useState(emptyForm);

  const resetForm = () => {
    setForm(emptyForm);
    setMessage("");
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        { message },
        { headers: { "Content-Type": "application/json" } }
      );

      let data = res.data.form_data || {};

      // DATE FIX
      let fixedDate = form.date;
      if (data.date) {
        let d = data.date.toLowerCase().trim();
        const today = new Date();

        if (d === "today") fixedDate = today.toISOString().split("T")[0];
        else if (d === "yesterday") {
          today.setDate(today.getDate() - 1);
          fixedDate = today.toISOString().split("T")[0];
        }
        else if (/^\d{2}-\d{2}-\d{4}$/.test(d)) {
          const [dd, mm, yyyy] = d.split("-");
          fixedDate = `${yyyy}-${mm}-${dd}`;
        }
        else if (/^\d{4}-\d{2}-\d{2}$/.test(d)) fixedDate = d;
      }

      // TIME FIX
      let fixedTime = form.time;
      if (data.time) {
        let t = data.time.toLowerCase().trim().replace(/\s/g, "");

        if (t === "morning") fixedTime = "09:00";
        else if (t === "afternoon") fixedTime = "15:00";
        else if (t === "evening") fixedTime = "18:00";
        else if (t.includes("am") || t.includes("pm")) {
          let meridian = t.includes("pm") ? "pm" : "am";
          let [h, m] = t.replace(/am|pm/g, "").split(":");

          h = parseInt(h);
          m = m || "00";

          if (meridian === "pm" && h !== 12) h += 12;
          if (meridian === "am" && h === 12) h = 0;

          fixedTime = `${h.toString().padStart(2, "0")}:${m}`;
        }
        else if (/^\d{2}:\d{2}$/.test(t)) fixedTime = t;
      }

      // RESET
      const isReset =
        data.hcp_name === "" &&
        data.date === "" &&
        data.time === "" &&
        data.sentiment === "" &&
        data.materials === "" &&
        data.topics === "";

      if (isReset) {
        setForm(emptyForm);
      } else {
        setForm((prev) => ({
          ...prev,
          hcp_name: data.hcp_name ?? prev.hcp_name,
          date: fixedDate || prev.date,
          time: fixedTime || prev.time,
          sentiment: data.sentiment ?? prev.sentiment,
          materials: data.materials ?? prev.materials,
          topics: data.topics ?? prev.topics
        }));
      }

      const aiText = `${res.data.response || "Done"}

👨‍⚕️ HCP: ${data.hcp_name || "N/A"}
📅 Date: ${fixedDate || "N/A"}
⏰ Time: ${fixedTime || "N/A"}
😊 Sentiment: ${data.sentiment || "N/A"}
📦 Materials: ${data.materials || "None"}
📌 Topics: ${data.topics || "N/A"}`;

      setChatHistory((prev) => [
        ...prev,
        { type: "user", text: message },
        { type: "ai", text: aiText }
      ]);

      setMessage("");

    } catch (err) {
      console.error(err);
      alert("Backend error");
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    background: "#f3f4f6",
    boxSizing: "border-box"
  };

  const section = { marginTop: "20px" };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial" }}>

      {/* LEFT */}
      <div style={{ width: "65%", padding: "25px", background: "#f5f7fa", overflowY: "scroll" }}>
        <h2>Log HCP Interaction</h2>

        {/* GRID */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
          <div>
            <label>HCP Name</label>
            <input value={form.hcp_name} readOnly style={inputStyle} />
          </div>

          <div>
            <label>Interaction Type</label>
            <select value={form.interaction_type} disabled style={inputStyle}>
              <option>Meeting</option>
              <option>Call</option>
              <option>Email</option>
            </select>
          </div>

          <div>
            <label>Date</label>
            <input type="date" value={form.date} readOnly style={inputStyle} />
          </div>

          <div>
            <label>Time</label>
            <input type="time" value={form.time} readOnly style={inputStyle} />
          </div>
        </div>

        <div style={section}>
          <label>Attendees</label>
          <input value={form.attendees} readOnly style={inputStyle} />
        </div>

        <div style={section}>
          <h4>Topics Discussed</h4>
          <textarea value={form.topics} readOnly style={{ ...inputStyle, height: "90px" }} />
        </div>

        <div style={section}>
          <h4>Materials Shared / Samples Distributed</h4>

          <b>Materials Shared</b>
          <div>{form.materials || "No materials added."}</div>
          <button style={{ marginTop: "5px" }}>🔍 Search/Add</button>

          <div style={{ marginTop: "10px" }}>
            <b>Samples Distributed</b>
            <div>No samples added.</div>
            <button style={{ marginTop: "5px" }}>➕ Add Sample</button>
          </div>
        </div>

        <div style={section}>
          <h4>Observed/Inferred HCP Sentiment</h4>

          {[
            { label: "positive", emoji: "😊" },
            { label: "neutral", emoji: "😐" },
            { label: "negative", emoji: "😠" }
          ].map((s) => (
            <label key={s.label} style={{ marginRight: "20px" }}>
              <input type="radio" checked={form.sentiment === s.label} disabled />
              {" "} {s.emoji} {s.label}
            </label>
          ))}
        </div>

        <div style={section}>
          <h4>Outcomes</h4>
          <textarea value={form.outcomes} readOnly style={{ ...inputStyle, height: "90px" }} />
        </div>

        <div style={section}>
          <h4>Follow-up Actions</h4>
          <textarea value={form.followup} readOnly style={{ ...inputStyle, height: "90px" }} />

          <div style={{
            marginTop: "15px",
            background: "#f0f9ff",
            padding: "10px",
            borderRadius: "8px",
            color: "#2563eb"
          }}>
            <b>AI Suggested Follow-ups:</b>
            <ul>
              <li>Schedule follow-up meeting in 2 weeks</li>
              <li>Send product brochure</li>
              <li>Add doctor to engagement list</li>
            </ul>
          </div>
        </div>

        <button onClick={resetForm} style={{ marginTop: "20px", padding: "10px", background: "red", cursor: "pointer", color: "white" }}>
          Reset Form
        </button>
      </div>

      {/* RIGHT */}
      <div style={{ width: "35%", padding: "20px", borderLeft: "1px solid #ddd", display: "flex", flexDirection: "column" }}>
        <h3>🤖 AI Assistant</h3>

        <p style={{ fontSize: "12px", color: "#666" }}>
          Log interaction details here via chat
        </p>

        <div style={{ background: "#dbeafe", padding: "10px", borderRadius: "8px" }}>
          Log interaction details here (e.g., "Met Dr. Smith...")
        </div>

        <div style={{ flex: 1, overflowY: "auto", marginTop: "10px" }}>
          {chatHistory.map((chat, i) => (
            <div key={i} style={{
              display: "flex",
              justifyContent: chat.type === "user" ? "flex-end" : "flex-start",
              marginBottom: "12px"
            }}>
              <div style={{
                background: chat.type === "user" ? "#2563eb" : "#d1fae5",
                color: chat.type === "user" ? "white" : "#065f46",
                padding: "10px",
                borderRadius: "12px",
                maxWidth: "80%"
              }}>
                {chat.text}
              </div>
            </div>
          ))}
        </div>

        <div style={{ position: "relative" }}>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Describe interaction..."
            style={{ ...inputStyle, background: "white" }}
          />

          <button
            onClick={sendMessage}
            style={{
              position: "absolute",
              right: "10px",
              bottom: "10px",
              width: "45px",
              height: "45px",
              borderRadius: "50%",
              background: "#2563eb",
              cursor: "pointer",
              color: "white"
            }}
          >
            A
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;