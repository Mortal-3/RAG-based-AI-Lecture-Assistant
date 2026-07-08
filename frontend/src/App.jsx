import { useState } from 'react'

function App() {
    const [question, setQuestion] = useState('')
    const [results, setResults] = useState(null)
    const [status, setStatus] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const apiUrl = 'http://localhost:5000/api'

    const fetchStatus = async () => {
        try {
            const response = await fetch(`${apiUrl}/status`)
            const data = await response.json()
            if (data.success) {
                setStatus(data.data)
            } else {
                setError(data.error || 'Could not load status')
            }
        } catch (err) {
            setError(err.message)
        }
    }

    const handleQuery = async () => {
        if (!question.trim()) {
            setError('Please enter a question first.')
            return
        }

        setLoading(true)
        setError('')

        try {
            const response = await fetch(`${apiUrl}/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question }),
            })
            const data = await response.json()
            if (data.success) {
                setResults(data.data)
            } else {
                setError(data.error || 'Failed to fetch results')
            }
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleProcessVideos = async () => {
        setLoading(true)
        setError('')

        try {
            const response = await fetch(`${apiUrl}/process-videos`, {
                method: 'POST',
            })
            const data = await response.json()
            if (!data.success) {
                setError(data.error || 'Failed to process videos')
            }
            await fetchStatus()
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const handleCreateChunks = async () => {
        setLoading(true)
        setError('')

        try {
            const response = await fetch(`${apiUrl}/create-chunks`, {
                method: 'POST',
            })
            const data = await response.json()
            if (!data.success) {
                setError(data.error || 'Failed to create chunks')
            }
            await fetchStatus()
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-shell">
            <header>
                <h1>RAG AI Lecture Assistant</h1>
                <p>Convert lecture videos into searchable answers.</p>
            </header>

            <section className="controls">
                <button onClick={handleProcessVideos} disabled={loading}>
                    Convert Videos
                </button>
                <button onClick={handleCreateChunks} disabled={loading}>
                    Create Transcript Chunks
                </button>
                <button onClick={fetchStatus} disabled={loading}>
                    Refresh Status
                </button>
            </section>

            <section className="query-panel">
                <textarea
                    rows="4"
                    placeholder="Ask a question about your lectures"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <button onClick={handleQuery} disabled={loading}>
                    {loading ? 'Searching...' : 'Search Lectures'}
                </button>
            </section>

            {error && <div className="error">{error}</div>}

            {status && (
                <section className="status-card">
                    <h2>Backend Status</h2>
                    <pre>{JSON.stringify(status, null, 2)}</pre>
                </section>
            )}

            {results && (
                <section className="results-card">
                    <h2>Search Results</h2>
                    <p>Question: {results.question}</p>
                    <div className="results-list">
                        {results.results.map((item) => (
                            <div key={item.chunk_id} className="result-item">
                                <strong>{item.title}</strong>
                                <p>{item.text}</p>
                                <small>Score: {item.score.toFixed(4)}</small>
                            </div>
                        ))}
                    </div>
                </section>
            )}
        </div>
    )
}

export default App
