import React from 'react';
import { Handle, Position } from '@xyflow/react';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { FileWarning, Variable } from 'lucide-react';


const InvalidNode = ({ data }: any) => (
    <div className="bg-white dark:bg-neutral-800 border border-[#1a192b] rounded p-3 pt-0 min-w-[160px] overflow-hidden dark:text-white dark:border-[#383745]">

        <div className="text-xs font-semibold text-[#1a192b] mb-2 font-mono flex flex-row items-center border-b pt-1 bg-muted -mx-3 dark:text-white border-[#1a192b] dark:border-[#383745]"><span className='mx-1 flex items-center gap-1'><FileWarning  width={16} className='text-red-500'/>Invalid Node</span></div>
        <span className='text-[9px] text-[#1a192b] dark:text-white'>Somewhere along the path<br/> an error occurred making this node unable to display</span>
    </div>
);

export default InvalidNode;