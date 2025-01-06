import { CreateAgentData, JudgeAgent } from '@/pages/api/apis'

export default function JudgerForm({ formData, setFormData }: { formData: Partial<JudgeAgent>, setFormData: (data: Partial<JudgeAgent>) => void }) {
    return (
        <>
            <div className="mb-4">
                <label className="block mb-2">身份设置</label>
                <input
                    type="text"
                    value={formData.identity_setting || ''}
                    onChange={e => setFormData({ ...formData, identity_setting: e.target.value })}
                    className="w-full p-2 border rounded"
                />
            </div>
            <div className="mb-4">
                <label className="block mb-2">任务</label>
                <input
                    type="text"
                    value={formData.task || ''}
                    onChange={e => setFormData({ ...formData, task: e.target.value })}
                    className="w-full p-2 border rounded"
                />
            </div>
            <div className="mb-4">
                <label className="block mb-2">输出</label>
                <input
                    type="text"
                    value={formData.output || ''}
                    onChange={e => setFormData({ ...formData, output: e.target.value.split(',') })}
                    className="w-full p-2 border rounded"
                />
            </div>
        </>
    )
} 