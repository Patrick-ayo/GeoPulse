import { useCallback, useEffect, useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  MarkerType,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { motion } from 'framer-motion';
import { Zap, Globe, Building2, TrendingUp } from 'lucide-react';

const nodeColors = {
  event: { bg: '#1E90FF', border: '#60A5FA' },
  macro: { bg: '#A855F7', border: '#C084FC' },
  sector: { bg: '#F59E0B', border: '#FBBF24' },
  asset: { bg: '#22C55E', border: '#4ADE80' },
};

const nodeIcons = {
  event: Zap,
  macro: Globe,
  sector: Building2,
  asset: TrendingUp,
};

function CustomNode({ data }) {
  const Icon = nodeIcons[data.nodeType] || Zap;
  const colors = nodeColors[data.nodeType] || nodeColors.event;

  return (
    <motion.div
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: data.delay || 0, duration: 0.3 }}
      className="relative"
    >
      <motion.div
        animate={{
          boxShadow: [
            `0 0 0 0 ${colors.bg}40`,
            `0 0 20px 10px ${colors.bg}20`,
            `0 0 0 0 ${colors.bg}40`,
          ],
        }}
        transition={{ duration: 2, repeat: Infinity }}
        className="px-4 py-3 rounded-lg border-2 min-w-[120px] text-center"
        style={{
          backgroundColor: `${colors.bg}20`,
          borderColor: colors.border,
        }}
      >
        <div className="flex items-center justify-center gap-2 mb-1">
          <Icon className="w-4 h-4" style={{ color: colors.border }} />
          <span className="text-xs uppercase tracking-wide" style={{ color: colors.border }}>
            {data.nodeType}
          </span>
        </div>
        <p className="text-sm font-medium text-white">{data.label}</p>
      </motion.div>
    </motion.div>
  );
}

const nodeTypes = {
  custom: CustomNode,
};

function buildGraphFromLogicChain(logicChain) {
  if (!logicChain || logicChain.length === 0) {
    return { nodes: [], edges: [] };
  }

  const nodes = logicChain.map((item, index) => ({
    id: `node-${index}`,
    type: 'custom',
    position: { x: index * 200, y: 100 + Math.sin(index) * 30 },
    data: {
      label: item.text,
      nodeType: item.type,
      delay: index * 0.2,
    },
  }));

  const edges = logicChain.slice(0, -1).map((_, index) => ({
    id: `edge-${index}`,
    source: `node-${index}`,
    target: `node-${index + 1}`,
    animated: true,
    style: { stroke: '#4B5563', strokeWidth: 2 },
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: '#4B5563',
    },
  }));

  return { nodes, edges };
}

export default function RippleGraph({ logicChain, severity }) {
  const { nodes: initialNodes, edges: initialEdges } = useMemo(
    () => buildGraphFromLogicChain(logicChain),
    [logicChain]
  );

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  useEffect(() => {
    const { nodes: newNodes, edges: newEdges } = buildGraphFromLogicChain(logicChain);
    setNodes(newNodes);
    setEdges(newEdges);
  }, [logicChain, setNodes, setEdges]);

  // Don't show graph for LOW severity events
  if (severity === 'LOW' || !logicChain || logicChain.length === 0) {
    return (
      <div className="bg-bg-card border border-gray-800 rounded-card p-6 h-[300px] flex items-center justify-center">
        <p className="text-text-secondary text-sm">
          {severity === 'LOW'
            ? 'Ripple visualization hidden for LOW severity events'
            : 'No logic chain available'}
        </p>
      </div>
    );
  }

  return (
    <div className="bg-bg-card border border-gray-800 rounded-card overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-800">
        <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider">
          Event → Macro → Sector → Asset
        </h3>
      </div>
      <div className="h-[280px]">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.4 }}
          proOptions={{ hideAttribution: true }}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
          panOnScroll
          zoomOnScroll={false}
        >
          <Background color="#1f2937" gap={16} size={1} />
          <Controls
            showInteractive={false}
            className="bg-bg-card border border-gray-700 rounded"
          />
        </ReactFlow>
      </div>
    </div>
  );
}
