import { motion } from 'framer-motion';
import { CheckCircle, XCircle, Clock, TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';

function getStatusIcon(status) {
  switch (status) {
    case 'CORRECT':
      return <CheckCircle className="w-4 h-4 text-accent-green" />;
    case 'INCORRECT':
      return <XCircle className="w-4 h-4 text-accent-red" />;
    default:
      return <Clock className="w-4 h-4 text-text-secondary" />;
  }
}

function getStatusBadge(status) {
  switch (status) {
    case 'CORRECT':
      return 'bg-accent-green/20 text-accent-green';
    case 'INCORRECT':
      return 'bg-accent-red/20 text-accent-red';
    default:
      return 'bg-gray-700/50 text-text-secondary';
  }
}

function formatChange(change) {
  const sign = change >= 0 ? '+' : '';
  return `${sign}${change.toFixed(2)}%`;
}

function CalibrationChart({ validations }) {
  // Group by confidence buckets (0-10%, 10-20%, etc.)
  const buckets = Array(10).fill(null).map(() => ({ total: 0, correct: 0 }));
  
  validations.forEach((v) => {
    const bucketIndex = Math.min(Math.floor(v.predicted_confidence * 10), 9);
    buckets[bucketIndex].total++;
    if (v.status === 'CORRECT') {
      buckets[bucketIndex].correct++;
    }
  });

  return (
    <div className="bg-bg-card border border-gray-800 rounded-card p-4">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="w-4 h-4 text-accent-blue" />
        <h4 className="text-sm font-semibold text-white">Calibration</h4>
      </div>
      <div className="flex items-end gap-1 h-20">
        {buckets.map((bucket, i) => {
          const accuracy = bucket.total > 0 ? (bucket.correct / bucket.total) * 100 : 0;
          const expected = (i + 0.5) * 10;
          return (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div className="w-full flex flex-col items-center">
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: `${accuracy * 0.8}px` }}
                  className={`w-full rounded-t ${
                    bucket.total > 0
                      ? accuracy >= expected ? 'bg-accent-green' : 'bg-accent-red'
                      : 'bg-gray-700'
                  }`}
                  style={{ minHeight: bucket.total > 0 ? 4 : 0 }}
                />
              </div>
            </div>
          );
        })}
      </div>
      <div className="flex justify-between text-xs text-text-secondary mt-2">
        <span>0%</span>
        <span>Confidence Bucket</span>
        <span>100%</span>
      </div>
    </div>
  );
}

export default function ValidationPanel({ validations, demoMode }) {
  // Calculate metrics
  const totalValidations = validations.length;
  const correctCount = validations.filter((v) => v.status === 'CORRECT').length;
  const accuracy = totalValidations > 0 ? (correctCount / totalValidations * 100).toFixed(1) : 0;
  const avgConfidence = totalValidations > 0
    ? (validations.reduce((sum, v) => sum + v.predicted_confidence, 0) / totalValidations * 100).toFixed(0)
    : 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-text-secondary uppercase tracking-wider">
          Validation Results
        </h2>
        {demoMode && (
          <span className="px-2 py-1 bg-accent-amber/20 text-accent-amber text-xs rounded">
            Simulated validation (demo mode)
          </span>
        )}
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-bg-card border border-gray-800 rounded-card p-4">
          <p className="text-xs text-text-secondary mb-1">Total Validated</p>
          <p className="text-2xl font-bold text-white">{totalValidations}</p>
        </div>
        <div className="bg-bg-card border border-gray-800 rounded-card p-4">
          <p className="text-xs text-text-secondary mb-1">Accuracy (24h)</p>
          <p className="text-2xl font-bold text-accent-green">{accuracy}%</p>
        </div>
        <div className="bg-bg-card border border-gray-800 rounded-card p-4">
          <p className="text-xs text-text-secondary mb-1">Correct Predictions</p>
          <p className="text-2xl font-bold text-white">{correctCount}</p>
        </div>
        <div className="bg-bg-card border border-gray-800 rounded-card p-4">
          <p className="text-xs text-text-secondary mb-1">Avg Confidence</p>
          <p className="text-2xl font-bold text-accent-blue">{avgConfidence}%</p>
        </div>
      </div>

      {/* Main content: Table + Calibration */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Table */}
        <div className="lg:col-span-2 bg-bg-card border border-gray-800 rounded-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-bg-primary">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Event
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Ticker
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Predicted
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Actual
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Window
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-semibold text-text-secondary uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {validations.map((v) => (
                  <motion.tr
                    key={v.event_id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="hover:bg-bg-card-alt transition-colors"
                  >
                    <td className="px-4 py-3">
                      <p className="text-white font-medium line-clamp-1 max-w-[200px]">
                        {v.headline}
                      </p>
                    </td>
                    <td className="px-4 py-3">
                      <span className="font-mono text-accent-blue">{v.predicted_ticker}</span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <div className="flex items-center justify-center gap-1">
                        {v.predicted_direction === 'BULLISH' ? (
                          <TrendingUp className="w-4 h-4 text-accent-green" />
                        ) : (
                          <TrendingDown className="w-4 h-4 text-accent-red" />
                        )}
                        <span className={
                          v.predicted_direction === 'BULLISH' ? 'text-accent-green' : 'text-accent-red'
                        }>
                          {v.predicted_direction}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={
                        v.actual_change_percent >= 0 ? 'text-accent-green' : 'text-accent-red'
                      }>
                        {formatChange(v.actual_change_percent)}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="text-text-secondary">{v.horizon}</span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium ${getStatusBadge(v.status)}`}>
                        {getStatusIcon(v.status)}
                        {v.status === 'CORRECT' ? 'Correct' : v.status === 'INCORRECT' ? 'Incorrect' : 'Pending'}
                      </span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Calibration Chart */}
        <CalibrationChart validations={validations} />
      </div>
    </motion.div>
  );
}
