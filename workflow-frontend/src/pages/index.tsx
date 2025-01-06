import { useState } from 'react'
import RightPanel from '@/components/RightPanel'
import { Agent } from './api/apis'

export default function Home() {
  const [executionResults, setExecutionResults] = useState<string[]>([])
  const [sequence, setSequence] = useState<Agent[]>([])

  return (
    <div className="flex h-screen">
      <RightPanel onAgentAdd={(agent: Agent) => {
        // 添加agent到右侧面板逻辑
      }} />
    </div>
  )
}
