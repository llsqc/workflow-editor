import { CreateAgentData, JudgeAgent } from '@/pages/api/apis'
import React from "react";

export default function JudgerForm({
                                       formData,
                                       setFormData
                                   }: {
    formData: Partial<JudgeAgent>;
    setFormData: (data: Partial<JudgeAgent>) => void;
}) {
    // 维护一个键值对的数组
    const [outputArray, setOutputArray] = React.useState<{ key: string, value: string }[]>(
        formData.output ? Object.entries(formData.output).map(([key, value]) => ({ key, value })) : []
    );

    const [isSaved, setIsSaved] = React.useState(false);

    // 更新输出
    const handleOutputChange = (index: number, key: string, value: string) => {
        const updatedArray = [...outputArray];
        updatedArray[index] = { key, value };
        setOutputArray(updatedArray);
    };

    // 添加新的键值对
    const handleAddOutputField = () => {
        setOutputArray([
            ...outputArray,
            { key: `key${outputArray.length + 1}`, value: '' }
        ]);
    };

    // 删除指定的键值对
    const handleRemoveOutputField = (index: number) => {
        const updatedArray = outputArray.filter((_, i) => i !== index);
        setOutputArray(updatedArray);
    };

    // 保存时将 outputArray 转换为对象
    const handleSave = () => {
        const updatedOutput = outputArray.reduce((acc, { key, value }) => {
            acc[key] = value;
            return acc;
        }, {} as { [key: string]: string });

        setFormData({ ...formData, output: updatedOutput });
        setIsSaved(true);
        alert("保存成功！")
    };

    React.useEffect(() => {
        // 更新 formData 的 output 字段
        setFormData({ ...formData, output: outputArray.reduce((acc, { key, value }) => {
                acc[key] = value;
                return acc;
            }, {} as { [key: string]: string }) });
    }, [outputArray, setFormData, formData]);

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
                {outputArray.map((item, index) => (
                    <div key={index} className="flex mb-2 items-center">
                        <div>当</div>
                        <input
                            type="text"
                            value={item.key}
                            onChange={e => handleOutputChange(index, e.target.value, item.value)}
                            className="w-1/4 p-2 border rounded mr-2"
                        />
                        <div>时</div>
                        <input
                            type="text"
                            value={item.value}
                            onChange={e => handleOutputChange(index, item.key, e.target.value)}
                            className="w-3/5 p-2 border rounded"
                        />

                        {
                            isSaved ||
                            <button
                                type="button"
                                onClick={() => handleRemoveOutputField(index)}
                                className="ml-1 bg-red-500 text-white rounded w-5 h-5"
                            >
                                -
                            </button>
                        }
                    </div>
                ))}

                {
                    isSaved ||
                    <button
                        type="button"
                        onClick={handleAddOutputField}
                        className="text-blue-500 mt-2"
                    >
                        添加
                    </button>
                }
            </div>

            {isSaved ?
                <button
                    type="button"
                    onClick={() => setIsSaved(false)}
                    className="text-green-500 mt-4"
                >
                    编辑
                </button>
                :
                <button
                    type="button"
                    onClick={handleSave}
                    className="text-green-500 mt-4"
                >
                    保存
                </button>
            }


        </>
    );
}
