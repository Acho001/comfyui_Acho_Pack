import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "Acho.SimpleCode",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "Acho_SimpleCode") {
            
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                const refreshSlots = () => {
                    const inputCountWidget = this.widgets.find(w => w.name === "input_count");
                    const outputCountWidget = this.widgets.find(w => w.name === "output_count");
                    if (!inputCountWidget || !outputCountWidget) return;

                    const targetInCount = inputCountWidget.value;
                    const targetOutCount = outputCountWidget.value;

                    // 1. 处理输入接口 (input_0, input_1...)
                    // 移除所有现有的动态输入
                    if (this.inputs) {
                        for (let i = this.inputs.length - 1; i >= 0; i--) {
                            if (this.inputs[i].name.startsWith("input_")) {
                                this.removeInput(i);
                            }
                        }
                    }
                    // 重新添加指定数量的输入
                    for (let i = 0; i < targetInCount; i++) {
                        this.addInput(`input_${i}`, "*");
                    }

                    // 2. 处理输出接口 (output_0, output_1...)
                    if (this.outputs) {
                        for (let i = this.outputs.length - 1; i >= 0; i--) {
                            if (this.outputs[i].name.startsWith("output_")) {
                                this.removeOutput(i);
                            }
                        }
                    }
                    for (let i = 0; i < targetOutCount; i++) {
                        this.addOutput(`output_${i}`, "*");
                    }

                    this.onResize?.(this.size);
                };

                // 添加真正的按钮 (模仿 KJNodes 样式)
                this.addWidget("button", "Update Slots (刷新接口)", null, () => {
                    refreshSlots();
                });

                // 初始同步：延迟执行以确保节点已完全构建
                setTimeout(() => {
                    // 只有在没有连接时才自动刷新，防止破坏加载的工作流
                    let hasLinks = false;
                    if (this.inputs) {
                        for (let i of this.inputs) if (i.link !== null) hasLinks = true;
                    }
                    if (this.outputs) {
                        for (let o of this.outputs) if (o.links && o.links.length > 0) hasLinks = true;
                    }
                    if (!hasLinks) refreshSlots();
                }, 100);

                return r;
            };
        }
    },
});