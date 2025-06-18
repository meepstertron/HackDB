import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Input } from '../ui/input';

const StringNode = ({ data }: any) => (
    <div className="bg-white border border-[#1a192b] rounded  p-3 min-w-[160px]">
        <div className="text-xs font-semibold text-[#1a192b] mb-2 font-mono border">String</div>
        <Input 
            className="h-8 px-2 text-sm rounded focus:ring-1 focus:ring-blue-500 border-[#1a192b]" 
            placeholder="Enter text..."
            value={data.value}
            onChange={(e) => data.onChange?.(e.target.value)}
        />
        <Handle 
            type="source" 
            position={Position.Bottom} 
            id="source1"
        />

    </div>
);

export default StringNode;