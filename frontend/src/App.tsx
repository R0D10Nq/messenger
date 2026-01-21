import { useEffect, useState } from 'react'

interface HealthStatus {
    status: string
    version: string
}

export function App() {
    const [health, setHealth] = useState<HealthStatus | null>(null)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        fetch('/api/health')
            .then((res) => res.json())
            .then((data: HealthStatus) => setHealth(data))
            .catch((err: Error) => setError(err.message))
    }, [])

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 shadow-xl border border-white/20">
                <h1 className="text-3xl font-bold text-white mb-4">My Messenger</h1>
                <div className="text-slate-300">
                    {error ? (
                        <p className="text-red-400">Ошибка подключения: {error}</p>
                    ) : health ? (
                        <div className="space-y-2">
                            <p>Статус API: <span className="text-green-400 font-medium">{health.status}</span></p>
                            <p>Версия: <span className="text-blue-400">{health.version}</span></p>
                        </div>
                    ) : (
                        <p>Загрузка...</p>
                    )}
                </div>
            </div>
        </div>
    )
}
