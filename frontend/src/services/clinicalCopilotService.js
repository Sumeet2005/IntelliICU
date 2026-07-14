import api from "../api/axios";

export const clinicalCopilotService = {
  askQuestion: async (patientId, question) => {
    const response = await api.post(
      "/clinical-copilot/chat",
      {
        patient_id: patientId,
        question,
      },
      {
        timeout: 180000, // 3 minutes
      }
    );

    return response.data;
  },

  askQuestionStream: async (patientId, question, onToken, onFinal) => {
    // Resolve base API URL (e.g. from Axios instance configuration)
    const baseURL = api.defaults.baseURL || "/api";
    
    const response = await fetch(`${baseURL}/clinical-copilot/chat?stream=true`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        patient_id: patientId,
        question,
      }),
    });

    if (!response.ok) {
      throw new Error(`Inference stream connection failed: HTTP ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        
        // Keep trailing incomplete line in buffer
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith("data: ")) {
            try {
              const data = JSON.parse(trimmed.substring(6));
              if (data.type === "token") {
                onToken(data.content);
              } else if (data.type === "final") {
                onFinal(data.content);
              }
            } catch (err) {
              console.warn("Failed to parse SSE JSON chunk:", trimmed, err);
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }
};