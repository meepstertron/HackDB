import TestNode from '@/components/nodes/test';
import { Command, CommandInput, CommandItem } from '@/components/ui/command';
import { CommandDialog, CommandEmpty, CommandList } from '@/components/ui/command';

import { FileQuestion } from 'lucide-react';
import React, { MouseEvent, TouchEvent, useCallback, useState } from 'react';
import { EdgeProps, getBezierPath, OnConnectEnd } from 'reactflow';
import ReactFlow, {
  addEdge,
  MiniMap,
  Controls,
  Background,
  Connection,
  Edge,
  Node,
  ReactFlowInstance,
  applyEdgeChanges,
  applyNodeChanges,
  NodeToolbar,
} from 'reactflow';
import 'reactflow/dist/style.css';




let selectableNodes = [
    { id: '1', label: 'String Node', type: 'ungrouped', icon: <FileQuestion /> },
    { id: '2', label: 'Another Node', type: 'ungrouped', icon: <FileQuestion /> },
];

interface NodeItem {
    id: string;
    label: string;
    type: string;
    icon: React.ReactNode;
}

let categories: Record<string, NodeItem[]> = {};
for (const node of selectableNodes) {
  if (!node.type) {
    node.type = 'ungrouped';
  }
  if (!categories[node.type]) {
    categories[node.type] = [];
  }
  categories[node.type].push(node);
}

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'input',
    data: { label: 'string Node'},
    position: { x: 250, y: 5 },
  },
  {
    id: '2',
    data: { label: 'Another Node' },
    position: { x: 100, y: 100 },
  },
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', type: "typeEdge", data: { type: 'string' } },
];
const TypeEdge: React.FC<EdgeProps> = ({
  id, sourceX, sourceY, targetX, targetY, data,
}) => {
  const [edgePath] = getBezierPath({ sourceX, sourceY, targetX, targetY });
  return (
    <>
      <path id={id} d={edgePath} stroke={data?.type === 'number' ? 'blue' : '#f0cf3e'} strokeWidth={2} fill="none" className='cursor-not-allowed' />

    </>
  );
};


const edgeTypes = { typeEdge: TypeEdge };
const nodeTypes = { test: TestNode };
const FlowEditor: React.FC = () => {
  const [nodeSelectorOpen, setNodeSelectorOpen] = useState(false);
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [connecting, setConnecting] = useState(false);

  const onNodesChange = useCallback(
    (changes: any[]) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes: any[]) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );
  const onConnectStart = useCallback(() => {
    setConnecting(true);
  }, []);
  const onConnect = useCallback(
    (connection: Edge | Connection) => {
      setEdges((eds) => addEdge(connection, eds));
      setConnecting(false); // Clear flag on successful connect
    },
    []
  );
  const onEdgeClick = useCallback(
  (event: React.MouseEvent, edge: Edge) => {
    event.stopPropagation();
    setEdges((eds) => eds.filter((e) => e.id !== edge.id));
  },
  []
);
const onConnectEnd: OnConnectEnd = (event: any, connectionState: any) => {
  if (!connectionState.isValid) {
    console.log("Dropped on pane");
    // your logic...
  }
};


  return (
    <div style={{ width: '100%', height: '90vh' }}>
      <CommandDialog open={nodeSelectorOpen} onOpenChange={setNodeSelectorOpen}>
        <CommandInput placeholder='Search for nodes...' />
        <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            
        </CommandList>
      </CommandDialog>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onEdgeClick={onEdgeClick}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        edgeTypes={edgeTypes}
        nodeTypes={nodeTypes}
        onConnect={onConnect}
        onConnectStart={onConnectStart}
        onConnectEnd={(event: any, connectionState: any) => {
        

          if (!connectionState.isValid) {
            console.log("Connection dropped outside a valid handle – do something!");
          }
        }}
        
        proOptions={{ hideAttribution: true }}
        fitView
      >
        
        <Controls />
        <Background />

      </ReactFlow>
    </div>
  );
};

export default FlowEditor;