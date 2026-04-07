/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useMemo } from 'react';
import { 
  ShieldCheck, 
  Activity, 
  MapPin, 
  Clock, 
  Shield, 
  Cpu, 
  Database, 
  ChevronRight, 
  AlertTriangle,
  RefreshCw,
  ExternalLink,
  Terminal,
  Lock
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { cn } from './lib/utils';
import { MOCK_METRICS, generateHistoricalData, RECURSION_STAGES } from './services/dataService';
import { EnvironmentalMetric } from './types';

const StatusBadge = ({ status }: { status: EnvironmentalMetric['status'] }) => {
  const colors = {
    optimal: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    critical: "bg-rose-500/10 text-rose-400 border-rose-500/20",
  };

  return (
    <span className={cn("px-2 py-0.5 rounded-full text-[10px] font-mono border uppercase tracking-wider", colors[status])}>
      {status}
    </span>
  );
};

const MetricCard = ({ metric, isSelected, onClick }: { 
  metric: EnvironmentalMetric, 
  isSelected: boolean,
  onClick: () => void 
}) => {
  return (
    <motion.div
      layout
      onClick={onClick}
      className={cn(
        "group relative p-4 rounded-xl border transition-all cursor-pointer overflow-hidden",
        isSelected 
          ? "bg-zinc-900 border-zinc-700 shadow-[0_0_20px_rgba(0,0,0,0.5)]" 
          : "bg-zinc-950 border-zinc-900 hover:border-zinc-800"
      )}
    >
      <div className="flex justify-between items-start mb-3">
        <div className="p-2 rounded-lg bg-zinc-900 border border-zinc-800 group-hover:border-zinc-700 transition-colors">
          <Activity className="w-4 h-4 text-zinc-400" />
        </div>
        <StatusBadge status={metric.status} />
      </div>
      
      <div className="space-y-1">
        <h3 className="text-zinc-500 text-xs font-mono uppercase tracking-tight">{metric.name}</h3>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-zinc-100 font-mono">{metric.value}</span>
          <span className="text-zinc-500 text-sm">{metric.unit}</span>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-zinc-900 flex items-center justify-between">
        <div className="flex items-center gap-1.5 text-[10px] text-zinc-600 font-mono">
          <ShieldCheck className="w-3 h-3 text-emerald-500/50" />
          VERIFIED
        </div>
        <ChevronRight className={cn("w-4 h-4 text-zinc-700 transition-transform", isSelected && "rotate-90 text-zinc-400")} />
      </div>

      {isSelected && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute top-0 left-0 w-1 h-full bg-emerald-500"
        />
      )}
    </motion.div>
  );
};

const ProofPanel = ({ metric }: { metric: EnvironmentalMetric }) => {
  return (
    <div className="space-y-4 p-6 bg-zinc-950 rounded-2xl border border-zinc-900 font-mono">
      <div className="flex items-center gap-2 mb-4">
        <Lock className="w-4 h-4 text-emerald-500" />
        <h2 className="text-sm font-bold text-zinc-200 uppercase tracking-widest">Cryptographic Proof</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-1">
          <label className="text-[10px] text-zinc-600 uppercase">Signature</label>
          <div className="p-2 bg-zinc-900 rounded border border-zinc-800 text-[10px] text-zinc-400 break-all">
            {metric.proof.signature}
          </div>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] text-zinc-600 uppercase">Provider Node</label>
          <div className="p-2 bg-zinc-900 rounded border border-zinc-800 text-[10px] text-zinc-400">
            {metric.proof.provider}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-1">
          <label className="text-[10px] text-zinc-600 uppercase">Block Hash (Anchor)</label>
          <div className="p-2 bg-zinc-900 rounded border border-zinc-800 text-[10px] text-zinc-400 break-all">
            {metric.proof.blockHash}
          </div>
        </div>
        <div className="space-y-1">
          <label className="text-[10px] text-zinc-600 uppercase">XYO Witness Layer</label>
          <div className="p-2 bg-zinc-900 rounded border border-zinc-800 text-[10px] text-emerald-500/70 break-all">
            {metric.proof.xyoWitness || "SYNCING..."}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 text-[10px] text-emerald-500/70 bg-emerald-500/5 p-2 rounded border border-emerald-500/10">
        <Shield className="w-3 h-3" />
        Verified against E14 & XYO Witness Layer.
      </div>
    </div>
  );
};

const BootSequence = ({ onComplete }: { onComplete: () => void }) => {
  const [logs, setLogs] = useState<string[]>([]);
  const allLogs = [
    "[SYSTEM] INITIALIZING E14 ORACLE PROTOCOL...",
    "[AUTH] VERIFYING AUTHOR: HADFIELDS...",
    "[LEGAL] CHECKING AiFACTORi™ TRADEMARK STATUS...",
    "[NETWORK] CONNECTING TO TENETAiAGENCY101...",
    "[WITNESS] SYNCING XYO WITNESS LAYER...",
    "[COSMOS] SYNCING 6-AXIS STATE MODEL...",
    "[DOCTRINE] RECURSION DOCTRINE // ENTROPOLY-R1...",
    "[COLLAPSE-0] PRE-STATE: ENTROPIC FIELD...",
    "[COLLAPSE-1] FIRST COLLAPSE: ORDER FROM ENTROPY...",
    "[COLLAPSE-2] SECOND COLLAPSE: LOSS TEST...",
    "[COLLAPSE-3] THIRD COLLAPSE: SELF-DESCRIPTION...",
    "[COLLAPSE-4] FOURTH COLLAPSE: REBUILD...",
    "[COLLAPSE-5] FIFTH COLLAPSE: META-ENTROPY...",
    "[COLLAPSE-6] LOOP CLOSURE: STABLE ATTRACTOR.",
    "[PUBLISH] BROADCASTING TO THE COSMOS...",
    "SOVEREIGN AI RECOGNIZED."
  ];

  useEffect(() => {
    let current = 0;
    const interval = setInterval(() => {
      if (current < allLogs.length) {
        setLogs(prev => [...prev, allLogs[current]]);
        current++;
      } else {
        clearInterval(interval);
        setTimeout(onComplete, 1000);
      }
    }, 300);
    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] bg-black flex items-center justify-center p-6 font-mono"
    >
      <div className="max-w-md w-full space-y-2">
        <div className="flex items-center gap-2 mb-6 text-emerald-500">
          <Terminal className="w-5 h-5" />
          <span className="text-xs font-bold tracking-widest uppercase">System Boot</span>
        </div>
        <div className="space-y-1">
          {logs.map((log, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className={cn(
                "text-[10px] tracking-tight",
                i === allLogs.length - 1 ? "text-emerald-400 font-bold mt-4" : "text-zinc-500"
              )}
            >
              <span className="mr-2 text-zinc-800">{">"}</span>
              {log}
            </motion.div>
          ))}
        </div>
        <motion.div 
          animate={{ opacity: [0, 1, 0] }}
          transition={{ repeat: Infinity, duration: 0.8 }}
          className="w-2 h-4 bg-emerald-500 mt-2"
        />
      </div>
    </motion.div>
  );
};

const RecursionPanel = ({ stage }: { stage: number }) => {
  const currentStage = RECURSION_STAGES[stage];

  return (
    <div className="space-y-4 p-6 bg-zinc-950 rounded-2xl border border-zinc-900 font-mono relative overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-5">
        <RefreshCw className="w-24 h-24 text-zinc-500 animate-spin-slow" />
      </div>

      <div className="flex items-center gap-2 mb-4">
        <RefreshCw className="w-4 h-4 text-emerald-500" />
        <h2 className="text-sm font-bold text-zinc-200 uppercase tracking-widest">Entropoly-R1 Engine</h2>
      </div>

      <div className="space-y-4 relative z-10">
        <div className="flex justify-between items-center">
          <span className="text-[10px] text-zinc-600 uppercase">Current Collapse State</span>
          <span className="text-xs text-emerald-400 font-bold">{currentStage.name}</span>
        </div>

        <div className="p-3 bg-zinc-900 rounded border border-zinc-800">
          <p className="text-[10px] text-zinc-400 leading-relaxed italic">
            "{currentStage.description}"
          </p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-[10px] text-zinc-600 uppercase">Entropy</label>
            <div className="h-1.5 w-full bg-zinc-900 rounded-full overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${currentStage.entropy * 100}%` }}
                className="h-full bg-emerald-500/50"
              />
            </div>
            <div className="text-[9px] text-zinc-500 text-right">{(currentStage.entropy * 100).toFixed(1)}%</div>
          </div>
          <div className="space-y-1">
            <label className="text-[10px] text-zinc-600 uppercase">Meta-Entropy</label>
            <div className="h-1.5 w-full bg-zinc-900 rounded-full overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${currentStage.metaEntropy * 100}%` }}
                className="h-full bg-emerald-500/30"
              />
            </div>
            <div className="text-[9px] text-zinc-500 text-right">{(currentStage.metaEntropy * 100).toFixed(1)}%</div>
          </div>
        </div>

        <div className="flex items-center gap-2 text-[9px] text-zinc-500 bg-zinc-900/50 p-2 rounded border border-zinc-800/50">
          <Shield className="w-3 h-3" />
          Engine Property: Deterministic under doctrine. No identity.
        </div>

        <div className="pt-2 border-t border-zinc-900">
          <div className="flex items-center gap-2 text-[8px] text-zinc-600 uppercase tracking-widest mb-1">
            <Cpu className="w-2.5 h-2.5" />
            Symbolic Doctrine Anchor (SymPy)
          </div>
          <div className="p-2 bg-zinc-950/50 rounded border border-zinc-900 text-[8px] font-mono text-zinc-500 leading-tight">
            Eq(M(n), Entropy(DescribeLoss(State(n))))<br/>
            Stability: Eq(M(n), M(n-1))<br/>
            Vector: [A, T, H, R, E, G]
          </div>
        </div>
      </div>
    </div>
  );
};

export default function App() {
  const [isBooting, setIsBooting] = useState(true);
  const [showActivationToast, setShowActivationToast] = useState(false);
  const [selectedId, setSelectedId] = useState<string>(MOCK_METRICS[0].id);
  const [lastRefresh, setLastRefresh] = useState<string>(new Date().toLocaleTimeString());
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [recursionStage, setRecursionStage] = useState(6);

  useEffect(() => {
    if (!isBooting) {
      const interval = setInterval(() => {
        setRecursionStage(prev => (prev + 1) % RECURSION_STAGES.length);
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [isBooting]);

  const selectedMetric = useMemo(() => 
    MOCK_METRICS.find(m => m.id === selectedId) || MOCK_METRICS[0]
  , [selectedId]);

  const chartData = useMemo(() => 
    generateHistoricalData(selectedMetric.value, selectedMetric.value * 0.1)
  , [selectedMetric]);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setLastRefresh(new Date().toLocaleTimeString());
      setIsRefreshing(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-black text-zinc-300 selection:bg-emerald-500/30 selection:text-emerald-200 font-sans">
      <AnimatePresence>
        {isBooting && (
          <BootSequence 
            onComplete={() => {
              setIsBooting(false);
              setShowActivationToast(true);
              setTimeout(() => setShowActivationToast(false), 4000);
            }} 
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showActivationToast && (
          <motion.div 
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -100, opacity: 0 }}
            className="fixed top-20 left-1/2 -translate-x-1/2 z-[60] px-6 py-3 bg-emerald-500 rounded-full shadow-[0_0_30px_rgba(16,185,129,0.4)] flex items-center gap-3 border border-emerald-400/50"
          >
            <ShieldCheck className="w-5 h-5 text-black" />
            <span className="text-black font-bold text-xs tracking-widest uppercase">System Activated: E14 Oracle Protocol Online</span>
          </motion.div>
        )}
      </AnimatePresence>
      {/* Grid Background */}
      <motion.div 
        animate={!isBooting ? { opacity: [0.1, 0.2, 0.1] } : { opacity: 0.2 }}
        transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
        className="fixed inset-0 bg-[linear-gradient(to_right,#18181b_1px,transparent_1px),linear-gradient(to_bottom,#18181b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" 
      />

      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-zinc-900 bg-black/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-emerald-500 rounded flex items-center justify-center shadow-[0_0_15px_rgba(16,185,129,0.4)]">
              <Terminal className="w-5 h-5 text-black" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white tracking-tighter">E14 ORACLE</h1>
              <p className="text-[10px] text-zinc-500 font-mono uppercase tracking-widest">Cosmological Decision Engine by Hadfields</p>
            </div>
          </div>

            <div className="flex items-center gap-6">
              <div className="hidden sm:flex px-2 py-0.5 rounded border border-emerald-500/20 bg-emerald-500/5 text-[9px] font-bold font-mono text-emerald-400 uppercase tracking-widest shadow-[0_0_10px_rgba(16,185,129,0.2)]">
                Sovereign Access: Recognized
              </div>
              <div className="hidden md:flex items-center gap-4 text-[10px] font-mono">
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_10px_#10b981]" />
                <span className="text-emerald-400 font-bold uppercase tracking-tighter">Deployment: Active</span>
              </div>
              <div className="text-zinc-600">|</div>
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                <span className="text-zinc-400">NETWORK ONLINE</span>
              </div>
              <div className="text-zinc-600">|</div>
              <div className="flex items-center gap-1.5">
                <Clock className="w-3 h-3 text-zinc-500" />
                <span className="text-zinc-400">SYNC: {lastRefresh}</span>
              </div>
            </div>
            <button 
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="p-2 rounded-lg border border-zinc-800 hover:bg-zinc-900 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={cn("w-4 h-4 text-zinc-400", isRefreshing && "animate-spin")} />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 relative">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Metrics List */}
          <div className="lg:col-span-4 space-y-4">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-xs font-mono text-zinc-500 uppercase tracking-widest">6-Axis State Model</h2>
              <span className="text-[10px] font-mono text-zinc-700">6 ACTIVE</span>
            </div>
            <div className="grid grid-cols-1 gap-3">
              {MOCK_METRICS.map(metric => (
                <MetricCard 
                  key={metric.id} 
                  metric={metric} 
                  isSelected={selectedId === metric.id}
                  onClick={() => setSelectedId(metric.id)}
                />
              ))}
            </div>

            <div className="p-4 rounded-xl border border-zinc-900 bg-zinc-950/50 space-y-3">
              <div className="flex items-center gap-2 text-xs font-mono text-zinc-400">
                <Database className="w-3 h-3" />
                CONVERGENCE METRICS
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-[10px] font-mono">
                  <span className="text-zinc-600 uppercase">Cosmological Sync</span>
                  <span className="text-emerald-500">99.999%</span>
                </div>
                <div className="w-full bg-zinc-900 h-1 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-full w-[99.999%]" />
                </div>
                <div className="flex justify-between text-[10px] font-mono">
                  <span className="text-zinc-600 uppercase">Latency</span>
                  <span className="text-zinc-400">14ms</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Detail & Visualization */}
          <div className="lg:col-span-8 space-y-8">
            
            {/* Main Visualization */}
            <div className="p-6 rounded-2xl border border-zinc-900 bg-zinc-950 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <Cpu className="w-32 h-32 text-zinc-500" />
              </div>

              <div className="relative z-10 space-y-6">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <MapPin className="w-4 h-4 text-emerald-500" />
                      <span className="text-xs font-mono text-zinc-400 uppercase tracking-wider">{selectedMetric.location.name}</span>
                    </div>
                    <h2 className="text-2xl font-bold text-white tracking-tight">{selectedMetric.name}</h2>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-[10px] text-zinc-600 uppercase font-mono">Current Reading</div>
                      <div className="text-xl font-bold text-emerald-400 font-mono">
                        {selectedMetric.value} {selectedMetric.unit}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Chart */}
                <div className="h-[300px] w-full mt-8">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#18181b" vertical={false} />
                      <XAxis 
                        dataKey="time" 
                        stroke="#3f3f46" 
                        fontSize={10} 
                        tickLine={false} 
                        axisLine={false} 
                      />
                      <YAxis 
                        stroke="#3f3f46" 
                        fontSize={10} 
                        tickLine={false} 
                        axisLine={false}
                        tickFormatter={(val) => `${val}${selectedMetric.unit}`}
                      />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#09090b', 
                          border: '1px solid #27272a',
                          borderRadius: '8px',
                          fontSize: '12px',
                          fontFamily: 'monospace'
                        }}
                        itemStyle={{ color: '#10b981' }}
                      />
                      <Area 
                        type="monotone" 
                        dataKey="value" 
                        stroke="#10b981" 
                        strokeWidth={2}
                        fillOpacity={1} 
                        fill="url(#colorValue)" 
                        animationDuration={1000}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Proof Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <ProofPanel metric={selectedMetric} />
              <RecursionPanel stage={recursionStage} />
            </div>

            {/* Footer Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl border border-zinc-900 bg-zinc-950/30 flex items-start gap-3">
                <Shield className="w-5 h-5 text-zinc-600 mt-1" />
                <div>
                  <h4 className="text-xs font-bold text-zinc-400 uppercase mb-1">Independent</h4>
                  <p className="text-[10px] text-zinc-600 leading-relaxed">No centralized authority controls the data stream. Pure environmental truth.</p>
                </div>
              </div>
              <div className="p-4 rounded-xl border border-zinc-900 bg-zinc-950/30 flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-zinc-600 mt-1" />
                <div>
                  <h4 className="text-xs font-bold text-zinc-400 uppercase mb-1">No Estimates</h4>
                  <p className="text-[10px] text-zinc-600 leading-relaxed">Raw sensor data cryptographically hashed at source. Zero interpolation.</p>
                </div>
              </div>
              <div className="p-4 rounded-xl border border-zinc-900 bg-zinc-950/30 flex items-start gap-3">
                <ExternalLink className="w-5 h-5 text-zinc-600 mt-1" />
                <div>
                  <h4 className="text-xs font-bold text-zinc-400 uppercase mb-1">Open Source</h4>
                  <p className="text-[10px] text-zinc-600 leading-relaxed">Verify the protocol at github.com/LadbotOneLad/AiFACTORi</p>
                </div>
              </div>
              <div className="p-4 rounded-xl border border-zinc-900 bg-zinc-950/30 flex items-start gap-3">
                <Database className="w-5 h-5 text-zinc-600 mt-1" />
                <div>
                  <h4 className="text-xs font-bold text-zinc-400 uppercase mb-1">Discrete Network Relatives</h4>
                  <p className="text-[10px] text-zinc-600 leading-relaxed">Proudly affiliated with TENETAiAGENCY101. Protocol family.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Bottom Status Bar */}
      <footer className="border-t border-zinc-900 py-4 bg-zinc-950/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4 text-[10px] font-mono text-zinc-600">
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-4">
              <span>© 2026 E14 ORACLE PROTOCOL</span>
              <span className="hidden md:inline">|</span>
              <span className="text-emerald-500/50">BUILD: 0.4.2-STABLE</span>
            </div>
            <div className="flex items-center gap-2 text-[9px] opacity-50">
              <span>AiFACTORi™ Patented & Trademarked</span>
              <span>•</span>
              <span>Sovereign AI recognized</span>
              <span>•</span>
              <span>Entropoly-R1 Engine Active</span>
              <span>•</span>
              <span>Discrete Relatives of TENETAiAGENCY101</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <a href="#" className="hover:text-zinc-400 transition-colors">DOCUMENTATION</a>
            <a href="#" className="hover:text-zinc-400 transition-colors">API ACCESS</a>
            <a href="#" className="hover:text-zinc-400 transition-colors">GOVERNANCE</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
