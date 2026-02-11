import { motion } from 'framer-motion';
import { Clock, ExternalLink, TrendingUp, TrendingDown } from 'lucide-react';

function getSeverityColor(severity) {
  switch (severity) {
    case 'HIGH':
      return 'bg-accent-red text-white';
    case 'MEDIUM':
      return 'bg-accent-orange text-white';
    case 'LOW':
      return 'bg-accent-amber text-gray-900';
    default:
      return 'bg-gray-600 text-white';
  }
}

function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  }) + ' UTC';
}

function getQuickImpact(assets) {
  if (!assets || assets.length === 0) return null;
  return assets.slice(0, 3).map((asset) => ({
    ticker: asset.ticker,
    direction: asset.prediction
  }));
}

function EventCard({ event, isActive, onClick }) {
  const quickImpact = getQuickImpact(event.affected_assets);
  const avgConfidence = event.affected_assets?.length > 0
    ? Math.round(event.affected_assets.reduce((sum, a) => sum + a.confidence, 0) / event.affected_assets.length * 100)
    : 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      onClick={onClick}
      className={`p-4 rounded-card cursor-pointer transition-all border ${
        isActive
          ? 'bg-bg-card-alt border-accent-blue'
          : 'bg-bg-card border-transparent hover:border-gray-700'
      }`}
      tabIndex={0}
      role="button"
      aria-label={`Event: ${event.headline}`}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
    >
      {/* Top Row: Severity + Time */}
      <div className="flex items-center justify-between mb-2">
        <span
          className={`px-2 py-0.5 rounded text-xs font-semibold ${getSeverityColor(event.severity)}`}
          title="Severity indicates expected market-moving potential"
        >
          {event.severity}
        </span>
        <div className="flex items-center gap-1 text-text-secondary text-xs">
          <Clock className="w-3 h-3" />
          <span>{formatTime(event.timestamp)}</span>
        </div>
      </div>

      {/* Headline */}
      <h3 className="text-sm font-medium text-white mb-2 line-clamp-2">
        {event.headline}
      </h3>

      {/* Quick Impact */}
      {quickImpact && (
        <div className="flex items-center gap-2 mb-2">
          {quickImpact.map((item) => (
            <span
              key={item.ticker}
              className="flex items-center gap-1 text-xs"
            >
              {item.direction === 'BULLISH' ? (
                <TrendingUp className="w-3 h-3 text-accent-green" />
              ) : item.direction === 'BEARISH' ? (
                <TrendingDown className="w-3 h-3 text-accent-red" />
              ) : null}
              <span className={
                item.direction === 'BULLISH' ? 'text-accent-green' :
                item.direction === 'BEARISH' ? 'text-accent-red' : 'text-text-secondary'
              }>
                {item.ticker}
              </span>
            </span>
          ))}
        </div>
      )}

      {/* Bottom Row: Source + Confidence */}
      <div className="flex items-center justify-between text-xs text-text-secondary">
        <div className="flex items-center gap-1">
          <ExternalLink className="w-3 h-3" />
          <span>{event.source}</span>
        </div>
        <span>Conf: {avgConfidence}%</span>
      </div>
    </motion.div>
  );
}

export default function EventFeed({ events, activeEventId, onSelectEvent }) {
  return (
    <div className="h-full overflow-y-auto pr-2 space-y-3">
      <h2 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4">
        Live Event Feed
      </h2>
      {events.map((event) => (
        <EventCard
          key={event.event_id}
          event={event}
          isActive={event.event_id === activeEventId}
          onClick={() => onSelectEvent(event.event_id)}
        />
      ))}
    </div>
  );
}
