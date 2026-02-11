import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Compass,
  TrendingUp,
  Heart,
  Target,
  Settings,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Clock,
  Star,
  BookmarkPlus,
  Bell,
  User,
  Filter,
  Activity,
  BarChart3,
  PieChart,
  Calendar
} from 'lucide-react';

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'discover', label: 'Discover', icon: Compass },
  { id: 'trending', label: 'Trending', icon: TrendingUp },
  { id: 'interests', label: 'My Interests', icon: Heart },
  { id: 'predictions', label: 'My Predictions', icon: Target },
  { id: 'settings', label: 'Settings', icon: Settings },
];

// Mock data for different tabs
const mockTrendingTopics = [
  { label: 'AI Regulation', events: 12, change: '+24%' },
  { label: 'Oil Prices', events: 8, change: '+18%' },
  { label: 'Fed Policy', events: 15, change: '+8%' },
  { label: 'Crypto ETFs', events: 6, change: '+45%' },
  { label: 'China Stimulus', events: 4, change: '+12%' },
];

const mockInterests = [
  { tag: 'Energy', weight: 85, notifications: true },
  { tag: 'Technology', weight: 72, notifications: true },
  { tag: 'Federal Reserve', weight: 68, notifications: false },
  { tag: 'Cryptocurrency', weight: 45, notifications: true },
  { tag: 'Trade Policy', weight: 32, notifications: false },
];

const mockPredictions = [
  { asset: 'XOM', prediction: 'BULLISH', confidence: 92, status: 'ACTIVE', timeLeft: '2h 15m' },
  { asset: 'MSFT', prediction: 'BEARISH', confidence: 65, status: 'PENDING', timeLeft: '8h 45m' },
  { asset: 'BTC', prediction: 'BULLISH', confidence: 78, status: 'ACTIVE', timeLeft: '1d 3h' },
  { asset: 'SPY', prediction: 'BULLISH', confidence: 88, status: 'VALIDATED', accuracy: 'CORRECT' },
];

function DashboardTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Activity className="w-4 h-4 text-accent-blue" />
        <h3 className="text-sm font-semibold text-white">Dashboard</h3>
      </div>
      
      {/* Quick Stats */}
      <div className="grid grid-cols-2 gap-3">
        <div className="p-3 bg-bg-primary rounded-lg">
          <div className="flex items-center gap-2 mb-1">
            <Calendar className="w-3 h-3 text-accent-blue" />
            <span className="text-xs text-text-secondary">Today</span>
          </div>
          <p className="text-lg font-bold text-white">24</p>
          <p className="text-xs text-text-secondary">Events</p>
        </div>
        <div className="p-3 bg-bg-primary rounded-lg">
          <div className="flex items-center gap-2 mb-1">
            <BarChart3 className="w-3 h-3 text-accent-green" />
            <span className="text-xs text-text-secondary">Accuracy</span>
          </div>
          <p className="text-lg font-bold text-accent-green">78%</p>
          <p className="text-xs text-text-secondary">Last 24h</p>
        </div>
        <div className="p-3 bg-bg-primary rounded-lg">
          <div className="flex items-center gap-2 mb-1">
            <Target className="w-3 h-3 text-accent-amber" />
            <span className="text-xs text-text-secondary">Active</span>
          </div>
          <p className="text-lg font-bold text-white">12</p>
          <p className="text-xs text-text-secondary">Predictions</p>
        </div>
        <div className="p-3 bg-bg-primary rounded-lg">
          <div className="flex items-center gap-2 mb-1">
            <PieChart className="w-3 h-3 text-accent-red" />
            <span className="text-xs text-text-secondary">Alerts</span>
          </div>
          <p className="text-lg font-bold text-accent-red">3</p>
          <p className="text-xs text-text-secondary">High Sev</p>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="space-y-2">
        <h4 className="text-xs text-text-secondary uppercase tracking-wider">Recent Activity</h4>
        <div className="space-y-2">
          <div className="p-3 bg-bg-primary rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-white">XOM Prediction</span>
              <span className="text-xs text-accent-green">+2.4%</span>
            </div>
            <p className="text-xs text-text-secondary">Validated • 15 min ago</p>
          </div>
          <div className="p-3 bg-bg-primary rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-white">Fed Rate Decision</span>
              <span className="text-xs text-accent-amber">HIGH</span>
            </div>
            <p className="text-xs text-text-secondary">New event • 32 min ago</p>
          </div>
          <div className="p-3 bg-bg-primary rounded-lg">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-white">MSFT Alert</span>
              <span className="text-xs text-accent-red">-1.2%</span>
            </div>
            <p className="text-xs text-text-secondary">Price movement • 1h ago</p>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="space-y-2">
        <h4 className="text-xs text-text-secondary uppercase tracking-wider">Quick Actions</h4>
        <div className="space-y-2">
          <button className="w-full p-3 bg-accent-blue/20 text-accent-blue rounded-lg text-left text-sm hover:bg-accent-blue/30 transition-colors">
            Create Custom Alert
          </button>
          <button className="w-full p-3 bg-bg-primary text-white rounded-lg text-left text-sm hover:bg-gray-800 transition-colors">
            Export Today's Data
          </button>
          <button className="w-full p-3 bg-bg-primary text-white rounded-lg text-left text-sm hover:bg-gray-800 transition-colors">
            View Full Analytics
          </button>
        </div>
      </div>
    </div>
  );
}

function DiscoverTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-4 h-4 text-accent-blue" />
        <h3 className="text-sm font-semibold text-white">Discover</h3>
      </div>
      
      <div className="space-y-2">
        <h4 className="text-xs text-text-secondary uppercase tracking-wider">Recommended for you</h4>
        <div className="space-y-3">
          <div className="p-3 bg-bg-primary rounded-lg">
            <p className="text-sm text-white mb-1">European Central Bank Policy</p>
            <p className="text-xs text-text-secondary mb-2">Based on your interest in monetary policy</p>
            <button className="text-xs text-accent-blue">+ Follow Topic</button>
          </div>
          <div className="p-3 bg-bg-primary rounded-lg">
            <p className="text-sm text-white mb-1">Renewable Energy Sector</p>
            <p className="text-xs text-text-secondary mb-2">High activity detected</p>
            <button className="text-xs text-accent-blue">+ Follow Topic</button>
          </div>
          <div className="p-3 bg-bg-primary rounded-lg">
            <p className="text-sm text-white mb-1">China Trade Relations</p>
            <p className="text-xs text-text-secondary mb-2">Trending in your region</p>
            <button className="text-xs text-accent-blue">+ Follow Topic</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function TrendingTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp className="w-4 h-4 text-accent-green" />
        <h3 className="text-sm font-semibold text-white">Trending</h3>
      </div>
      
      <div className="space-y-2">
        <h4 className="text-xs text-text-secondary uppercase tracking-wider">Hot Topics</h4>
        <div className="space-y-2">
          {mockTrendingTopics.map((topic, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-bg-primary rounded-lg hover:bg-gray-800 cursor-pointer">
              <div>
                <p className="text-sm text-white">{topic.label}</p>
                <p className="text-xs text-text-secondary">{topic.events} events</p>
              </div>
              <span className="text-xs text-accent-green font-semibold">{topic.change}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function InterestsTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Heart className="w-4 h-4 text-accent-red" />
          <h3 className="text-sm font-semibold text-white">My Interests</h3>
        </div>
        <button className="text-xs text-accent-blue">+ Add</button>
      </div>
      
      <div className="space-y-3">
        {mockInterests.map((interest, index) => (
          <div key={index} className="p-3 bg-bg-primary rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-white">{interest.tag}</span>
              <div className="flex items-center gap-2">
                <Bell className={`w-4 h-4 ${interest.notifications ? 'text-accent-blue' : 'text-gray-600'}`} />
                <span className="text-xs text-text-secondary">{interest.weight}%</span>
              </div>
            </div>
            <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
              <div 
                className="h-full bg-accent-blue rounded-full"
                style={{ width: `${interest.weight}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PredictionsTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Target className="w-4 h-4 text-accent-blue" />
        <h3 className="text-sm font-semibold text-white">My Predictions</h3>
      </div>
      
      <div className="space-y-2">
        <h4 className="text-xs text-text-secondary uppercase tracking-wider">Active & Recent</h4>
        <div className="space-y-3">
          {mockPredictions.map((pred, index) => (
            <div key={index} className="p-3 bg-bg-primary rounded-lg border border-gray-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-mono text-accent-blue">{pred.asset}</span>
                <span className={`text-xs px-2 py-0.5 rounded ${
                  pred.status === 'ACTIVE' ? 'bg-accent-green/20 text-accent-green' :
                  pred.status === 'PENDING' ? 'bg-accent-amber/20 text-accent-amber' :
                  'bg-accent-blue/20 text-accent-blue'
                }`}>
                  {pred.status}
                </span>
              </div>
              <div className="flex items-center justify-between mb-1">
                <span className={`text-xs ${
                  pred.prediction === 'BULLISH' ? 'text-accent-green' : 'text-accent-red'
                }`}>
                  {pred.prediction}
                </span>
                <span className="text-xs text-text-secondary">{pred.confidence}% conf</span>
              </div>
              {pred.timeLeft && (
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-text-secondary" />
                  <span className="text-xs text-text-secondary">{pred.timeLeft}</span>
                </div>
              )}
              {pred.accuracy && (
                <div className="text-xs text-accent-green mt-1">
                  ✓ {pred.accuracy}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function SettingsTab() {
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-4 h-4 text-text-secondary" />
        <h3 className="text-sm font-semibold text-white">Settings</h3>
      </div>
      
      <div className="space-y-4">
        <div className="space-y-2">
          <h4 className="text-xs text-text-secondary uppercase tracking-wider">Notifications</h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-bg-primary rounded-lg">
              <span className="text-sm text-white">High Severity Events</span>
              <button className="w-10 h-5 bg-accent-blue rounded-full relative">
                <div className="w-4 h-4 bg-white rounded-full absolute right-0.5 top-0.5" />
              </button>
            </div>
            <div className="flex items-center justify-between p-3 bg-bg-primary rounded-lg">
              <span className="text-sm text-white">Prediction Updates</span>
              <button className="w-10 h-5 bg-gray-600 rounded-full relative">
                <div className="w-4 h-4 bg-white rounded-full absolute left-0.5 top-0.5" />
              </button>
            </div>
          </div>
        </div>
        
        <div className="space-y-2">
          <h4 className="text-xs text-text-secondary uppercase tracking-wider">Display</h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-bg-primary rounded-lg">
              <span className="text-sm text-white">Auto-refresh</span>
              <select className="bg-gray-700 text-white text-sm rounded px-2 py-1">
                <option>5 seconds</option>
                <option>10 seconds</option>
                <option>30 seconds</option>
              </select>
            </div>
            <div className="flex items-center justify-between p-3 bg-bg-primary rounded-lg">
              <span className="text-sm text-white">Confidence threshold</span>
              <input 
                type="range" 
                min="0" 
                max="100" 
                defaultValue="60"
                className="w-16"
              />
            </div>
          </div>
        </div>
        
        <div className="space-y-2">
          <h4 className="text-xs text-text-secondary uppercase tracking-wider">Account</h4>
          <div className="space-y-2">
            <button className="w-full p-3 bg-bg-primary rounded-lg text-left text-sm text-white hover:bg-gray-800">
              Profile Settings
            </button>
            <button className="w-full p-3 bg-bg-primary rounded-lg text-left text-sm text-white hover:bg-gray-800">
              Export Data
            </button>
            <button className="w-full p-3 bg-accent-red/20 rounded-lg text-left text-sm text-accent-red hover:bg-accent-red/30">
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function RightPanel({ isExpanded, setIsExpanded }) {
  const [activeTab, setActiveTab] = useState('dashboard');

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardTab />;
      case 'discover':
        return <DiscoverTab />;
      case 'trending':
        return <TrendingTab />;
      case 'interests':
        return <InterestsTab />;
      case 'predictions':
        return <PredictionsTab />;
      case 'settings':
        return <SettingsTab />;
      default:
        return <DashboardTab />;
    }
  };

  return (
    <div className="fixed right-0 top-16 bottom-0 z-40 flex">
      {/* Toggle Button */}
      <button
        onClick={toggleExpanded}
        className="w-10 h-16 bg-bg-card border-l border-t border-b border-gray-800 rounded-l-lg flex items-center justify-center text-text-secondary hover:text-white transition-colors hover:bg-bg-card-alt"
        aria-label={isExpanded ? "Collapse panel" : "Expand panel"}
      >
        {isExpanded ? (
          <ChevronRight className="w-5 h-5" />
        ) : (
          <ChevronLeft className="w-5 h-5" />
        )}
      </button>

      {/* Panel */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 320, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            className="bg-bg-card-alt border-l border-gray-800 overflow-hidden"
          >
            <div className="flex flex-col h-full">
              {/* Tab Navigation */}
              <div className="border-b border-gray-800 px-4 py-3">
                <div className="grid grid-cols-3 gap-1">
                  {tabs.map((tab) => {
                    const Icon = tab.icon;
                    return (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`p-2 rounded-lg transition-colors text-xs flex flex-col items-center gap-1 ${
                          activeTab === tab.id
                            ? 'bg-accent-blue/20 text-accent-blue'
                            : 'text-text-secondary hover:text-white hover:bg-gray-700'
                        }`}
                        title={tab.label}
                      >
                        <Icon className="w-4 h-4" />
                        <span className="truncate w-full">{tab.label.split(' ')[0]}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Tab Content */}
              <div className="flex-1 overflow-y-auto p-4">
                <motion.div
                  key={activeTab}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  {renderTabContent()}
                </motion.div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Mobile Overlay */}
      {isExpanded && (
        <div 
          className="fixed inset-0 bg-black/30 backdrop-blur-sm lg:hidden"
          onClick={() => setIsExpanded(false)}
        />
      )}
    </div>
  );
}

// Mobile-optimized version that slides up from bottom
export function MobileRightPanel({ isExpanded, setIsExpanded, activeTab, setActiveTab }) {
  const [showContent, setShowContent] = useState(false);

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <DashboardTab />;
      case 'discover':
        return <DiscoverTab />;
      case 'trending':
        return <TrendingTab />;
      case 'interests':
        return <InterestsTab />;
      case 'predictions':
        return <PredictionsTab />;
      case 'settings':
        return <SettingsTab />;
      default:
        return <DashboardTab />;
    }
  };

  return (
    <AnimatePresence>
      {isExpanded && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50"
            onClick={() => setIsExpanded(false)}
          />

          {/* Panel */}
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="fixed bottom-0 left-0 right-0 z-50 bg-bg-card-alt border-t border-gray-800 rounded-t-2xl max-h-[80vh] flex flex-col"
          >
            {/* Handle */}
            <div className="flex justify-center py-2">
              <div className="w-12 h-1 bg-gray-600 rounded-full" />
            </div>

            {/* Tab Navigation */}
            <div className="border-b border-gray-800 px-4 pb-3">
              <div className="flex overflow-x-auto gap-2 scrollbar-hide">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex-shrink-0 p-3 rounded-lg transition-colors text-xs flex flex-col items-center gap-2 min-w-[70px] ${
                        activeTab === tab.id
                          ? 'bg-accent-blue/20 text-accent-blue'
                          : 'text-text-secondary hover:text-white hover:bg-gray-700'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="text-[10px] leading-none">{tab.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2 }}
              >
                {renderTabContent()}
              </motion.div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}