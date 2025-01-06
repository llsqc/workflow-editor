import { CreateAgentData, HandleAgent, PainterAgent } from '@/pages/api/apis'
import { Editor } from '@monaco-editor/react'

export default function HandlerForm({ formData, setFormData }: { formData: Partial<HandleAgent>, setFormData: (data: Partial<HandleAgent>) => void }) {
    // 编辑器内容变化时更新状态
    const handleEditorChange = (value: string | undefined) => {
        setFormData({ ...formData, deal: value || '' });
    };

    return (
        <div>
            <div className="mb-4">
                <label className="block mb-2">代码块</label>
                <div className="relative">
                    <Editor
                        className={"w-full pt-2"}
                        height="350px"  // 设置编辑器高度
                        language="python"  // 设置代码语言为 Python
                        theme="vs-dark"  // 设置主题，可以选择 "vs-dark" 或 "light"
                        value={formData.deal || ''}  // 设置初始值
                        onChange={handleEditorChange}  // 监听代码变化
                        options={{
                            selectOnLineNumbers: true,
                            minimap: { enabled: false },  // 禁用右侧缩略图
                            fontSize: 16,  // 设置字体大小
                        }}
                    />
                </div>
            </div>
        </div>
    )
}
