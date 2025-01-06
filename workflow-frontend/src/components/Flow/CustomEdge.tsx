import {
    BaseEdge,
    EdgeLabelRenderer,
    getStraightPath,
    useReactFlow,
} from "@xyflow/react";

export default function CustomEdge({id, sourceX, sourceY, targetX, targetY}){
    const {setEdges} = useReactFlow();
    const [edgePath, labelX, labelY] = getStraightPath({sourceX, sourceY, targetX, targetY});

    return (
        <>
            <BaseEdge id={id} path={edgePath} />
            <EdgeLabelRenderer>
                <button
                    style={{position: 'absolute',
                        transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`}}
                    className="nodrag nopan"
                    onClick={() => {
                        setEdges((edges) => edges.filter((edge) => edge.id !== id));
                    }}
                >
                    删除
                </button>
            </EdgeLabelRenderer>
        </>
    );
}