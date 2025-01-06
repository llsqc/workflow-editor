import { CreateAgentData, PainterAgent } from '@/pages/api/apis'

export default function PainterForm({ formData, setFormData }: { formData: Partial<PainterAgent>, setFormData: (data: Partial<PainterAgent>) => void }) {
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
                <label className="block mb-2">风格</label>
                <input
                    type="text"
                    value={formData.style || ''}
                    onChange={e => setFormData({ ...formData, style: e.target.value })}
                    className="w-full p-2 border rounded"
                />
            </div>
        </>
    )
} 