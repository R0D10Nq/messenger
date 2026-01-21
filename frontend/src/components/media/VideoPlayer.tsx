/**
 * Компонент видеоплеера с субтитрами
 */

import { useState, useRef, useEffect } from 'react';
import type { SubtitleCue, SubtitleSettings } from '../../types/subtitle';
import { DEFAULT_SUBTITLE_SETTINGS } from '../../types/subtitle';

interface VideoPlayerProps {
    src: string;
    poster?: string;
    subtitles?: SubtitleCue[];
    subtitleSettings?: SubtitleSettings;
    onTimeUpdate?: (currentTime: number) => void;
}

export function VideoPlayer({
    src,
    poster,
    subtitles = [],
    subtitleSettings = DEFAULT_SUBTITLE_SETTINGS,
    onTimeUpdate,
}: VideoPlayerProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [currentTime, setCurrentTime] = useState(0);
    const [currentCue, setCurrentCue] = useState<SubtitleCue | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [showControls, setShowControls] = useState(true);

    useEffect(() => {
        if (!subtitleSettings.enabled || subtitles.length === 0) {
            setCurrentCue(null);
            return;
        }

        const activeCue = subtitles.find(
            (cue) => currentTime >= cue.start_time && currentTime <= cue.end_time
        );
        setCurrentCue(activeCue || null);
    }, [currentTime, subtitles, subtitleSettings.enabled]);

    const handleTimeUpdate = () => {
        if (videoRef.current) {
            const time = videoRef.current.currentTime;
            setCurrentTime(time);
            onTimeUpdate?.(time);
        }
    };

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);

    const togglePlay = () => {
        if (videoRef.current) {
            if (isPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
        }
    };

    const subtitleStyle = {
        fontSize: `${subtitleSettings.font_size}px`,
        color: subtitleSettings.text_color,
        backgroundColor: `${subtitleSettings.background_color}${Math.round(subtitleSettings.background_opacity * 255).toString(16).padStart(2, '0')}`,
    };

    return (
        <div
            className="relative bg-black rounded-lg overflow-hidden group"
            onMouseEnter={() => setShowControls(true)}
            onMouseLeave={() => setShowControls(false)}
        >
            <video
                ref={videoRef}
                src={src}
                poster={poster}
                className="w-full h-full"
                onTimeUpdate={handleTimeUpdate}
                onPlay={handlePlay}
                onPause={handlePause}
                onClick={togglePlay}
            />

            {subtitleSettings.enabled && currentCue && (
                <div
                    className={`absolute left-0 right-0 flex justify-center px-4 pointer-events-none ${subtitleSettings.position === 'top' ? 'top-4' : 'bottom-16'
                        }`}
                >
                    <div
                        className="px-3 py-1 rounded text-center max-w-[80%]"
                        style={subtitleStyle}
                    >
                        {currentCue.text}
                    </div>
                </div>
            )}

            <div
                className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 transition-opacity ${showControls ? 'opacity-100' : 'opacity-0'
                    }`}
            >
                <div className="flex items-center gap-3">
                    <button
                        onClick={togglePlay}
                        className="p-2 text-white hover:text-blue-400 transition-colors"
                    >
                        {isPlaying ? (
                            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" />
                            </svg>
                        ) : (
                            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M8 5v14l11-7z" />
                            </svg>
                        )}
                    </button>

                    <div className="flex-1 h-1 bg-white/30 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-blue-500"
                            style={{
                                width: videoRef.current
                                    ? `${(currentTime / videoRef.current.duration) * 100}%`
                                    : '0%',
                            }}
                        />
                    </div>

                    <span className="text-white text-sm tabular-nums">
                        {formatTime(currentTime)}
                    </span>
                </div>
            </div>
        </div>
    );
}

function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

interface SubtitleOverlayProps {
    cue: SubtitleCue | null;
    settings: SubtitleSettings;
}

export function SubtitleOverlay({ cue, settings }: SubtitleOverlayProps) {
    if (!settings.enabled || !cue) {
        return null;
    }

    const style = {
        fontSize: `${settings.font_size}px`,
        color: settings.text_color,
        backgroundColor: `${settings.background_color}${Math.round(settings.background_opacity * 255).toString(16).padStart(2, '0')}`,
    };

    return (
        <div
            className={`absolute left-0 right-0 flex justify-center px-4 ${settings.position === 'top' ? 'top-4' : 'bottom-16'
                }`}
        >
            <div className="px-3 py-1 rounded text-center max-w-[80%]" style={style}>
                {cue.text}
            </div>
        </div>
    );
}
