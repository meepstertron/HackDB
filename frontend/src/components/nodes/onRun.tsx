import React from 'react';
import { Handle, Position } from '@xyflow/react';
import { Input } from '../ui/input';
import { DollarSign } from 'lucide-react';
import LabelHandle from './LabelHandle';

const OnRunNode = ({ data }: any) => (
    <div className="bg-white border border-[#1a192b] rounded p-3 pt-0 min-w-[160px] min-h-[80px] overflow-hidden">

        <div className="text-xs font-semibold text-[#1a192b] dark:text-white mb-0 font-mono flex flex-row items-center border-b pt-1 bg-muted -mx-3 border-[#1a192b] dark:border-white"><span className='mx-1'>On Run</span></div>
        <span className='text-[7px] font-mono text-muted-foreground '>triggers connected nodes when execution starts</span>

        <LabelHandle
            type="source" 
            position={Position.Right} 
            id="trigger1"
            style={{ top: '80%', backgroundColor: 'lightblue' }}
            label="Trigger"
        />

    </div>
);

export default OnRunNode;