import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Input } from '../ui/input';
import { DollarSign } from 'lucide-react';

const NumberNode = ({ data }: any) => (
    <div className="bg-white border border-[#1a192b] rounded p-3 pt-0 min-w-[160px] overflow-hidden">

        <div className="text-xs font-semibold text-[#1a192b] mb-2 font-mono flex flex-row items-center border-b pt-1 bg-muted -mx-3 border-[#1a192b]"><span className='mx-1'>Number</span></div>
        <Input
            className="h-8 px-2 text-sm rounded focus:ring-1 focus:ring-blue-500 border-[#1a192b]"
            placeholder="Enter number..."
            value={data.value}
            onChange={(e) => data.onChange?.(e.target.value)}
            defaultValue={data.value || 0}
        />
        <Handle
            type="source" 
            position={Position.Right} 
            id="source1"
            style={{ top: '60%' }}
        />

    </div>
);

export default NumberNode;