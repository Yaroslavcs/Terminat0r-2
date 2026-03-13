const BASE = process.env.EXPO_PUBLIC_API_URL || "http://localhost:8000";

export const api = {
  async getQuest(deviceId: string, questId: number) {
    const res = await fetch(
      `${BASE}/api/quest/${questId}?device_id=${encodeURIComponent(deviceId)}`
    );
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async generateQuest(deviceId: string, task: string) {
    const res = await fetch(`${BASE}/api/quest/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task, device_id: deviceId }),
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },

  async verifyQuest(deviceId: string, questId: number, imageB64?: string) {
    const res = await fetch(`${BASE}/api/quest/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        device_id: deviceId,
        quest_id: questId,
        image_b64: imageB64 || null,
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    if (data.job_id) {
      return this.pollJob(data.job_id);
    }
    return data;
  },

  async pollJob(jobId: string): Promise<{
    verified: boolean;
    message: string;
    gold_earned: number;
    xp_earned: number;
    total_gold: number;
    total_xp: number;
    level: number;
  }> {
    const maxAttempts = 30;
    for (let i = 0; i < maxAttempts; i++) {
      const res = await fetch(`${BASE}/api/job/${jobId}`);
      if (!res.ok) throw new Error(await res.text());
      const job = await res.json();
      if (job.status === "completed") return job.result;
      if (job.status === "failed") throw new Error(job.error || "verification failed");
      await new Promise((r) => setTimeout(r, 1000));
    }
    throw new Error("verification timeout");
  },

  async analyzeScene(imageB64: string) {
    const res = await fetch(`${BASE}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_b64: imageB64 }),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    if (data.job_id) {
      return this.pollJobForFact(data.job_id);
    }
    return data;
  },

  async pollJobForFact(jobId: string): Promise<{ fact: string; category: string }> {
    const maxAttempts = 20;
    for (let i = 0; i < maxAttempts; i++) {
      const res = await fetch(`${BASE}/api/job/${jobId}`);
      if (!res.ok) throw new Error(await res.text());
      const job = await res.json();
      if (job.status === "completed") return job.result;
      if (job.status === "failed") throw new Error(job.error || "analysis failed");
      await new Promise((r) => setTimeout(r, 1500));
    }
    throw new Error("analysis timeout");
  },

  async getStats(deviceId: string) {
    const res = await fetch(`${BASE}/api/user/${encodeURIComponent(deviceId)}/stats`);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
};
