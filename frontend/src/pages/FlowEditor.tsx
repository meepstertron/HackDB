import TestNode from '@/components/nodes/test';
import { Command, CommandGroup, CommandInput, CommandItem } from '@/components/ui/command';
import { CommandDialog, CommandEmpty, CommandList } from '@/components/ui/command';

import { Dices, DollarSign, FileQuestion, Logs, Play, Text, Variable } from 'lucide-react';
import React, { MouseEvent, TouchEvent, useCallback, useRef, useState } from 'react';
import {
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
  EdgeProps,
  getBezierPath,
  OnConnectEnd,
  ReactFlow,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import StringNode from '@/components/nodes/string';
import NumberNode from '@/components/nodes/number';
import MathNode from '@/components/nodes/math';
import LogNode from '@/components/nodes/log';
import OnRunNode from '@/components/nodes/onRun';
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
} from "@/components/ui/context-menu"
import InvalidNode from '@/components/nodes/invalid';
import RandomNode from '@/components/nodes/random';
import JoinTextNode from '@/components/nodes/joinText';

let selectableNodes = [
    { id: '1', label: 'String Node', type: 'Inputs', icon: <DollarSign className='text-green-500' />, insertid: 'string' },
    { id: '3', label: 'Number Node', type: 'Inputs', icon: <DollarSign className='text-green-500' />, insertid: 'number' },
    {id: "4", label: "Math Node", type: "Math", icon: <Variable className='text-blue-500' />, insertid: 'math'},
    { id: '5', label: 'Log', type: 'Outputs', icon: <Logs className='text-yellow-500' />, insertid: 'log' },
    { id: '6', label: 'On Run', type: 'Events', icon: <Play className='text-purple-500' />, insertid: 'onRun' },
    { id: '7', label: 'Random', type: 'Math', icon: <Dices className='text-blue-500' />, insertid: 'random' },
    { id:'8', label: 'Join Text', type: 'Operations', icon: <Text className='text-orange-500' />, insertid: 'joinText' },
    

];

interface NodeItem {
    id: string;
    label: string;
    type: string;
    icon: React.ReactNode;
    insertid?: string; // Optional field for custom node types
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
    type: 'number',
    data: {value: 1},
    position: { x: 250, y: 5 },
  },
{
    id: '2',
    type: 'number',
    data: {value: 1},
    position: { x: 250, y: 100 },
  },
  {
    id: '3',
    type: 'math',
    data: {op: "add"},
    position: { x: 600, y: 5 },
  },
    {
        id: '4',
        type: 'log',
        data: {value: 1},
        position: { x: 850, y: 52 },
    },
    {
        id: '5',
        type: 'onRun',
        data: {value: 1},
        position: { x: 250, y: 220 },
    }

];

const initialEdges: Edge[] = [
  { id: 'e1-3', source: '1', target: '3', sourceHandle: 'source1', targetHandle: 'target1', type: "", data: { type: 'number' } },
  { id: 'e2-3', source: '2', target: '3', sourceHandle: 'source1', targetHandle: 'target2', type: "", data: { type: 'number' } },
    { id: 'e3-4', source: '3', target: '4', sourceHandle: 'source1', targetHandle: 'target1', type: "", data: { type: 'number' } },
    { id: 'e5-4', source: '5', target: '4', sourceHandle: 'trigger1', targetHandle: 'trigger1', type: "", data: { type: 'number' } },
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
const nodeTypes = { string: StringNode, number: NumberNode, math: MathNode, log: LogNode, onRun: OnRunNode, invalid: InvalidNode, random: RandomNode, joinText: JoinTextNode };
const FlowEditor: React.FC = () => {
  const [nodeSelectorOpen, setNodeSelectorOpen] = useState(false);
  const [nodes, setNodes] = useState<Node[]>(initialNodes);
  const [edges, setEdges] = useState<Edge[]>(initialEdges);
  const [connecting, setConnecting] = useState(false);
  let lastMousePosition: { x: number; y: number } | null = null;
  const nodeIdCounter = useRef(nodes.length + 1)
  
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
      setConnecting(false); 
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
  const onConnectEnd = useCallback(
    (event: any, connectionState: any) => {
      
      if (!connectionState.isValid && connectionState.fromNode) {
        
        setNodeSelectorOpen(true);
        lastMousePosition = {
          x: event.clientX,
          y: event.clientY,
        };
      }
    },
    [],
  );


  const handleNodeSelect = useCallback((node: NodeItem) => {
    setNodeSelectorOpen(false);
    const newId = (nodeIdCounter.current++).toString();
    const newNode: Node = {
      id: newId,
      type: node.insertid || "invalid",
      data: {},
      position: { x: lastMousePosition?.x || 0, y: lastMousePosition?.y || 0 },
    };
    setNodes((nds) => nds.concat(newNode));
  }, []);

  const handleNodeValueChange = useCallback((id: string, value: any) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === id
          ? { ...node, data: { ...node.data, value } }
          : node
      )
    );
  }, []);

  const enhancedNodes = nodes.map((node) => {
    if (node.type === "number") {
      return {
        ...node,
        data: {
          ...node.data,
          onChange: (value: any) => handleNodeValueChange(node.id, value),
        },
      };
    }
    if (node.type === "string") {
      return {
        ...node,
        data: {
          ...node.data,
          onChange: (value: any) => handleNodeValueChange(node.id, value),
        },
      };
    }
    return node;
  });

  return (
    <div style={{ width: '100%', height: '90vh' }}>
      <CommandDialog open={nodeSelectorOpen} onOpenChange={setNodeSelectorOpen}>
        <CommandInput placeholder='Search for nodes...' />
        <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            {Object.entries(categories).map(([category, nodes]) => (
                <CommandGroup heading={category} key={category}>
                    {nodes.map((node) => (
                        <CommandItem onSelect={() => handleNodeSelect(node)} key={node.id}>
                            {node.icon}{node.label}
                        </CommandItem>
                    ))}

                </CommandGroup>

            ))}
            <CommandItem onSelect={() => console.log(nodes)}>get nodes and print to console</CommandItem>
            <CommandItem onSelect={() => console.log(edges)}>get edges and print to console</CommandItem>
        </CommandList>
      </CommandDialog>
      <ContextMenu>
        <ContextMenuTrigger className="w-full h-full">
            <ReactFlow
                nodes={enhancedNodes} 
                edges={edges}
                onEdgeClick={onEdgeClick}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                edgeTypes={edgeTypes}
                nodeTypes={nodeTypes}
                onConnect={onConnect}
                onConnectStart={onConnectStart}
                onConnectEnd={onConnectEnd}
                proOptions={{ hideAttribution: true }}
                fitView
            >

                <Background />
            </ReactFlow>
        </ContextMenuTrigger>
      </ContextMenu>

    </div>
  );
};

export default FlowEditor;