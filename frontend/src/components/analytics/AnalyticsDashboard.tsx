/**
 * Компонент панели аналитики
 */

import { useState, useEffect } from 'react';
import { analyticsService } from '../../services/analytics';
import type { AnalyticsPeriod, MetricSummary, OverviewResponse } from '../../types/analytics';
import { PERIOD_LABELS } from '../../types/analytics';

interface AnalyticsDashboardProps {
    onClose?: () => void;
}

export function AnalyticsDashboard({ onClose }: AnalyticsDashboardProps) {
    const [period, setPeriod] = useState<AnalyticsPeriod>('week');
    const [overview, setOverview] = useState<OverviewResponse | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, [period]);

    const loadData = async () => {
        try {
            setLoading(true);
            const data = await analyticsService.getOverview(period);
            setOverview(data);
        } catch (err) {
            console.error('Ошибка загрузки аналитики:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white dark:bg-gray-800">
            {onClose && (
                <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Аналитика
                    </h2>
                    <button
                        onClick={onClose}
                        className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>
            )}

            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <div className="flex gap-2">
                    {(Object.keys(PERIOD_LABELS) as AnalyticsPeriod[]).map((p) => (
                        <button
                            key={p}
                            onClick={() => setPeriod(p)}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${period === p
                                    ? 'bg-blue-500 text-white'
                                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                                }`}
                        >
                            {PERIOD_LABELS[p]}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
                {loading ? (
                    <div className="grid grid-cols-2 gap-4">
                        {[1, 2, 3, 4].map((i) => (
                            <div key={i} className="h-32 bg-gray-100 dark:bg-gray-700 rounded-xl animate-pulse" />
                        ))}
                    </div>
                ) : overview ? (
                    <div className="space-y-6">
                        <div className="grid grid-cols-2 gap-4">
                            <MetricCard
                                title="Сообщения"
                                metric={overview.messages}
                                icon={
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                                    </svg>
                                }
                            />
                            <MetricCard
                                title="Активные пользователи"
                                metric={overview.active_users}
                                icon={
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                                    </svg>
                                }
                            />
                            <MetricCard
                                title="Новые чаты"
                                metric={overview.new_chats}
                                icon={
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                                    </svg>
                                }
                            />
                            <MetricCard
                                title="Медиафайлы"
                                metric={overview.media_shared}
                                icon={
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                }
                            />
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
                            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-4">
                                Активность за период
                            </h3>
                            <div className="h-48 flex items-end gap-1">
                                {Array.from({ length: 7 }).map((_, i) => (
                                    <div
                                        key={i}
                                        className="flex-1 bg-blue-500 rounded-t"
                                        style={{ height: `${20 + Math.random() * 80}%` }}
                                    />
                                ))}
                            </div>
                            <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                                <span>Пн</span>
                                <span>Вт</span>
                                <span>Ср</span>
                                <span>Чт</span>
                                <span>Пт</span>
                                <span>Сб</span>
                                <span>Вс</span>
                            </div>
                        </div>
                    </div>
                ) : null}
            </div>
        </div>
    );
}

interface MetricCardProps {
    title: string;
    metric: MetricSummary;
    icon: React.ReactNode;
}

function MetricCard({ title, metric, icon }: MetricCardProps) {
    const trendColor = metric.trend === 'up' ? 'text-green-500' : metric.trend === 'down' ? 'text-red-500' : 'text-gray-500';
    const trendIcon = metric.trend === 'up' ? '↑' : metric.trend === 'down' ? '↓' : '→';

    return (
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
            <div className="flex items-center justify-between mb-2">
                <span className="text-gray-500 dark:text-gray-400">{icon}</span>
                <span className={`text-sm font-medium ${trendColor}`}>
                    {trendIcon} {Math.abs(metric.change_percent)}%
                </span>
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {metric.current.toLocaleString()}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">{title}</p>
        </div>
    );
}
