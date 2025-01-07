import React, { useState, useEffect } from 'react';
import { Agent } from "@/pages/api/apis";
import {marked} from 'marked';
import styles from './LeftPanel.module.css';


interface LeftPnelProps {
    workflowAgents: Agent[];  // 工作流中的所有 agents
    currentOutput: { id: string, content: string }[];  // 当前的输出
}

const LeftPanel = ({ workflowAgents, currentOutput }: LeftPnelProps) => {
    // 使用 useState 来存储 output 缓存
    const [outputCache, setOutputCache] = useState<{ [key: string]: string }>({});

    // 每次 currentOutput 更新时，更新缓存
    useEffect(() => {
        const newCache = { ...outputCache }; // 复制当前缓存
        currentOutput.forEach(output => {
            if (newCache[output.id] !== output.content) {
                newCache[output.id] = output.content;
            }
        });
        setOutputCache(newCache); // 更新缓存
    }, [currentOutput]);

    // 将 Markdown 转换为 HTML
    const renderMarkdown = (content: string) => {
        return { __html: marked(content) };
    };

    return (
        <div className={"w-1/3 border-r max-h-full overflow-y-auto"}>
            <div className="text-xl font-bold -mb-1 p-4 pt-5 pl-6 pb-3 sticky border-b-2 top-0 bg-gray-100">输出</div>
            <div className="space-y-4 p-4">
                {workflowAgents.length > 0 ? (
                    workflowAgents.map((agent, index) => (
                        <div key={agent.id} className="p-2 border-0 rounded-md">
                            <div className="font-semibold mb-3 rounded p-3 bg-gray-100">{`Step ${index + 1}: ${agent.name}`}</div>
                            {
                                outputCache[agent.id] !== undefined ? (
                                    <div
                                        className="markdown-output p-4 border"
                                        dangerouslySetInnerHTML={renderMarkdown(outputCache[agent.id])}
                                    />
                                ) : (
                                    <p>未执行</p>
                                )
                            }
                        </div>
                    ))
                ) : (
                    <p className="text-gray-500">没有待执行的步骤。</p>
                )}
            </div>
        </div>
    );
};

export default LeftPanel;
