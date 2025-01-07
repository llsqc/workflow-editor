import { useState, useEffect } from 'react'
import { Agent, getAgentList, deleteAgent, updateAgent, createAgent, AnalyseAgent, JudgeAgent, HandleAgent, PainterAgent, getSceneList } from '@/pages/api/apis'
import AnalyserForm from './Right/AnalyserForm'
import JudgeForm from './Right/JudgerForm'
import HandlerForm from './Right/HandlerForm'
import PainterForm from './Right/PainterForm'
import CenterPanel from './CenterPanel'
import { useDrag, useDrop } from 'react-dnd';


interface RightPanelProps {
    onAgentAdd: (agent: Agent) => void
}

export default function RightPanel({ onAgentAdd }: RightPanelProps) {
    const [agents, setAgents] = useState<Agent[]>([])
    const [showAddForm, setShowAddForm] = useState(false)
    const [editAgent, setEditAgent] = useState<Agent | null>(null)

    const fetchData = async () => {
        const allAgents: Agent[] = []
        for(let i = 0; i < 4; i++){
            const res = await getAgentList(i)
            if(res.payload){
                allAgents.push(...res.payload)
            }
        }
        setAgents(allAgents)
    }

    useEffect(() => {
        fetchData()
    }, []);

    const groupedAgents = agents.reduce((acc, agent) => {
        if (!acc[agent.kind]) {
            acc[agent.kind] = []
        }
        acc[agent.kind].push(agent)
        return acc
    }, {} as Record<number, Agent[]>)

    return (
        <>
            <CenterPanel agents={agents} />
            <div className="w-1/4  border-l pl-6 pr-4  overflow-y-auto relative   " >
                <div className="flex justify-between items-center -ml-6 mb-4 pt-5 sticky top-0 pb-3 pl-6 -mr-4  bg-gray-100 border-b-2 px-4">
                    <div className="text-xl font-bold  sticky top-0 w-full h-15">Agent列表</div>
                    <button
                        onClick={() => setShowAddForm(true)}
                        className="text-2xl bg-black border border-gray-300 ml-4 px-3 text-white rounded "
                    >
                        +
                    </button>
                </div>

                {Object.entries(groupedAgents).map(([kind, agents]) => (
                    <AgentGroup
                        key={kind}
                        kind={parseInt(kind)}
                        agents={agents}
                        onEditAgent={(agent) => setEditAgent(agent)}
                    />
                ))}

                {showAddForm && (
                    <AddAgentForm
                        onClose={() => setShowAddForm(false)}
                        onAdd={async (data) => {
                            const res = await createAgent(data)
                            const newAgent: Agent = {
                                ...data,
                                id: res.payload
                            }
                            setAgents([...agents, newAgent])
                            onAgentAdd(newAgent)
                            setShowAddForm(false)
                        }}
                    />
                )}

                {editAgent && (
                    <EditAgentForm
                        agent={editAgent}
                        onClose={() => setEditAgent(null)}
                        onDelete={async (agent) => {
                            await deleteAgent(agent.id)
                            await fetchData()
                            setEditAgent(null)
                        }}
                        onUpdate={async (updatedAgent) => {
                            await updateAgent({...updatedAgent})
                            await fetchData()
                            onAgentAdd(updatedAgent)
                            setEditAgent(null)
                        }}
                    />
                )}


            </div>
        </>
    )
}

function AgentGroup({ kind, agents, onEditAgent }: { kind: number, agents: Agent[], onEditAgent: (agent: Agent) => void }) {
    const [isExpanded, setIsExpanded] = useState(true)
    const kindNames = ['Analyser', 'Judge', 'Handler', 'Painter']
    const icons = ['💬', '📈', '💻', '🎨']

    return (
        <div className="mb-4">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full text-left font-bold p-2 bg-gray-100"
            >
                {kindNames[kind]} ({agents.length})
            </button>
            {isExpanded && (
                <div className="space-y-2 mt-2">
                    {agents.map((agent) => (
                        <AgentCard key={agent.id} agent={agent} onEdit={() => onEditAgent(agent)} />
                    ))}
                </div>
            )}
        </div>
    )
}

function AgentCard({ agent, onEdit }: { agent: Agent, onEdit: () => void }) {
    const [{ isDragging }, drag] = useDrag(() => ({
        type: 'AGENT',
        item: { ...agent },
        collect: (monitor) => ({
            isDragging: monitor.isDragging()
        })
    }))
    const icons = ['💬', '📈', '💻', '🎨']

    return (
        <div
            ref={drag}
            className={`p-4 border rounded ${isDragging ? 'opacity-50' : ''}`}
            onClick={onEdit}
        >
            <h3 className="font-bold">{icons[agent.kind] + agent.name}</h3>
            <p className="text-sm overflow-hidden max-w-full">{agent.description}</p>
        </div>
    )
}

function AddAgentForm({ onClose, onAdd }: { onClose: () => void, onAdd: (data: any) => Promise<void> }) {
    const [kindData, setKindData] = useState({ kind: 0 })

    const kindOptions = [
        { value: 0, label: 'Analyser' },
        { value: 1, label: 'Judge' },
        { value: 2, label: 'Handler' },
        { value: 3, label: 'Painter' }
    ]

    const [formData, setFormData] = useState<Partial<AnalyseAgent | JudgeAgent | HandleAgent | PainterAgent>>({
        kind: kindData.kind,
        name: '',
        description: '',
        avatar: '',
    })

    useEffect(() => {
        switch (kindData.kind) {
            case 0:
                setFormData({ ...formData, kind: 0, identity_setting: '', task: '' })
                break
            case 1:
                setFormData({ ...formData, kind: 1, identity_setting: '', task: '', output: [] })
                break
            case 2:
                setFormData({ ...formData, kind: 2, identity_setting: '', task: '' })
                break
            case 3:
                setFormData({ ...formData, kind: 3, identity_setting: '', style: '' })
                break
            default:
                break
        }
    }, [kindData.kind])

    const renderForm = () => {
        switch (formData.kind) {
            case 0:
                return <AnalyserForm formData={formData as Partial<AnalyseAgent>} setFormData={setFormData} />
            case 1:
                return <JudgeForm formData={formData as Partial<JudgeAgent>} setFormData={setFormData} />
            case 2:
                return <HandlerForm formData={formData as Partial<HandleAgent>} setFormData={setFormData} />
            case 3:
                return <PainterForm formData={formData as Partial<PainterAgent>} setFormData={setFormData} />
            default:
                return null
        }
    }

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="bg-white p-4 rounded max-w-md w-full">
                <div>
                    <div className="mb-4">
                        <label className="block mb-2">类型</label>
                        <select
                            value={kindData.kind}
                            onChange={e => {
                                const newKind = Number(e.target.value)
                                setKindData({ kind: newKind })
                                setFormData({ ...formData, kind: newKind })
                            }}
                            className="w-full p-2 border rounded"
                        >
                            {kindOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="mb-4">
                        <label className="block mb-2">名称</label>
                        <input
                            type="text"
                            value={formData.name || ''}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                            className="w-full p-2 border rounded"
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block mb-2">描述</label>
                        <input
                            type="text"
                            value={formData.description || ''}
                            onChange={e => setFormData({ ...formData, description: e.target.value })}
                            className="w-full p-2 border rounded"
                        />
                    </div>
                    {renderForm()}
                    <div className="flex justify-end gap-2">
                        <button type="button" onClick={onClose} className="px-4 py-2 border rounded">
                            取消
                        </button>
                        <button onClick={() => onAdd(formData)} className="px-4 py-2 bg-blue-500 text-white rounded">
                            添加
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

function EditAgentForm({ agent, onClose, onUpdate, onDelete }: { agent: Agent, onClose: () => void, onUpdate: (agent: Agent) => void, onDelete: (agent: Agent) => void }) {
    const [formData, setFormData] = useState<Partial<AnalyseAgent | JudgeAgent | HandleAgent | PainterAgent>>({
        ...agent
    })


    const renderForm = () => {
        switch (formData.kind) {
            case 0:
                return <AnalyserForm formData={formData as Partial<AnalyseAgent>} setFormData={setFormData} />
            case 1:
                return <JudgeForm formData={formData as Partial<JudgeAgent>} setFormData={setFormData} />
            case 2:
                return <HandlerForm formData={formData as Partial<HandleAgent>} setFormData={setFormData} />
            case 3:
                return <PainterForm formData={formData as Partial<PainterAgent>} setFormData={setFormData} />
            default:
                return null
        }
    }


    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div className="bg-white p-4 rounded max-w-xl w-full">
                <div>
                    <div className="mb-4">
                        <label className="block mb-2">名称</label>
                        <input
                            type="text"
                            value={formData.name || ''}
                            onChange={e => setFormData({ ...formData, name: e.target.value })}
                            className="w-full p-2 border rounded"
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block mb-2">描述</label>
                        <input
                            type="text"
                            value={formData.description || ''}
                            onChange={e => setFormData({ ...formData, description: e.target.value })}
                            className="w-full p-2 border rounded"
                        />
                    </div>
                    {renderForm()}
                    <div className="flex justify-end gap-2">
                        <button type="button" onClick={()=>onDelete(formData)} className="px-4 py-2 border-red-500 text-red-500 rounded">
                            删除
                        </button>
                        <button type="button" onClick={onClose} className="px-4 py-2 border rounded">
                            取消
                        </button>
                        <button onClick={() => onUpdate(formData)} className="px-4 py-2 bg-blue-500 text-white rounded">
                            保存
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}