const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json({ limit: "2mb" }));

const API_KEY = "PEGA_TU_API_KEY_ELEVENLABS";
const VOICE_ID = "EXAVITQu4vr4xnSDxMaL"; // Rachel (femenina)

app.post("/hablar", async (req, res) => {
  try {
    const { texto } = req.body;

    if (!texto) return res.status(400).send("Sin texto");

    const response = await axios({
      method: "POST",
      url: `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`,
      headers: {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
      },
      data: {
        text: texto,
        voice_settings: {
          stability: 0.4,
          similarity_boost: 0.85,
          style: 0.7,
          use_speaker_boost: true
        }
      },
      responseType: "arraybuffer"
    });

    res.set("Content-Type", "audio/mpeg");
    res.send(response.data);

  } catch (err) {
    console.error(err.response?.data || err.message);
    res.status(500).send("Error generando voz");
  }
});

app.listen(3000, () =>
  console.log("🔥 Backend listo en http://localhost:3000")
);
