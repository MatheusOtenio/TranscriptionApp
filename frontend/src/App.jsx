import styles from "./App.module.css";
import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [transcription, setTranscription] = useState("");
  const [loading, setLoading] = useState(false);

  const handleTranscribe = async () => {
    setLoading(true);
    setTranscription("");
    try {
      const response = await fetch("http://127.0.0.1:8000/transcrever/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setTranscription(data.transcricao || "Erro ao transcrever");
    } catch (error) {
      setTranscription("Erro na requisição");
    }
    setLoading(false);
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Transcrição de Vídeo</h1>
        <p className={styles.subtitle}>
          Cole o link de um vídeo para obter a transcrição
        </p>
      </header>

      <div className={styles.inputGroup}>
        <input
          type="text"
          placeholder="Ex: https://youtube.com/watch?v=..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className={styles.input}
          disabled={loading}
        />
        <button
          onClick={handleTranscribe}
          disabled={loading}
          className={styles.button}
        >
          {loading ? (
            <div className={styles.loadingContainer}>
              <span className={styles.loadingSpinner} />
              Processando...
            </div>
          ) : (
            "Transcrever"
          )}
        </button>
      </div>

      {transcription && (
        <div className={styles.resultContainer}>
          <h2 className={styles.resultTitle}>Transcrição:</h2>
          <div className={styles.resultContent}>
            {transcription.startsWith("Erro") ? (
              <div className={styles.error}>
                <svg className={styles.errorIcon} viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M12,2C6.48,2 2,6.48 2,12s4.48,10 10,10 10-4.48 10-10S17.52,2 12,2zm1,15h-2v-2h2v2zm0-4h-2V7h2v6z"
                  />
                </svg>
                {transcription}
              </div>
            ) : (
              <p className={styles.transcriptionText}>{transcription}</p>
            )}
          </div>
        </div>
      )}

      <p className={styles.note}>
        Áudios com muita poluição sonora podem sair com leves diferenças.
      </p>
    </div>
  );
}

export default App;
