import {useState, useCallback, useEffect, useRef, useMemo} from 'react'
import { useDrop } from 'react-dnd'
import { Agent, callAgent, createScene, updateScene, getSceneList, deleteScene } from '@/pages/api/apis'
import type { Scene } from '@/pages/api/apis'
import LeftPanel from "@/components/LeftPanel"
import {
    addEdge,
    applyEdgeChanges,
    applyNodeChanges,
    Background,
    Controls,
    type Edge,
    type Node,
    type OnConnect,
    type OnEdgesChange,
    type OnNodesChange,
    ReactFlow,
    useEdgesState,
    useNodesState,
    MarkerType
} from "@xyflow/react"
import '@xyflow/react/dist/style.css'
import DeletableNode from "@/components/Flow/DeletableNode";

// 初始化组件
export default function CenterPanel() {
    const [workflowAgents, setWorkflowAgents] = useState<Agent[]>([]) // 用于存储按照顺序排列的工作流
    const [input, setInput] = useState('')
    const [output, setOutput] = useState('')
    const [currentOutput, setCurrentOutput] = useState<{ id: string, content: string }[]>([{ id: '', content: '' }])
    const [sceneExists, setSceneExists] = useState(false)
    const [sceneName, setSceneName] = useState("未命名")  // 新增：保存场景名称
    const [isEditingName, setIsEditingName] = useState(false)  // 新增：编辑模式状态
    const [sceneList, setSceneList] = useState<Scene[]>([])  // 场景列表
    const [sceneDropdown, setSceneDropdown] = useState(false)  // 场景下拉框状态

    const [selectedNode, setSelectedNode] = useState<Node | null>(null);



    // Agent Nodes
    const initialNodes: Node[] = [{ id: '1', data: { label: '🔥  start', id:'1' }, position: { x: 0, y: 0 }, sourcePosition: 'right', type: 'deletableNode', style: { border: '3px solid #1e2022' } }]
    const initialEdges: Edge[] = []

    const [nodes, setNodes] = useNodesState(initialNodes)
    const [edges, setEdges] = useEdgesState(initialEdges)
    const onNodesChange: OnNodesChange = useCallback(
        (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
        [setNodes]
    )
    const onEdgesChange: OnEdgesChange = useCallback(
        (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
        [setEdges]
    )
    const onConnect: OnConnect = useCallback(
        (params) => {
            setEdges((eds) => addEdge(params, eds))
        },
        [setEdges]
    )

    const deleteNode = (nodeId: string) => {
        // 删除当前节点及与之连接的边
        setNodes((nds) => nds.filter((node) => node.id !== nodeId));
        setEdges((eds) => eds.filter((edge) => edge.source !== nodeId && edge.target !== nodeId));
        setSelectedNode(null);  // 删除后取消选中
    };

    const nodeTypes = useMemo(() => ({
        deletableNode: (props) => <DeletableNode {...props} deleteNode={deleteNode} />, // 将 deleteNode 传递给子组件
    }), [deleteNode]);

    const onNodeClick = useCallback(
        (event: React.MouseEvent, node: Node) => {
            setSelectedNode(node); // 选中当前点击的节点
        },
        []
    );

    const nodeIcon = ['💬', '📈', '💻', '🎨']

    const agentsRef = useRef<Agent[]>([])

    const [{ isOver }, drop] = useDrop(() => ({
        accept: 'AGENT',
        drop: (item: Agent, monitor) => {
            const clientOffset = monitor.getClientOffset()
            if (!clientOffset) return
            // 将代理添加到 refs 中
            agentsRef.current = [...agentsRef.current, item]
            setNodes((prevNodes) => [
                ...prevNodes,
                { id: item.id, data: { label: nodeIcon[item.kind] + item.name , id: item.id }, position: { x: clientOffset.x - 600, y: clientOffset.y - 200 }, type: 'deletableNode' }
            ])
        },
        collect: (monitor) => ({
            isOver: monitor.isOver()
        })
    }))

    /**
     * @description 获取场景列表
     */
    const fetchSceneList = async () => {
        const res = await getSceneList({ page: 1, pageSize: 10 })
        const sceneList:Scene[] = res.payload?.scenes
        setSceneList(sceneList)
        console.log(sceneList)
    }

    useEffect(() => {
        fetchSceneList()
    }, [])

    const handleSelectScene = (sceneId: string) => {
        const selectedScene: Scene | undefined = sceneList.find(scene => scene.id === sceneId)
        if (!selectedScene) return
        setSceneExists(true)
        setSceneName(selectedScene.name)
        updateGraphFromScene(selectedScene.agents)
    }

    /**
     * @description 从场景中更新ReactFlow图
     * @param agents
     */
    const updateGraphFromScene = (agents: Agent[]) => {
        // 清空现有节点和边
        setEdges(initialEdges)
        setNodes(initialNodes)
        agentsRef.current = []

        // 在开头添加start节点
        const startNode: Node = {
            id: 'start',
            data: { label: '🔥  start' ,id : '1'},
            position: { x: 0, y: 0 },
            type: 'deletableNode',
            style: { border: '3px solid #1e2022' }
        }

        // 更新节点
        const newNodes = [startNode, ...agents.map((agent, index) => {
            agentsRef.current = [...agentsRef.current, agent]
            return {
                id: agent.id,
                data: { label: nodeIcon[agent.kind] + agent.name, id: agent.id },
                position: { x: (index + 1) * 300, y: index % 2 === 1 ? 0 : 100 },
                type: 'deletableNode',
            }
        })]
        setNodes(newNodes)

        // 创建连接每个代理节点的边
        const newEdges = agents.slice(1).map((agent, index) => ({
            id: `e${agents[index].id}-${agent.id}`,
            source: agents[index].id,
            target: agent.id,
            markerEnd: { type: MarkerType.ArrowClosed },
            animated: true,
            style: { stroke: '#1e2022', strokeWidth: 2 }
        }))

        // 添加start节点到第一个代理节点的边
        setEdges([
            {
                id: `e_start-${agents[0].id}`,
                source: 'start',
                target: agents[0].id,
                markerEnd: { type: MarkerType.ArrowClosed },
                animated: true,
                style: { stroke: '#1e2022', strokeWidth: 2 }
            },
            ...newEdges
        ])
    }

    /**
     * @description 创建场景
     */
    const handleCreateScene = async () => {
        console.log(workflowAgents)

        // 确保workflowAgents从"start"节点之后开始（不包括start节点本身）
        const newScene = { "name": sceneName, "agents": workflowAgents.map(agent => agent.id) }
        const res = await createScene(newScene)
        if (res.code == 0) {
            setSceneExists(true)
            console.log("create scene success", res)
        }
        await fetchSceneList()
    }


    /**
     * @description 更新场景
     */
    const handleUpdateScene = () => {
        console.log(workflowAgents)
        const newScene = { "name": sceneName, "agents": workflowAgents.map((agent) =>agent.id) }
        const res = updateScene(newScene)
        if(res?.code == 0){
            console.log("update scene success",res)
        }
    }

    /**
     * @description 删除场景
     */
    const handleDeleteScene = async () => {
        const currentSceneId = sceneList.find(scene => scene.name === sceneName)?.id
        if(!currentSceneId) return
        console.log(currentSceneId)
        const res = await deleteScene({id :currentSceneId})
        if(res?.code == 0){
            console.log("delete scene success",res)
            window.location.reload();
            return
        }
        console.error(res)
    }

    /**
     * @description 根据 edges 设置WorkflowAgents
     */
    useEffect(() => {
        const order = getWorkflowOrder(edges)  // 获取顺序

        // 使用 refs 获取代理数组
        const orderedAgents = order
            .map(id => agentsRef.current.find(agent => agent.id === id))
            .filter(agent => agent)  // 过滤掉未找到的 agent
        setWorkflowAgents(orderedAgents)
    }, [edges])

    /**
     * @description 执行工作流
     */
    const executeWorkflow = async () => {
        let currentInput = input // 初始输入
        let finalOutput = "" // 最终拼接的输出内容

        // 遍历顺序的 workflowAgents 来逐个执行
        for (let i = 0; i < workflowAgents.length; i++) {
            const agent = workflowAgents[i]
            const result = await executeAgent(agent, currentInput)
            finalOutput += result.content
            currentInput = result.content

            // 更新每个 agent 的输出
            setCurrentOutput(prev => [
                ...prev,
                { id: agent.id, content: result.content }
            ])
        }
        setOutput(finalOutput)
    }

    /**
     * @description 执行单个agent
     * @param agent
     * @param input
     */
    const executeAgent = async (agent: Agent, input: string) => {
        const res = await callAgent({
            id: agent.id,
            kind: agent.kind,
            input: input,
        })

        const reader = res.body?.getReader()
        const decoder = new TextDecoder("utf-8")
        let partialContent = ""

        let done = false
        while (!done) {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-expect-error
            const { value, done: isDone } = await reader.read()
            done = isDone

            const chunk = decoder.decode(value, { stream: true })
            const lines = chunk.split("\n").filter(line => line.trim())

            for (const line of lines) {
                try {
                    const parsedData = JSON.parse(line)
                    if (parsedData.content) {
                        partialContent += parsedData.content
                        setCurrentOutput([{ id: agent.id, content: partialContent }])
                    }
                } catch (e) {
                    console.error("Failed to parse line:", line, e)
                }
            }
        }

        return { content: partialContent }
    }

    /**
     * @description 根据edges输出工作流顺序
     */
    const getWorkflowOrder = (edges: Edge[]) => {
        // 构建一个图
        const graph: { [key: string]: string[] } = {}
        const allNodes = new Set<string>()

        // 处理 edges 构建图
        edges.forEach(edge => {
            const { source, target } = edge
            if (!graph[source]) graph[source] = []
            graph[source].push(target)
            allNodes.add(source)
            allNodes.add(target)
        })

        // 拓扑排序函数
        const topologicalSort = () => {
            const visited: Set<string> = new Set()
            const result: string[] = []
            const visit = (node: string) => {
                if (visited.has(node)) return
                visited.add(node)

                if (graph[node]) {
                    graph[node].forEach(visit)
                }

                result.push(node)
            }

            allNodes.forEach(visit)
            return result.reverse() // 返回的顺序是从开始到结束
        }

        return topologicalSort()
    }

    /**
     * @description edges样式更改
     */
    const customEdges = edges.map(edge => ({
        ...edge,
        markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 15,
            height: 15,
            color: '#1e2022',
        },
        animated: true,
        style: { stroke: '#1e2022', strokeWidth: 2 }
    }))

    /**
     * @description nodes样式更改
     */
    const customNodes = nodes.map(node => ({
        ...node,
        style: { border: 'none' },
        sourcePosition: 'right',
        targetPosition: 'left',
    }))

    // 编辑场景名称
    const handleNameClick = () => {
        setIsEditingName(true)
    }

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSceneName(e.target.value)
    }

    const handleNameBlur = () => {
        setIsEditingName(false)
    }


    // @ts-ignore
    return (
        <>
            <LeftPanel workflowAgents={workflowAgents} currentOutput={currentOutput} />
            <div ref={drop} className="flex flex-col p-4 w-2/3">
                <div className="mb-4 flex justify-between pl-4 pr-4 pt-4">
                    <div className={"flex"}>
                        <h2 className="text-xl font-bold">我的工作流</h2>
                        <h2
                            className={"text-xl font-bold ml-4"}
                            onClick={handleNameClick}
                        >
                            {isEditingName ? (
                                <input
                                    type="text"
                                    value={sceneName}
                                    onChange={handleNameChange}
                                    onBlur={handleNameBlur}
                                    className="border-b-2"
                                />
                            ) : (
                                sceneName
                            )}
                        </h2>
                    </div>

                    <div className={"flex"}>
                        {
                            sceneExists &&
                            <button
                                onClick={handleDeleteScene}
                                className="px-4 py-2 bg-gray-200 border border-gray-300 ml-4 text-black rounded"
                            >
                                删除场景
                            </button>
                        }
                        {/* 场景选择下拉框 */}
                        <div className="relative">
                            <button
                                className="px-4 py-2 bg-gray-200 border border-gray-300 text-black rounded w-30 ml-4"
                                onClick={() => setSceneDropdown(!sceneDropdown)}
                            >
                                选择场景
                            </button>
                            {
                                sceneDropdown &&
                                <div
                                    className="absolute px-0 py-2 left-0 mt-2 bg-white rounded z-50 w-34"
                                    onMouseLeave={()=> setSceneDropdown(false)}
                                >
                                    {sceneList.map((scene) => (
                                        <div
                                            key={scene.id}
                                            onClick={() => handleSelectScene(scene.id)}
                                            className="px-4 py-2 hover:bg-gray-100 cursor-pointer z-20"
                                        >
                                            {scene.name}
                                        </div>
                                    ))}
                                </div>
                            }
                        </div>
                        {
                            sceneExists ?
                                <button
                                    onClick={handleUpdateScene}
                                    className="px-4 py-2 bg-gray-200 border border-gray-300 ml-4 text-black rounded"
                                >
                                    保存场景
                                </button>
                                :
                                <button
                                    onClick={handleCreateScene}
                                    className="px-4 py-2 bg-gray-200 border border-gray-300 ml-4 text-black rounded"
                                >
                                    创建场景
                                </button>
                        }
                    </div>
                </div>

                <div className="w-full h-96 pl-4 pr-4 rounded ">
                    <ReactFlow
                        className={"relative"}
                        nodes={customNodes}
                        nodeTypes={nodeTypes}
                        edges={customEdges}
                        onNodesChange={onNodesChange}
                        onEdgesChange={onEdgesChange}
                        onNodeClick={onNodeClick}
                        onConnect={onConnect}
                        minZoom={0.5}
                        maxZoom={2}>
                        <Background bgColor="#f9f9f9" gap={16} className={"rounded"} />
                        <Controls />
                    </ReactFlow>
                </div>

                {/* Input */}
                <div className="mb-4 pr-4 pl-4 mt-4 ">
                    <div className={"flex justify-between relative"}>
                        <div className="font-bold mb-3 p-2  w-1/4 pl-6 border-b-2 rounded bg-gray-100">
                            输入
                        </div>
                        <button
                            onClick={executeWorkflow}
                            className="absolute right-0 px-4 py-2 mb-2 bg-green-600 text-white rounded ml-4"
                        >
                            执行工作流
                        </button>
                    </div>

                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        className="w-full p-2 border-gray-300 border rounded h-60 bg-white "
                    />
                </div>
            </div>
        </>
    )
}
