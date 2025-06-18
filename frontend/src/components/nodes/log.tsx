import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Input } from '../ui/input';
import { DollarSign } from 'lucide-react';
import LabelHandle from './LabelHandle';

const LogNode = ({ data }: any) => (
    <div className="bg-white border border-[#1a192b] rounded p-3 pt-0 min-w-[160px] min-h-[80px] overflow-hidden">

        <div className="text-xs font-semibold text-[#1a192b] mb-2 font-mono flex flex-row items-center border-b pt-1 bg-muted -mx-3 border-[#1a192b]"><span className='mx-1'>Log to Console</span></div>
        
        <LabelHandle
            type="target" 
            position={Position.Left} 
            id="target1"
            style={{ top: '50%' }}
        />
        <LabelHandle
            type="target" 
            position={Position.Left} 
            id="trigger1"
            style={{ top: '80%', backgroundColor: 'lightblue' }}
            label="Trigger"
        />

    </div>
);

export default LogNode;