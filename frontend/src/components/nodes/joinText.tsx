import React from 'react';
import { Handle, Position } from '@xyflow/react';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Variable } from 'lucide-react';
import LabelHandle from './LabelHandle';


const JoinTextNode = ({ data }: any) => (
    <div className="bg-white dark:bg-neutral-800 border border-[#1a192b] rounded p-3 pt-0 min-w-[160px] overflow-hidden dark:text-white dark:border-[#383745]">

        <div className="text-xs font-semibold text-[#1a192b] mb-2 font-mono flex flex-row items-center border-b pt-1 bg-muted -mx-3 dark:text-white border-[#1a192b] dark:border-[#383745]"><span className='mx-1 flex items-center gap-1'><Variable width={16} className='text-blue-500'/>Join</span></div>

        <div className='flex flex-col items-start w-full'>
        <LabelHandle
            type="target"
            position={Position.Left}
            id="target1"
            style={{ top: '50%' }}
            label="Input"
        />
        <LabelHandle
            type="target"
            position={Position.Left}
            id="target2"
            style={{ top: '75%' }}
            label="Input"
        />
        </div>
        <LabelHandle
            type="source"
            position={Position.Right}
            id="source1"
            label='Joined Text'
        />

    </div>
);

export default JoinTextNode;