import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

const TestNode: React.FC<NodeProps> = ({ data }) => (
  <div style={{ padding: 10, border: '1px solid #222', borderRadius: 5, background: '#fff' }}>
    {data.label}
    <Handle
      type="source"
      position={Position.Right}
      style={{
        width: 16,
        height: 16,
        borderRadius: 0, // makes it a square
        background: 'red',
        border: '2px solid #222',
        top: '50%',
        transform: 'translateY(-50%)',
      }}
    />
    <Handle
      type="target"
      position={Position.Left}
      style={{
        width: 16,
        height: 16,
        borderRadius: 0,
        background: 'blue',
        border: '2px solid #222',
        top: '50%',
        transform: 'translateY(-50%)',
      }}
    />
  </div>
);

export default TestNode;