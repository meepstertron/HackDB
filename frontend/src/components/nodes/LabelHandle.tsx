import { Handle, Position, HandleType } from "@xyflow/react";
import "@/index.css"

interface LabelHandleProps {
    type: HandleType;
    position: Position;
    id: string;
    label?: string;
    style?: React.CSSProperties;
}

function LabelHandle({ type, position, id, label = "Input", style }: LabelHandleProps) {
    return (
        <>
            <Handle
            type={type}
            position={position}
            id={id}
            style={style}

            >
                <div className={`handletext-${position} text-[9px] font-mono`}>{label}</div>
            </Handle>
        </>
    );
}

export default LabelHandle;