import { Handle, Position } from "@xyflow/react";
import React, { useState } from "react";


export default function DeletableNode( {data,deleteNode} ) {

    const [isFocus, setIsFocus] = useState(false);
    const handleDelete = ()=>{
        console.log("delete node",data.id)
        deleteNode(data.id)
    }

    return (
        <div
            className={`bg-white max-h-18 w-60 py-3 rounded flex justify-center items-center  ${isFocus ? "border-black" : "shadow-gray-300"}`}
            onMouseMoveCapture={()=>{setIsFocus(true)}}
            onMouseOutCapture={()=>{setIsFocus(false)}}
        >
            {
                data.id === '1' ||
                <Handle type="target" position={Position.Left} />
            }
            <label className={"flex relative items-center font-bold h-8 mr-auto ml-6"}>
                {
                    JSON.stringify(data.label).replace(/^["']|["']$/g, '')
                }
                {
                    data.id === '1' ||
                    <button
                        onClick={handleDelete}
                        className={`ml-auto mr-2 h-8 w-8 ${isFocus ? "block" : "hidden"}`}
                    >
                        ❌
                    </button>
                }
            </label>
            <Handle type="source" position={Position.Right}/>
        </div>
    )
}