import { AnalyseAgent, CreateAgentData } from '@/pages/api/apis'

export default function AnalyserForm({ formData, setFormData }: { formData: Partial<AnalyseAgent>, setFormData: (data: Partial<AnalyseAgent>) => void }) {
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
                <textarea
                    value={formData.task || ''}
                    onChange={e => setFormData({ ...formData, task: e.target.value })}
                    className="w-full p-2 border rounded h-40 "
                />
            </div>
        </>
    )
}
