import { CreateAgentData, JudgeAgent } from '@/pages/api/apis'

export default function JudgerForm({ formData, setFormData }: { formData: Partial<JudgeAgent>, setFormData: (data: Partial<JudgeAgent>) => void }) {
    // 更新输出
    const handleOutputChange = (key: string, value: string) => {
        const updatedOutput = { ...formData.output };
        updatedOutput[key] = value;
        setFormData({ ...formData, output: updatedOutput });
    };

    // 添加新的键值对
    const handleAddOutputField = () => {
        const updatedOutput = { ...formData.output };
        updatedOutput[`key${Object.keys(updatedOutput).length + 1}`] = '';  // Add a new key-value pair with an incremented key
        setFormData({ ...formData, output: updatedOutput });
    };

    // 删除指定的键值对
    const handleRemoveOutputField = (key: string) => {
        const updatedOutput = { ...formData.output };
        delete updatedOutput[key]; // 删除指定的键
        setFormData({ ...formData, output: updatedOutput });
    };

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
                {formData.output && Object.keys(formData.output).map((key, index) => (
                    <div key={index} className="flex mb-2 items-center">
                        <div>当</div>
                        <input
                            type="text"
                            value={key}
                            onChange={e => handleOutputChange(e.target.value, formData.output[key])}
                            className="w-1/4 p-2 border rounded mr-2"
                        />
                        <div>时</div>
                        <input
                            type="text"
                            value={formData.output[key] || ''}
                            onChange={e => handleOutputChange(key, e.target.value)}
                            className="w-3/5 p-2 border rounded"
                        />
                        <button
                            type="button"
                            onClick={() => handleRemoveOutputField(key)}
                            className="ml-1 bg-red-500 text-white rounded w-5 h-5"
                        >
                            -
                        </button>
                    </div>
                ))}
                <button
                    type="button"
                    onClick={handleAddOutputField}
                    className="text-blue-500 mt-2"
                >
                    添加
                </button>
            </div>
        </>
    );
}
