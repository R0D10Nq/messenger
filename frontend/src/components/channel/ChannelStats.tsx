/**
 * Компонент статистики канала
 */

import { useState, useEffect } from 'react';
import { channelService } from '../../services/channel';
import type { ChannelStats as ChannelStatsType } from '../../types/channel';

interface ChannelStatsProps {
    channelId: string;
}

export function ChannelStats({ channelId }: ChannelStatsProps) {
    const [stats, setStats] = useState<ChannelStatsType | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadStats();
    }, [channelId]);

    const loadStats = async () => {
        try {
            setLoading(true);
            const data = await channelService.getChannelStats(channelId);
            setStats(data);
        } catch (err) {
            console.error('Ошибка загрузки статистики:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="p-6 animate-pulse">
                <div className="grid grid-cols-2 gap-4">
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="h-20 bg-gray-200 dark:bg-gray-700 rounded-xl" />
                    ))}
                </div>
            </div>
        );
    }

    if (!stats) {
        return null;
    }

    return (
        <div className="p-6 space-y-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Статистика канала
            </h3>

            <div className="grid grid-cols-2 gap-4">
                <StatCard
                    title="Подписчики"
                    value={stats.subscriber_count.toLocaleString()}
                    icon={
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                    }
                    trend={stats.growth_rate}
                />

                <StatCard
                    title="Публикации"
                    value={stats.total_posts.toLocaleString()}
                    icon={
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                    }
                />

                <StatCard
                    title="Всего просмотров"
                    value={formatNumber(stats.total_views)}
                    icon={
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                    }
                />

                <StatCard
                    title="Среднее просмотров"
                    value={Math.round(stats.avg_views_per_post).toLocaleString()}
                    icon={
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    }
                />
            </div>

            {stats.top_posts.length > 0 && (
                <div>
                    <h4 className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3">
                        Популярные публикации
                    </h4>
                    <div className="space-y-2">
                        {stats.top_posts.slice(0, 3).map((post, idx) => (
                            <div
                                key={idx}
                                className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
                            >
                                <p className="text-sm text-gray-900 dark:text-white line-clamp-2">
                                    {post.content}
                                </p>
                                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                    {post.views?.toLocaleString() || 0} просмотров
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

interface StatCardProps {
    title: string;
    value: string;
    icon: React.ReactNode;
    trend?: number;
}

function StatCard({ title, value, icon, trend }: StatCardProps) {
    return (
        <div className="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-xl">
            <div className="flex items-center justify-between mb-2">
                <span className="text-gray-500 dark:text-gray-400">{icon}</span>
                {trend !== undefined && (
                    <span className={`text-xs font-medium ${trend >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        {trend >= 0 ? '+' : ''}{trend.toFixed(1)}%
                    </span>
                )}
            </div>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
            <p className="text-xs text-gray-500 dark:text-gray-400">{title}</p>
        </div>
    );
}

function formatNumber(num: number): string {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
}
